"""
12_batch_ingest.py
-------------------
Scan ~/as-outputs for M&A-readiness gensearch results, match each to a
T1 ticker by the company name in the prompt, parse + ingest into the
research table. Idempotent (INSERT OR REPLACE). No grep, no shell globs.

Usage: python3 12_batch_ingest.py
Reads the ticker->(as_id, name-substring) map below.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
OUT = HOME / "as-outputs"
SCRIPTS = Path(__file__).resolve().parent

# ticker: (as_company_id, name substring to match in the prompt)
T1 = {
    "GLENMARK": ("TK61665", "Glenmark"),
    "BIOCON": ("TK226997", "Biocon"),
    "DRREDDY": ("TK112871", "Dr Reddy"),
    "INFY": ("TK179981", "Infosys"),
    "MARICO": ("TK448632", "Marico"),
    "ASIANPAINT": ("TK523533", "Asian Paints"),
    "TCS": ("TK242393", "Tata Consultancy"),
    "BRITANNIA": ("TK523774", "Britannia"),
    "HYUNDAI": ("TK971018", "Hyundai"),
    "TATACONSUM": ("TK536231", "Tata Consumer"),
    "HINDUNILVR": ("TK532742", "Hindustan Unilever"),
    "CRISIL": ("TK219296", "CRISIL"),
    "LT": ("TK758735", "Larsen"),
    "SUNPHARMA": ("TK290076", "Sun Pharm"),
    "ITC": ("TK716833", "ITC Ltd"),
    "PAYTM": ("TK534185", "One97"),
    "MOTHERSON": ("TK240411", "Motherson"),
    "PIDILITIND": ("TK207274", "Pidilite"),
    "NESTLEIND": ("TK758734", "Nestle India"),
    "M&M": ("TK527972", "Mahindra"),
    "HEROMOTOCO": ("TK758669", "Hero MotoCorp"),
    "CUMMINSIND": ("TK719426", "Cummins"),
    "LODHA": ("TK522435", "Lodha"),
    "MAZDOCK": ("TK860487", "Mazagon"),
    "POWERINDIA": ("TK814499", "Hitachi"),
    "BAJAJ-AUTO": ("TK380146", "Bajaj Auto"),
    "PTC": ("TK226817", "PTC India"),
    # --- T2 (38) ---
    "TANLA": ("TK359503", "Tanla"),
    "GESHIP": ("TK527318", "Great Eastern Shipping"),
    "HONAUT": ("TK749707", "Honeywell Automation India"),
    "NCC": ("TK170777", "NCC Ltd"),
    "SKFINDIA": ("TK717583", "SKF India"),
    "NAVA": ("TK175974", "Nava Ltd"),
    "REDINGTON": ("TK360796", "Redington"),
    "WABAG": ("TK525530", "VA Tech Wabag"),
    "TATAELXSI": ("TK30833", "Tata Elxsi"),
    "NBCC": ("TK586954", "NBCC"),
    "SUPREMEIND": ("TK163664", "Supreme Industries"),
    "ASTRAL": ("TK371945", "Astral Ltd"),
    "AHLUCONT": ("TK463412", "Ahluwalia"),
    "SONATSOFTW": ("TK24790", "Sonata Software"),
    "AWL": ("TK903551", "AWL Agri"),
    "BATAINDIA": ("TK188863", "Bata India"),
    "CASTROLIND": ("TK716807", "Castrol India"),
    "GUJGASLTD": ("__GUJGAS__", "Gujarat Gas"),
    "JUBLPHARMA": ("TK534819", "Jubilant Pharmova"),
    "JPPOWER": ("TK286381", "Jaiprakash Power"),
    "SCHAEFFLER": ("TK38403", "Schaeffler India"),
    "HEXT": ("TK584419", "Hexaware"),
    "PAGEIND": ("TK368328", "Page Industries"),
    "KPITTECH": ("TK797174", "KPIT"),
    "AEGISLOG": ("TK111643", "Aegis Logistics"),
    "MARKSANS": ("TK430537", "Marksans"),
    "FIEMIND": ("TK345033", "Fiem Industries"),
    "3MINDIA": ("TK180405", "3M India"),
    "CDSL": ("TK612370", "Central Depository"),
    "SHAKTIPUMP": ("TK163568", "Shakti Pumps"),
    "AFFLE": ("TK826583", "Affle"),
    "CAMS": ("TK314081", "Computer Age Management"),
    "PINELABS": ("7df177d9d2e1c6ce577af1d0fdb702aa", "Pine Labs"),
    "COFORGE": ("TK240248", "Coforge"),
    "PERSISTENT": ("TK505816", "Persistent Systems"),
    "CARERATING": ("TK610634", "CARE Ratings"),
    "MCX": ("TK581801", "Multi Commodity Exchange"),
}

# --- T3 (57): high-ARS names ranked top-150 by ARS but tier-scoped out of T1/T2 ---
T3 = {
    "ROUTE": ("TK859140", "Route Mobile"),
    "IRCON": ("TK511642", "IRCON"),
    "MASTEK": ("TK181214", "Mastek"),
    "MSTCLTD": ("TK814762", "MSTC"),
    "PNCINFRA": ("TK686337", "PNC Infratech"),
    "LTTS": ("TK726316", "L&T Technology"),
    "RVNL": ("TK815624", "Rail Vikas"),
    "IRB": ("TK419568", "IRB Infrastructure Developers"),
    "CMSINFO": ("TK900357", "CMS Info"),
    "DATAMATICS": ("TK230891", "Datamatics"),
    "DEEPAKFERT": ("TK525586", "Deepak Fertilisers"),
    "SYNGENE": ("TK693860", "Syngene"),
    "SUNTV": ("TK323372", "Sun TV"),
    "KRBL": ("TK76611", "KRBL"),
    "GRANULES": ("TK413657", "Granules"),
    "MOIL": ("TK534042", "MOIL"),
    "ADVENZYMES": ("TK722599", "Advanced Enzyme"),
    "TIMKEN": ("TK62113", "Timken India"),
    "BAJAJELEC": ("TK111651", "Bajaj Electricals"),
    "LTM": ("TK721859", "LTIMindtree"),
    "WELSPUNLIV": ("TK46746", "Welspun Living"),
    "IGL": ("TK215914", "Indraprastha Gas"),
    "MPHASIS": ("TK216344", "Mphasis"),
    "MGL": ("TK720513", "Mahanagar Gas"),
    "CLEAN": ("TK884461", "Clean Science"),
    "PARADEEP": ("TK914583", "Paradeep Phosphates"),
    "CONCOR": ("TK454567", "Container Corporation"),
    "SAREGAMA": ("TK97866", "Saregama"),
    "ASAHIINDIA": ("TK758709", "Asahi India Glass"),
    "LALPATHLAB": ("TK705385", "Lal PathLabs"),
    "SIEMENS": ("TK758733", "Siemens"),
    "MANYAVAR": ("TK904309", "Vedant Fashions"),
    "EXIDEIND": ("TK37230", "Exide Industries"),
    "IONEXCHANG": ("TK169230", "Ion Exchange"),
    "HAPPSTMNDS": ("TK858987", "Happiest Minds"),
    "JAMNAAUTO": ("TK731782", "Jamna Auto"),
    "DABUR": ("TK205426", "Dabur"),
    "KPIL": ("TK329894", "Kalpataru Projects"),
    "ALIVUS": ("TK886326", "Alivus"),
    "WELENT": ("TK258433", "Welspun Enterprises"),
    "ATUL": ("TK507681", "Atul Ltd"),
    "AFCONS": ("TK971951", "Afcons"),
    "KSCL": ("TK395526", "Kaveri Seed"),
    "ATGL": ("TK781726", "Adani Total Gas"),
    "HINDALCO": ("TK758875", "Hindalco"),
    "BDL": ("TK785639", "Bharat Dynamics"),
    "CELLO": ("TK947283", "Cello World"),
    "RAYMONDLSL": ("0ac89653e0594caca853e80f2474372a", "Raymond Lifestyle"),
    "OIL": ("TK486834", "Oil India"),
    "KEC": ("TK316263", "KEC International"),
    "TBOTEK": ("TK901547", "TBO Tek"),
    "KITEX": ("TK339291", "Kitex"),
    "CERA": ("TK134705", "Cera Sanitaryware"),
    "GILLETTE": ("TK758671", "Gillette India"),
    "ECLERX": ("TK410943", "eClerx"),
    "PRAJIND": ("TK222005", "Praj Industries"),
    "BSOFT": ("TK58615", "Birlasoft"),
}

# --- T3 Run-3 (52): the 40-50 ARS band, taking T3 coverage down to ARS>=40 ---
T3_RUN3 = {
    "ELECTCAST": ("TK188877", "Electrosteel Castings"),
    "GODREJCP": ("TK109414", "Godrej Consumer"),
    "PCBL": ("TK545844", "PCBL"),
    "NTPC": ("TK183249", "NTPC Ltd"),
    "MAHSEAMLES": ("TK180049", "Maharashtra Seamless"),
    "UBL": ("TK168412", "United Breweries Ltd"),
    "ARE&M": ("__WEB__", "Amara Raja"),
    "BERGEPAINT": ("TK111661", "Berger Paints"),
    "NLCINDIA": ("TK331927", "NLC India"),
    "DYNAMATECH": ("TK180975", "Dynamatic"),
    "RATNAMANI": ("__WEB__", "Ratnamani"),
    "GOKEX": ("TK285319", "Gokaldas"),
    "GMDCLTD": ("__WEB__", "Gujarat Mineral Development"),
    "APOLLOTYRE": ("TK716154", "Apollo Tyres"),
    "BEML": ("__WEB__", "BEML"),
    "SHREECEM": ("TK731796", "Shree Cement"),
    "USHAMART": ("TK717596", "Usha Martin Ltd"),
    "BBTC": ("__WEB__", "Bombay Burmah"),
    "KANSAINER": ("TK111738", "Kansai Nerolac"),
    "PETRONET": ("TK226811", "Petronet LNG"),
    "TEGA": ("TK898322", "Tega Industries"),
    "AMBUJACEM": ("TK716830", "Ambuja Cements"),
    "DALBHARAT": ("TK714602", "Dalmia Bharat Ltd"),
    "PGIL": ("TK361616", "Pearl Global"),
    "PFIZER": ("__WEB__", "Pfizer"),
    "EPL": ("__WEB__", "EPL Ltd"),
    "APLLTD": ("TK516939", "Alembic Pharmaceuticals"),
    "CIPLA": ("TK167945", "Cipla Ltd"),
    "HAVELLS": ("TK216503", "Havells"),
    "COLPAL": ("TK524664", "Colgate"),
    "GODREJAGRO": ("TK768519", "Godrej Agrovet"),
    "MSUMI": ("TK865684", "Motherson Sumi Wiring"),
    "AURIONPRO": ("TK303535", "Aurionpro"),
    "KIRLOSBROS": ("TK111813", "Kirloskar Brothers"),
    "TORNTPOWER": ("TK344526", "Torrent Power"),
    "PIIND": ("TK277334", "PI Industries"),
    "CAMPUS": ("TK913861", "Campus Activewear"),
    "ELECON": ("TK112868", "Elecon Engineering"),
    "BALKRISIND": ("TK127419", "Balkrishna Industries"),
    "ZENSARTECH": ("TK331522", "Zensar"),
    "HERITGFOOD": ("TK343169", "Heritage Foods Ltd"),
    "ARVIND": ("__WEB__", "Arvind Ltd"),
    "BLUEJET": ("TK946589", "Blue Jet Healthcare"),
    "ALKEM": ("TK705381", "Alkem Laboratories"),
    "ASHOKA": ("TK522431", "Ashoka Buildcon"),
    "RAILTEL": ("TK870611", "RailTel"),
    "GAIL": ("TK586809", "GAIL"),
    "OFSS": ("TK156252", "Oracle Financial Services"),
    "CCAVENUE": ("__WEB__", "Avenues"),
    "JINDALSAW": ("TK112505", "Jindal Saw Ltd"),
    "FINCABLES": ("TK716823", "Finolex Cables"),
    "HINDZINC": ("TK168922", "Hindustan Zinc"),
}


def company_in_prompt(path):
    try:
        d = json.loads(path.read_text())
    except Exception:
        return None
    prompt = (d.get("input") or {}).get("prompt", "")
    m = re.search(r"profile for ([^(]+)\(", prompt)
    return m.group(1).strip() if m else None


def main():
    # newest first so re-runs pick the latest result per company
    files = sorted(OUT.glob("*M_A-readiness*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    done = set()
    universe = {**T1, **T3, **T3_RUN3}
    for tkr, (cid, sub) in universe.items():
        if tkr in done:
            continue
        match = None
        for f in files:
            co = company_in_prompt(f) or ""
            if sub.lower() in co.lower():
                match = f
                break
        if not match:
            print(f"{tkr}: no file yet")
            continue
        payload = HOME / "tmp" / "payloads" / f"{tkr}.json"
        payload.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(SCRIPTS / "11_parse_as_output.py"),
                        str(match), tkr, cid, "--out", str(payload)],
                       capture_output=True)
        r = subprocess.run([sys.executable, str(SCRIPTS / "10_ingest_research.py"),
                            str(payload)], capture_output=True, text=True)
        print(r.stdout.strip() or f"{tkr}: ingest produced no output")
        done.add(tkr)


if __name__ == "__main__":
    main()
