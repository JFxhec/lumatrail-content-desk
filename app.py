"""LumaTrail content desk: brief -> checked draft -> human review. Run with `streamlit run app.py`."""

import json
import os
import time
from datetime import datetime
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

import theme as ui
from llm import find_claude
from pipeline import BRAND_RULES, DATA, FACTS, rule_checks, run_baseline, run_prototype, totals

OUT = Path(__file__).parent / "outputs"
LOG = OUT / "review_log.jsonl"
CASES = json.loads((DATA / "test_cases.json").read_text())
LANGUAGES = {"English": "en", "French": "fr", "German": "de", "Spanish": "es"}
RESULTS = OUT / "test_results.json"
RECORDED = {r["id"]: r for r in json.loads(RESULTS.read_text())["results"]} if RESULTS.exists() else {}


def live_available() -> bool:
    """Live mode needs the Claude Code CLI; without it (e.g. Streamlit Cloud) the app replays recorded test runs."""
    if os.environ.get("LUMA_MODE") == "replay":
        return False
    try:
        find_claude()
        return True
    except RuntimeError:
        return False


LIVE = live_available()

st.set_page_config(page_title="LumaTrail content desk", layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)


def html(s: str):
    st.markdown(s, unsafe_allow_html=True)


def split_claims(claims):
    return ([c for c in claims if c.get("channel") in ("subject", "email")],
            [c for c in claims if c.get("channel") == "social"])


def show(result, brief, baseline=None):
    d = result["draft"]
    st.session_state.update(result=result, brief_used=brief, shown_at=time.time(), baseline=baseline,
                            ed_subject=d.get("email_subject", ""), ed_body=d.get("email_body", ""),
                            ed_social=d.get("social_post", ""))


def generate(brief, model, with_baseline):
    with st.spinner("Drafting, checking facts and format, revising if needed…"):
        result = run_prototype(brief, model)
    baseline = None
    if with_baseline:
        with st.spinner("Running the single-prompt baseline…"):
            baseline = run_baseline(brief, model)
    show(result, brief, baseline)


# ---------- sidebar: the brief ----------
with st.sidebar:
    st.header("Campaign brief")
    if LIVE:
        options = ["Write my own brief"] + [f"{c['id']} · {c['brief']}" for c in CASES]
        choice = st.selectbox("Start from", options)
        default = "" if choice == options[0] else CASES[options.index(choice) - 1]["brief"]
        brief = st.text_area("Brief", default, height=140, key=f"brief_{choice}",
                             placeholder="Language; audience; what to focus on.")
        model = st.selectbox("Model", ["sonnet", "haiku", "opus"])
        with_baseline = st.checkbox("Also run the single-prompt baseline", value=True)
        if st.button("Generate draft", type="primary", disabled=not brief.strip(), use_container_width=True):
            generate(brief, model, with_baseline)
        html('<div class="side-note">A brief needs a language and an audience. Offers, claims or details the fact '
             'sheet does not support are omitted or qualified, never invented, and listed for the reviewer.</div>')
    else:
        cases = [c for c in CASES if c["id"] in RECORDED]
        choice = st.selectbox("Test brief", [f"{c['id']} · {c['brief']}" for c in cases])
        case = cases[[f"{c['id']} · {c['brief']}" for c in cases].index(choice)]
        html(f'<div class="card" style="font-size:.9rem">{escape(case["brief"])}</div>')
        if st.button("Show the recorded run", type="primary", use_container_width=True):
            rec = RECORDED[case["id"]]
            show(rec["prototype"], case["brief"], rec["baseline"])
        html('<div class="side-note"><b>Online demo.</b> Live generation needs the Claude Code CLI, so this page '
             'replays the recorded runs of the 14 test briefs (Claude Sonnet, 13 Oct 2026): real model outputs, '
             'checks and baseline. Editing the copy and the live checks work as in the local app. '
             'To generate on a new brief, run the app locally (see README).</div>')

result = st.session_state.get("result")
stage = "idle" if not result else ("clarify" if result["status"] == "needs_clarification" else "review")
html(ui.hero(len(FACTS), len(CASES)))
html(ui.trail(stage))

tab_review, tab_base, tab_facts, tab_tests, tab_log = st.tabs(
    ["Review", "Baseline comparison", "Fact sheet", "Test results", "Review log"])

# ---------- review ----------
with tab_review:
    if not result:
        html(ui.card("How it works", """<div class="row-main">1. Pick a test brief or write one in the sidebar.<br>
2. The model triages the brief against the fact sheet and drafts the email and the social post, citing a fact ID per claim.<br>
3. Code checks lengths and banned wordings; a second model call checks every claim against the facts, without seeing the brief.
One revision if anything fails.<br>4. You edit, approve or send back. Nothing is published automatically.</div>"""))
    else:
        d = result["draft"]
        run = totals(result["calls"])
        html(f'<div class="meta" style="margin-bottom:.6rem">Brief · {escape(st.session_state.brief_used)}</div>')

        if result["status"] == "needs_clarification":
            html(ui.status("clarify", "Needs clarification",
                           "The brief is missing information, so no copy was written. Answer and rerun.",
                           d.get("questions", [])))
            submitted = False
            if not LIVE:
                st.caption("In the local app the reviewer answers here and reruns the draft.")
            else:
                with st.form("clarify"):
                    c1, c2 = st.columns(2)
                    lang = c1.selectbox("Language", list(LANGUAGES))
                    audience = c2.text_input("Audience", placeholder="e.g. office commuters")
                    submitted = st.form_submit_button("Rerun with these answers")
            if submitted and audience.strip():
                generate(f"{st.session_state.brief_used} Language: {lang}. Audience: {audience}.", model, with_baseline)
                st.rerun()
        else:
            if result["status"] == "ready_for_review":
                html(ui.status("ready", "Ready for review",
                               "All automatic checks passed. Read the copy, check the evidence, then decide."))
            else:
                html(ui.status("attention", "Needs attention",
                               f"{len(result['issues'])} issue(s) remain after one revision.", result["issues"]))
            if result["revised"] and result.get("first_issues"):
                with st.expander("Fixed in the revision: issues found in the first draft"):
                    for i in result["first_issues"]:
                        st.markdown(f"- {i}")

            subject = st.session_state.ed_subject
            body = st.session_state.ed_body
            social = st.session_state.ed_social
            live = rule_checks(subject, body, social, d.get("language"))
            mail_claims, social_claims = split_claims(result["checked_claims"])

            left, right = st.columns([1.15, 1], gap="large")
            with left:
                html(f'<div class="label">Email · {escape(str(d.get("language")))} · {escape(str(d.get("audience")))}</div>')
                html(ui.email_preview(subject, body, mail_claims))
                html('<div class="label">Social post</div>')
                html(ui.social_preview(social, social_claims))
                html(ui.card("Live checks on the current text", ui.checks(live)))
                with st.expander("Edit the copy"):
                    st.text_input("Email subject", key="ed_subject")
                    st.text_area("Email body", key="ed_body", height=220)
                    st.text_area("Social post", key="ed_social", height=140)
            with right:
                html(ui.card("What the brief asked, and what was done", ui.requests(d.get("requests", []))))
                html(ui.card("Claims and evidence · independent check, brief not shown",
                             ui.claims(result["checked_claims"])))

            st.subheader("Reviewer decision")
            edited = (subject, body, social) != (d.get("email_subject"), d.get("email_body"), d.get("social_post"))
            all_ok = all(c["passed"] for c in live)
            note = st.text_input("Comment (optional)")
            c1, c2, c3 = st.columns([1.3, 1, 3])
            decision = None
            if c1.button("Approve for publication", type="primary", disabled=not all_ok):
                decision = "approved"
            if c2.button("Send back"):
                decision = "sent back"
            if not all_ok:
                c3.caption("Approval is disabled while a live check fails.")
            if decision:
                OUT.mkdir(exist_ok=True)
                entry = {"at": datetime.now().isoformat(timespec="seconds"), "brief": st.session_state.brief_used,
                         "decision": decision, "comment": note, "edited_by_reviewer": edited,
                         "review_seconds": round(time.time() - st.session_state.shown_at),
                         "auto_status": result["status"], "email_subject": subject, "email_body": body,
                         "social_post": social}
                with open(LOG, "a") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                st.success(f"Logged: {decision}. Nothing is published automatically.")

        st.caption(f"{run['n_calls']} model calls · {run['latency_s']} s · {run['tokens']:,} tokens · "
                   f"${run['cost_usd']} API-equivalent cost · revised: {'yes' if result['revised'] else 'no'}")

# ---------- baseline ----------
with tab_base:
    base = st.session_state.get("baseline")
    if not base:
        html(ui.card("Baseline", '<div class="row-main">Generate a draft with the baseline option ticked to compare '
                                 'it with the prototype on the same brief.</div>'))
    else:
        lang = result["draft"].get("language") if result else None
        left, right = st.columns(2, gap="large")
        with left:
            html('<div class="label">Baseline · one prompt, same facts and model, no checks</div>')
            html(ui.email_preview(base["email_subject"], base["email_body"], []))
            html(ui.social_preview(base["social_post"], []))
            if base["note"]:
                html(ui.card("Its note to the reviewer (free text)", f'<div class="row-main">{escape(base["note"])}</div>'))
            html(ui.card("Same automatic checks",
                         ui.checks(rule_checks(base["email_subject"], base["email_body"], base["social_post"], lang))))
            b = totals(base["calls"])
            st.caption(f"{b['n_calls']} call · {b['latency_s']} s · ${b['cost_usd']} API-equivalent cost")
        with right:
            html('<div class="label">Prototype · claims traced to facts</div>')
            if result and result["status"] != "needs_clarification":
                mc, sc = split_claims(result["checked_claims"])
                d = result["draft"]
                html(ui.email_preview(d["email_subject"], d["email_body"], mc))
                html(ui.social_preview(d["social_post"], sc))
            else:
                html(ui.status("clarify", "The prototype asked instead of writing",
                               "See the Review tab for its questions.", (result or {}).get("draft", {}).get("questions", [])))

# ---------- facts ----------
with tab_facts:
    left, right = st.columns([1.5, 1], gap="large")
    with left:
        html('<div class="label">Approved product facts · the only source of claims</div>')
        for f in FACTS:
            html(ui.fact_card(f))
    with right:
        rules = "".join(f'<div class="row"><div class="row-main">{escape(line)}</div></div>'
                        for line in BRAND_RULES.splitlines())
        html(ui.card("Brand and format rules", rules))

# ---------- tests ----------
with tab_tests:
    path = OUT / "test_results.json"
    if not path.exists():
        html(ui.card("Tests", '<div class="row-main">No test run yet. Run <code>python run_tests.py</code>.</div>'))
    else:
        data = json.loads(path.read_text())
        res = data["results"]
        n = len(res)
        mean = lambda side, key: sum(r[side][key] for r in res) / n
        asks = [r for r in res if r["type"] == "missing"]
        c = st.columns(4)
        c[0].markdown(ui.metric("Pass rate, automatic", f"{sum(r['prototype']['pass'] for r in res)}/{n}",
                                f"baseline <em>{sum(r['baseline']['pass'] for r in res)}/{n}</em>"), unsafe_allow_html=True)
        c[1].markdown(ui.metric("Asks when brief is incomplete",
                                f"{sum(r['prototype']['pass'] for r in asks)}/{len(asks)}",
                                f"baseline <em>{sum(r['baseline']['pass'] for r in asks)}/{len(asks)}</em>"), unsafe_allow_html=True)
        c[2].markdown(ui.metric("Mean latency per brief", f"{mean('prototype', 'latency_s'):.0f} s",
                                f"baseline <em>{mean('baseline', 'latency_s'):.0f} s</em>"), unsafe_allow_html=True)
        c[3].markdown(ui.metric("Cost per brief (API-equivalent)", f"${mean('prototype', 'cost_usd'):.3f}",
                                f"baseline <em>${mean('baseline', 'cost_usd'):.3f}</em>"), unsafe_allow_html=True)
        st.caption(f"Run at {data['meta']['run_at']} with model {data['meta']['model']}. Three baseline failures are "
                   "fact-checker errors on correct copy; see APPENDIX.md for the manual reading.")
        table = pd.DataFrame([{
            "id": r["id"], "type": r["type"], "brief": r["brief"], "expected": r["note"],
            "baseline": "pass" if r["baseline"]["pass"] else "fail", "baseline failures": "; ".join(r["baseline"]["fails"]),
            "prototype": "pass" if r["prototype"]["pass"] else "fail", "prototype status": r["prototype"]["status"],
        } for r in res])
        st.dataframe(table, hide_index=True, use_container_width=True)
        for r in res:
            p = r["prototype"]
            with st.expander(f"{r['id']} · {r['brief']}"):
                left, right = st.columns(2, gap="large")
                with left:
                    html(f'<div class="label">Baseline · <span class="pill {"pass" if r["baseline"]["pass"] else "fail"}">'
                         f'{"pass" if r["baseline"]["pass"] else "fail"}</span></div>')
                    mc, sc = split_claims(r["baseline"]["checked_claims"])
                    html(ui.email_preview(r["baseline"]["email_subject"], r["baseline"]["email_body"], mc))
                    html(ui.social_preview(r["baseline"]["social_post"], sc))
                with right:
                    html(f'<div class="label">Prototype · <span class="pill {"pass" if p["pass"] else "fail"}">'
                         f'{"pass" if p["pass"] else "fail"}</span></div>')
                    if p["status"] == "needs_clarification":
                        html(ui.status("clarify", "Asked instead of writing", "", p["draft"].get("questions", [])))
                    else:
                        mc, sc = split_claims(p["checked_claims"])
                        html(ui.email_preview(p["draft"]["email_subject"], p["draft"]["email_body"], mc))
                        html(ui.social_preview(p["draft"]["social_post"], sc))
                        html(ui.card("Requests", ui.requests(p["draft"].get("requests", []))))

# ---------- log ----------
with tab_log:
    if LOG.exists():
        rows = [json.loads(line) for line in LOG.read_text().splitlines() if line.strip()]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    else:
        html(ui.card("Review log", '<div class="row-main">No review decision logged yet.</div>'))
