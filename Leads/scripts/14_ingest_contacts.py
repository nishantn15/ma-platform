"""
14_ingest_contacts.py
---------------------
Upsert one AlphaSense contact result into the `contacts` table.
Called after each exhaustive-contact as_search query. Derives the single
best actionable channel (primary_*) per the locked rule:
  named-exec DIRECT email when literally published  ->  else IR inbox
  ->  else IR-advisor agency  ->  else RTA.
Never fabricates name+domain emails. Provenance preserved.

Usage: python3 14_ingest_contacts.py <payload.json>

payload.json shape (mirrors the AS exhaustive-contact JSON):
{
  "nse_symbol": "TANLA", "as_company_id": "TK359503",
  "general_ir": {"email","phone","desk_name"},
  "named_ir_contacts": [{"name","title","email","phone"}],
  "company_secretary": {"name","email","phone"},
  "cfo": {"name","email"}, "ceo_md": {"name","title"}, "chairman": {"name"},
  "ir_advisor_agency": {"firm","contact_name","email","phone"},
  "registrar_rta": {"firm","email","phone"},
  "registered_office", "corporate_office", "website",
  "best_channel_note": "...",
  "confidence": "high|medium|verify",
  "sources": [{"field","source","date"}]
}
"""
import json
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"


def g(d, *path):
    """Safe nested get."""
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur or None


def derive_primary(ir_head_name, ir_head_email, ir_inbox, advisor_contact,
                   advisor_firm, rta_email, rta_firm, cs_name):
    """Best actionable channel: named-direct email > IR inbox > advisor > RTA.
    A named email only counts as 'direct' if it differs from the generic IR
    inbox — AS often repeats the inbox in a person's email field, which is
    NOT a personal address and must not be mislabelled as named_direct."""
    def norm(e):
        return (e or "").strip().lower()
    if ir_head_email and norm(ir_head_email) != norm(ir_inbox):
        return ir_head_name, ir_head_email, "named_direct"
    if ir_inbox:
        # address it to a human if we have one
        return (ir_head_name or cs_name), ir_inbox, "ir_inbox"
    if advisor_contact or advisor_firm:
        return (advisor_firm or "IR advisor"), advisor_contact, "advisor"
    if rta_email:
        return (rta_firm or "Registrar"), rta_email, "rta"
    return None, None, None


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 14_ingest_contacts.py <payload.json>")
    p = json.loads(Path(sys.argv[1]).read_text())

    named = (p.get("named_ir_contacts") or [{}])
    head = named[0] if named else {}
    advisor = p.get("ir_advisor_agency") or {}
    advisor_contact = advisor.get("contact_name")
    if advisor_contact and (advisor.get("email") or advisor.get("phone")):
        extra = "; ".join(x for x in [advisor.get("email"), advisor.get("phone")] if x)
        advisor_contact = f"{advisor_contact} ({extra})"

    primary_name, primary_email, primary_kind = derive_primary(
        g(head, "name"), g(head, "email"), g(p, "general_ir", "email"),
        advisor_contact, advisor.get("firm"),
        g(p, "registrar_rta", "email"), g(p, "registrar_rta", "firm"),
        g(p, "company_secretary", "name"),
    )

    sources = p.get("sources") or []
    # contact_source / date = the source backing the primary email, else first source
    csrc, cdate = None, None
    if sources:
        csrc = "; ".join(sorted({s.get("source", "") for s in sources if s.get("source")}))[:300]
        dates = sorted({s.get("date", "") for s in sources if s.get("date")})
        cdate = dates[-1] if dates else None

    row = {
        "nse_symbol": p["nse_symbol"],
        "as_company_id": p.get("as_company_id"),
        "ir_inbox_email": g(p, "general_ir", "email"),
        "ir_phone": g(p, "general_ir", "phone"),
        "ir_head_name": g(head, "name"),
        "ir_head_title": g(head, "title"),
        "ir_head_email": g(head, "email"),
        "ir_head_phone": g(head, "phone"),
        "cs_name": g(p, "company_secretary", "name"),
        "cs_email": g(p, "company_secretary", "email"),
        "cfo_name": g(p, "cfo", "name"),
        "cfo_email": g(p, "cfo", "email"),
        "ceo_md_name": g(p, "ceo_md", "name"),
        "ceo_md_title": g(p, "ceo_md", "title"),
        "chairman_name": g(p, "chairman", "name"),
        "ir_advisor_firm": advisor.get("firm"),
        "ir_advisor_contact": advisor_contact,
        "rta_firm": g(p, "registrar_rta", "firm"),
        "rta_email": g(p, "registrar_rta", "email"),
        "rta_phone": g(p, "registrar_rta", "phone"),
        "registered_office": p.get("registered_office"),
        "corporate_office": p.get("corporate_office"),
        "website": p.get("website"),
        "primary_name": primary_name,
        "primary_email": primary_email,
        "primary_email_kind": primary_kind,
        "best_channel_note": p.get("best_channel_note"),
        "contact_source": csrc,
        "contact_date": cdate,
        "contact_confidence": p.get("confidence")
            or ("high" if primary_kind in ("named_direct", "ir_inbox") else "verify"),
        "sources_json": json.dumps(sources) if sources else None,
        "generated_at": p.get("generated_at") or time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    cols = ",".join(row.keys())
    ph = ",".join("?" for _ in row)
    conn.execute(f"INSERT OR REPLACE INTO contacts ({cols}) VALUES ({ph})", list(row.values()))
    conn.commit()
    conn.close()
    print(f"[contacts] {row['nse_symbol']} — primary={row['primary_email']} "
          f"({row['primary_email_kind']}) ir_head={row['ir_head_name']} "
          f"cs={row['cs_name']} cfo={row['cfo_name']} conf={row['contact_confidence']}")


if __name__ == "__main__":
    main()
