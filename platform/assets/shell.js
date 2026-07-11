/* Shared workspace shell: loads the canonical spine and renders the
   sidebar nav + top account bar. Every page calls Shell.mount(active).
   Static, no backend - the spine JSON is the single source of truth. */
const Shell = (() => {
  const MODULES = [
    { id: "home",        href: "index.html",       ix: "⌂", label: "Account Home", grp: "Workspace" },
    { id: "learning",    href: "learning.html",    ix: "M1", label: "Learning Journey", grp: "Capability build" },
    { id: "ideas",       href: "ideas.html",       ix: "M2", label: "Ideas Funnel",     grp: "Capability build" },
    { id: "exchange",    href: "exchange.html",    ix: "M3", label: "Patent Exchange",  grp: "Capability build" },
    { id: "targets",     href: "targets.html",     ix: "M4", label: "Target Sourcing",  grp: "Transaction" },
    { id: "integration", href: "integration.html", ix: "M5", label: "Deal Integration", grp: "Transaction" }
  ];

  let _spine = null;
  async function spine() {
    if (_spine) return _spine;
    _spine = await fetch("data/spine.json").then(r => r.json());
    return _spine;
  }

  // M4 live public-data capability screen (real AlphaSense-sourced comparables)
  let _targets = null;
  async function targets() {
    if (_targets) return _targets;
    _targets = await fetch("data/targets.json").then(r => r.json());
    return _targets;
  }

  function nav(active) {
    let html = "", lastGrp = "";
    for (const m of MODULES) {
      if (m.grp !== lastGrp) { html += `<div class="grp">${m.grp}</div>`; lastGrp = m.grp; }
      html += `<a href="${m.href}" class="${m.id === active ? "active" : ""}">
        <span class="ix">${m.ix}</span><span>${m.label}</span></a>`;
    }
    return html;
  }

  async function mount(active) {
    const s = await spine();
    const a = s.account;
    document.body.classList.add("app-body");
    const app = document.createElement("div");
    app.className = "app";
    app.innerHTML = `
      <aside class="sidebar">
        <div class="brand">
          <div class="mark">M<span class="amp">&amp;</span>A Leadership</div>
          <div class="sub">Capability Workspace</div>
        </div>
        <nav class="nav">${nav(active)}</nav>
        <div class="foot">${a.company}<br>${a.cohort}</div>
      </aside>
      <div class="main">
        <div class="topbar">
          <div class="acct">
            <span class="co">${a.company}</span>
            <span class="pill">Year ${a.programYear} of ${a.programSpan}</span>
          </div>
          <div class="yr">${a.sector} &middot; ${a.cohort}</div>
        </div>
        <div class="content" id="content"></div>
      </div>`;
    // move existing body children into #content
    const staged = Array.from(document.body.children);
    document.body.insertBefore(app, document.body.firstChild);
    const content = app.querySelector("#content");
    for (const el of staged) if (el !== app) content.appendChild(el);
    return s;
  }

  // small helpers
  const chipClass = st => ({ passed:"done", done:"done", completed:"done", active:"active", in_progress:"active" }[st] || "pending");
  const chip = (txt, st) => `<span class="chip ${chipClass(st)}">${txt}</span>`;

  return { mount, spine, targets, chip, chipClass, MODULES };
})();
