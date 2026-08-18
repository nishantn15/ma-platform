/* Shared workspace shell: loads the canonical spine and renders the
   sidebar nav + top account bar. Every page calls Shell.mount(active).
   Static, no backend - the spine JSON is the single source of truth. */
const Shell = (() => {
  /* Nav layout only. The LABELS are not here - they come from spine.vocabulary,
     which is canonical against TK's customers deck. M1-M5 survive as the nav
     index (internal shorthand) and never as the name of a thing.
     Group order is the information architecture: the two intake engines feed
     the Pathway Matrix, and the execution modules hang off it. */
  const LAYOUT = [
    { id: "home",        href: "index.html",       ix: "⌂",  grp: "Workspace",         fallback: "Account Home" },
    { id: "charter",     href: "charter.html",     ix: "EGC", grp: "Capability journey" },
    { id: "learning",    href: "learning.html",    ix: "M1", grp: "Capability journey" },
    { id: "ideas",       href: "ideas.html",       ix: "M2", grp: "Intake engines" },
    { id: "exchange",    href: "exchange.html",    ix: "M3", grp: "Intake engines" },
    { id: "pathway",     href: "pathway.html",     ix: "◈",  grp: "The decision" },
    { id: "targets",     href: "targets.html",     ix: "M4", grp: "Execution routes" },
    { id: "integration", href: "integration.html", ix: "M5", grp: "Execution routes" }
  ];

  // resolved once the spine loads; MODULES stays a live view for callers
  const MODULES = LAYOUT.map(m => ({ ...m, label: m.fallback || m.id }));
  function applyVocabulary(vocab) {
    if (!vocab || !vocab.modules) return;
    const byId = Object.fromEntries(vocab.modules.map(m => [m.id, m]));
    for (const m of MODULES) {
      const v = byId[m.id];
      if (v) { m.label = v.name; m.code = v.code; m.role = v.role; }
    }
  }
  const nameOf = id => (MODULES.find(m => m.id === id) || {}).label || id;

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

  /* The causal thread, stated once. Injected by mount() so the pipeline order
     can never drift from page to page - and so it reads as a pipeline through
     the matrix rather than five parallel modules. */
  const THREAD = [
    { ids: ["charter"],           txt: "EGC charter opens" },
    { ids: ["learning"],          txt: "M1 names the gap" },
    { ids: ["ideas", "exchange"], txt: "M2 / M3 intake" },
    { ids: ["pathway"],           txt: "◈ pathway matrix" },
    { ids: ["targets"],           txt: "M4 target" },
    { ids: ["integration"],       txt: "M5 integration" }
  ];
  function crumb(active) {
    const body = THREAD
      .map(s => (s.ids.includes(active) ? `<b>${s.txt}</b>` : s.txt))
      .join(" &rarr; ");
    return `<div class="crumb">CAUSAL THREAD &nbsp;${body}</div>`;
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
    applyVocabulary(s.vocabulary);
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
    if (active !== "home") content.insertAdjacentHTML("afterbegin", crumb(active));
    return s;
  }

  // small helpers
  const chipClass = st => ({ passed:"done", done:"done", completed:"done", active:"active", in_progress:"active" }[st] || "pending");
  const chip = (txt, st) => `<span class="chip ${chipClass(st)}">${txt}</span>`;

  return { mount, spine, targets, chip, chipClass, crumb, nameOf, MODULES };
})();
