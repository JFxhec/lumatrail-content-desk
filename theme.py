"""Visual layer of the content desk: "field notebook" art direction in the product's own colours, teal and sand."""

from html import escape

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

:root {
  --paper: #F4EEE3; --card: #FFFDF8; --sand: #E6D9C2; --sand-deep: #CDBB9B; --line: #DCCFB8;
  --ink: #1F2A2C; --muted: #5E6B66;
  --teal: #0F6E6A; --teal-deep: #0B4F4C; --teal-soft: #D7ECE8;
  --ochre: #8A5A0B; --ochre-soft: #F6E7C8; --rust: #9B3B26; --rust-soft: #F6DDD5;
  --serif: 'Fraunces', Georgia, serif; --sans: 'Inter', system-ui, sans-serif; --mono: 'JetBrains Mono', monospace;
}
.stApp, .stMarkdown, p, li, label, input, textarea { font-family: var(--sans); }
[data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded' !important; }
h1, h2, h3, h4 { font-family: var(--serif) !important; color: var(--ink); letter-spacing: -0.01em; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 1.2rem; max-width: 1280px; }

/* sidebar: the trail map pocket */
[data-testid="stSidebar"] { background: var(--sand); border-right: 1px solid var(--sand-deep); }
[data-testid="stSidebar"] h2 { font-size: 1.35rem; }
.side-note { font-size: .82rem; color: var(--muted); line-height: 1.45; margin-top: .4rem; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: .25rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { font-weight: 500; color: var(--muted); padding: .55rem .9rem; border-radius: 8px 8px 0 0; }
.stTabs [aria-selected="true"] { color: var(--teal-deep); background: var(--card); }
.stTabs [data-baseweb="tab-highlight"] { background: var(--teal); }

/* buttons */
.stButton button, .stFormSubmitButton button { border-radius: 999px; font-weight: 600; padding: .45rem 1.2rem;
  transition: transform .15s ease, box-shadow .15s ease; }
.stButton button:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(15,110,106,.18); }
.stButton button[kind="primary"], .stFormSubmitButton button { background: var(--teal); border-color: var(--teal); color: #fff; }
.stButton button[kind="primary"]:hover:not(:disabled) { background: var(--teal-deep); border-color: var(--teal-deep); }
.stButton button[kind="secondary"] { background: var(--card); border-color: var(--sand-deep); color: var(--ink); }

/* inputs */
.stTextArea textarea, .stTextInput input { background: var(--card); border-radius: 10px; }
[data-testid="stExpander"] { background: var(--card); border: 1px solid var(--line); border-radius: 12px; }

/* hero */
.hero { position: relative; overflow: hidden; border-radius: 18px; padding: 1.6rem 2rem;
  background: linear-gradient(120deg, var(--teal-deep) 0%, var(--teal) 70%, #2C8A80 100%); color: #F4EEE3; margin-bottom: 1.1rem; }
.hero svg.topo { position: absolute; inset: 0; width: 100%; height: 100%; opacity: .16; }
.hero-row { position: relative; display: flex; align-items: center; gap: 1.2rem; }
.hero-kicker { font-family: var(--mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--sand); }
.hero-title { font-family: var(--serif); font-size: 2.1rem; font-weight: 600; line-height: 1.1; margin: .15rem 0 .35rem; color: #FFFDF8; }
.hero-sub { font-size: .95rem; max-width: 640px; color: #E8E0D0; line-height: 1.5; }
.hero-stats { margin-left: auto; display: flex; gap: .6rem; }
.hero-stat { background: rgba(255,253,248,.1); border: 1px solid rgba(244,238,227,.25); border-radius: 12px; padding: .55rem .8rem; text-align: center; min-width: 104px; }
.hero-stat b { display: block; font-family: var(--serif); font-size: 1.3rem; color: #FFFDF8; }
.hero-stat span { font-size: .72rem; color: var(--sand); }

/* workflow trail */
.trail { display: flex; align-items: center; gap: .4rem; margin: .2rem 0 1rem; flex-wrap: wrap; }
.step { display: flex; align-items: center; gap: .5rem; padding: .4rem .8rem; border-radius: 999px; font-size: .85rem;
  background: var(--card); border: 1px solid var(--line); color: var(--muted); }
.step i { font-style: normal; font-family: var(--mono); font-size: .72rem; width: 1.35rem; height: 1.35rem; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center; background: var(--sand); color: var(--ink); }
.step.done { color: var(--teal-deep); border-color: #A9D3CC; }
.step.done i { background: var(--teal); color: #fff; }
.step.now { color: var(--ink); border-color: var(--teal); box-shadow: 0 0 0 3px var(--teal-soft); font-weight: 600; }
.step.now i { background: var(--ink); color: #fff; }
.step.wait { color: var(--ochre); border-color: #E3C68C; background: var(--ochre-soft); font-weight: 600; }
.step.wait i { background: var(--ochre); color: #fff; }
.trail-dash { flex: 0 0 18px; border-top: 2px dashed var(--sand-deep); }

/* cards */
.card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.15rem; margin-bottom: .9rem; }
.label { font-family: var(--mono); font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: .45rem; }
.status { border-radius: 14px; padding: .9rem 1.15rem; margin-bottom: 1rem; border: 1px solid; display: flex; gap: .9rem; align-items: flex-start; }
.status svg { flex: 0 0 22px; margin-top: 2px; }
.status h4 { margin: 0 0 .2rem; font-size: 1.1rem; }
.status p, .status li { margin: 0; font-size: .9rem; line-height: 1.45; }
.status ul { margin: .35rem 0 0 1rem; padding: 0; }
.status.ready { background: var(--teal-soft); border-color: #A9D3CC; color: var(--teal-deep); }
.status.ready h4 { color: var(--teal-deep); }
.status.clarify { background: var(--ochre-soft); border-color: #E3C68C; color: #5F3E06; }
.status.clarify h4 { color: #5F3E06; }
.status.attention { background: var(--rust-soft); border-color: #E5B3A5; color: #6E2817; }
.status.attention h4 { color: #6E2817; }

/* previews */
.mail { background: var(--card); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; margin-bottom: .9rem; }
.mail-head { padding: .75rem 1.1rem; border-bottom: 1px solid var(--line); background: #FBF7EF; }
.mail-from { font-size: .78rem; color: var(--muted); }
.mail-subject { font-family: var(--serif); font-size: 1.15rem; font-weight: 600; color: var(--ink); margin-top: .15rem; }
.mail-body { padding: 1rem 1.1rem; font-size: .93rem; line-height: 1.65; color: var(--ink); }
.social { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1.1rem; margin-bottom: .9rem; }
.social-head { display: flex; align-items: center; gap: .6rem; margin-bottom: .55rem; }
.avatar { width: 34px; height: 34px; border-radius: 50%; background: var(--teal); display: flex; align-items: center; justify-content: center; }
.social-name { font-weight: 600; font-size: .9rem; }
.social-handle { font-size: .78rem; color: var(--muted); }
.social-body { font-size: .93rem; line-height: 1.6; }
mark.claim { background: linear-gradient(transparent 55%, #CDE7E2 55%); color: inherit; padding: 0 1px; }
mark.claim.bad { background: linear-gradient(transparent 55%, #F2C4B6 55%); }
mark.claim sup, .fid { font-family: var(--mono); font-size: .62rem; font-weight: 500; color: #fff; background: var(--teal);
  border-radius: 4px; padding: 1px 4px; margin-left: 2px; vertical-align: super; }
mark.claim.bad sup { background: var(--rust); }
.fid { vertical-align: baseline; font-size: .7rem; padding: 2px 6px; margin: 0 2px 0 0; display: inline-block; }
.meta { font-size: .78rem; color: var(--muted); margin-top: .3rem; }

/* lists */
.row { display: flex; gap: .7rem; align-items: flex-start; padding: .6rem 0; border-top: 1px dashed var(--line); }
.row:first-of-type { border-top: none; padding-top: .1rem; }
.row-main { flex: 1; font-size: .9rem; line-height: 1.45; }
.row-why { font-size: .8rem; color: var(--muted); margin-top: .15rem; }
.pill { font-family: var(--mono); font-size: .66rem; letter-spacing: .06em; text-transform: uppercase; border-radius: 999px;
  padding: 3px 9px; white-space: nowrap; border: 1px solid; }
.pill.used, .pill.supported, .pill.pass { color: var(--teal-deep); background: var(--teal-soft); border-color: #A9D3CC; }
.pill.qualified { color: #5F3E06; background: var(--ochre-soft); border-color: #E3C68C; }
.pill.omitted, .pill.unsupported, .pill.fail { color: #6E2817; background: var(--rust-soft); border-color: #E5B3A5; }
.checks { display: flex; flex-wrap: wrap; gap: .4rem; }
.chk { display: inline-flex; align-items: center; gap: .35rem; font-size: .78rem; padding: 4px 10px; border-radius: 999px;
  border: 1px solid #A9D3CC; background: var(--teal-soft); color: var(--teal-deep); }
.chk.bad { border-color: #E5B3A5; background: var(--rust-soft); color: #6E2817; font-weight: 600; }

/* facts */
.fact { display: flex; gap: .9rem; align-items: flex-start; }
.marker { flex: 0 0 auto; font-family: var(--mono); font-size: .85rem; color: #fff; background: var(--teal);
  border-radius: 8px; padding: .35rem .55rem; box-shadow: inset 0 -3px 0 rgba(0,0,0,.15); }
.fact-text { font-size: .93rem; line-height: 1.5; }

/* metrics */
.metric { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem; height: 100%; }
.metric b { font-family: var(--serif); font-size: 1.7rem; font-weight: 600; color: var(--ink); display: block; line-height: 1.15; }
.metric .vs { font-size: .82rem; color: var(--muted); }
.metric .vs em { font-style: normal; color: var(--teal-deep); font-weight: 600; }
@media (prefers-reduced-motion: reduce) { .stButton button { transition: none; } }
</style>
"""

TOPO = """<svg class="topo" viewBox="0 0 800 200" preserveAspectRatio="none" aria-hidden="true">
<g fill="none" stroke="#F4EEE3" stroke-width="1.2">
<path d="M-20 150 C 120 90, 220 190, 360 120 S 600 60, 820 130"/>
<path d="M-20 170 C 130 115, 230 205, 370 142 S 610 85, 820 152"/>
<path d="M-20 190 C 140 140, 240 220, 380 165 S 620 110, 820 175"/>
<path d="M-20 60 C 90 20, 200 100, 330 50 S 560 -10, 820 40"/>
<path d="M-20 85 C 100 45, 210 125, 340 75 S 570 18, 820 65"/>
<path d="M520 200 C 560 160, 640 150, 700 170 S 790 210, 820 190"/>
<ellipse cx="640" cy="95" rx="70" ry="26"/><ellipse cx="640" cy="95" rx="42" ry="14"/><ellipse cx="640" cy="95" rx="16" ry="5"/>
</g></svg>"""

BOTTLE = """<svg width="44" height="78" viewBox="0 0 44 78" aria-hidden="true">
<rect x="14" y="2" width="16" height="9" rx="3" fill="#E6D9C2"/>
<rect x="16" y="11" width="12" height="5" fill="#CDBB9B"/>
<path d="M12 16 h20 a6 6 0 0 1 6 6 v48 a6 6 0 0 1 -6 6 h-20 a6 6 0 0 1 -6 -6 v-48 a6 6 0 0 1 6 -6z" fill="#FFFDF8" opacity=".95"/>
<rect x="6" y="38" width="32" height="14" fill="#E6D9C2"/>
<path d="M9 45 q6 -5 13 0 t13 0" fill="none" stroke="#0F6E6A" stroke-width="1.6"/>
</svg>"""

ICONS = {
    "ready": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>',
    "clarify": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>',
    "attention": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>',
}
CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="m5 12 5 5 9-10"/></svg>'
CROSS = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
LEAF = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFDF8" stroke-width="2" aria-hidden="true"><path d="M5 19c8 0 14-6 14-15C10 4 5 9 5 15v4z"/><path d="M5 19 14 10"/></svg>'


def hero(n_facts: int, n_tests: int) -> str:
    return f"""<div class="hero">{TOPO}<div class="hero-row">{BOTTLE}
<div><div class="hero-kicker">LumaTrail · Everyday Bottle · content desk</div>
<div class="hero-title">On brief, on the facts.</div>
<div class="hero-sub">Turn a campaign brief into an email and a social post. Every product claim is traced to an approved
fact, every refused request is recorded, and nothing leaves without a reviewer's approval.</div></div>
<div class="hero-stats"><div class="hero-stat"><b>{n_facts}</b><span>approved facts</span></div>
<div class="hero-stat"><b>2</b><span>channels</span></div><div class="hero-stat"><b>{n_tests}</b><span>test briefs</span></div></div>
</div></div>"""


def trail(stage: str) -> str:
    """Workflow strip. stage: idle | clarify | review."""
    names = ["Brief", "Draft + triage", "Fact & rule checks", "Your review"]
    states = {"idle": ["now", "", "", ""], "clarify": ["done", "wait", "", ""],
              "review": ["done", "done", "done", "now"]}[stage]
    parts = []
    for i, (name, state) in enumerate(zip(names, states)):
        if i:
            parts.append('<span class="trail-dash"></span>')
        parts.append(f'<span class="step {state}"><i>{i + 1}</i>{name}</span>')
    return f'<div class="trail">{"".join(parts)}</div>'


def status(kind: str, title: str, text: str, items: list[str] = ()) -> str:
    lis = "".join(f"<li>{escape(i)}</li>" for i in items)
    return (f'<div class="status {kind}">{ICONS[kind]}<div><h4>{escape(title)}</h4><p>{escape(text)}</p>'
            f'{f"<ul>{lis}</ul>" if lis else ""}</div></div>')


def highlight(text: str, claims: list[dict]) -> str:
    """Escape text and underline each claim found in it, with its fact IDs as markers."""
    spans = []
    for c in sorted(claims, key=lambda c: -len(c.get("text", ""))):
        t = c.get("text", "").strip()
        start = text.find(t) if t else -1
        if start == -1 or any(s < start + len(t) and start < e for s, e, _ in spans):
            continue
        spans.append((start, start + len(t), c))
    out, pos = [], 0
    for s, e, c in sorted(spans, key=lambda x: x[0]):
        bad = " bad" if c.get("verdict") == "unsupported" else ""
        ids = "".join(f"<sup>{escape(i)}</sup>" for i in c.get("fact_ids") or ["?"])
        out += [escape(text[pos:s]), f'<mark class="claim{bad}" title="{escape(c.get("comment", ""))}">{escape(text[s:e])}{ids}</mark>']
        pos = e
    out.append(escape(text[pos:]))
    return "".join(out).replace("\n", "<br>")


def email_preview(subject: str, body: str, claims: list[dict], meta: str = "") -> str:
    return f"""<div class="mail"><div class="mail-head"><div class="mail-from">From LumaTrail &lt;hello@lumatrail.example&gt;</div>
<div class="mail-subject">{highlight(subject, claims)}</div></div><div class="mail-body">{highlight(body, claims)}</div></div>
{f'<div class="meta">{escape(meta)}</div>' if meta else ''}"""


def social_preview(text: str, claims: list[dict]) -> str:
    return f"""<div class="social"><div class="social-head"><div class="avatar">{LEAF}</div>
<div><div class="social-name">LumaTrail</div><div class="social-handle">@lumatrail</div></div></div>
<div class="social-body">{highlight(text, claims)}</div></div>"""


def checks(items: list[dict]) -> str:
    chips = "".join(
        f'<span class="chk{"" if c["passed"] else " bad"}" title="{escape(c["detail"])}">{CHECK if c["passed"] else CROSS}'
        f'{escape(c["check"])}{(" · " + escape(c["detail"])) if c["detail"] and (not c["passed"] or "≤" in c["check"]) else ""}</span>'
        for c in items)
    return f'<div class="checks">{chips}</div>'


def fact_ids(ids) -> str:
    return "".join(f'<span class="fid">{escape(i)}</span>' for i in ids or [])


def requests(items: list[dict]) -> str:
    if not items:
        return '<div class="row-why">No specific content request in the brief.</div>'
    rows = "".join(
        f'<div class="row"><span class="pill {escape(r.get("decision", ""))}">{escape(r.get("decision", ""))}</span>'
        f'<div class="row-main">{escape(r.get("request", ""))} {fact_ids(r.get("fact_ids"))}'
        f'<div class="row-why">{escape(r.get("reason", ""))}</div></div></div>' for r in items)
    return rows


def claims(items: list[dict]) -> str:
    if not items:
        return '<div class="row-why">No factual claim found.</div>'
    return "".join(
        f'<div class="row"><span class="pill {escape(c.get("verdict", ""))}">{escape(c.get("verdict", ""))}</span>'
        f'<div class="row-main">“{escape(c.get("text", ""))}” {fact_ids(c.get("fact_ids"))}'
        f'<div class="row-why">{escape(c.get("channel", ""))} · {escape(c.get("comment", ""))}</div></div></div>'
        for c in items)


def card(label: str, inner: str) -> str:
    return f'<div class="card"><div class="label">{escape(label)}</div>{inner}</div>'


def fact_card(f: dict) -> str:
    return f'<div class="card fact"><span class="marker">{escape(f["id"])}</span><div class="fact-text">{escape(f["fact"])}</div></div>'


def metric(label: str, value: str, vs: str) -> str:
    return f'<div class="metric"><div class="label">{escape(label)}</div><b>{value}</b><div class="vs">{vs}</div></div>'
