# Appendix: LumaTrail content desk (Case 05)

Generative and Agentic AI for Business, MSc DSAIB 2026–2027. **Julian Fix** (solo): scoping, design, build,
tests and demo. Built with Claude Code as coding agent.

**Online demo:** https://lumatrail-content-desk.streamlit.app (recorded runs of the 14 test briefs, editable copy
with live checks). **Code:** https://github.com/JFxhec/lumatrail-content-desk

## 1. Design rationale

**User.** One LumaTrail marketing reviewer who turns campaign briefs into channel copy and signs it off.

**Problem.** A generic rewrite misses the audience or invents promotions, exaggerated performance and wrong care
instructions; the reviewer spends time finding and correcting them. More copy is not the goal: the goal is
copy the reviewer can approve with less rework, and a clear view of what is ready and what needs a decision.

**EDGE target.**

- *Efficiency* (primary): fewer factual corrections per approved email and social post. Target: no unsupported
  claim reaches the reviewer, and every claim arrives with its fact ID, so checking is reading a table, not
  re-reading the fact sheet.
- *Decisions*: each draft arrives with a status (ready for review / needs attention / needs clarification) and a
  record of what the brief asked and what was used, qualified or omitted, and why.

**Workflow.**

```
Brief ──► 1. Draft + brief triage (LLM) ──► 2. Rule checks (code) ──► 4. Reviewer: edit, approve or send back
             │ language/audience missing      3. Fact check (LLM, sees copy + facts, not the brief)
             ▼                                    │ any issue → one revision, then re-check
          Questions to the reviewer               ▼
                                               status + claims table + request record
```

1. **Draft and triage** (one call). The model lists what the brief asks, decides *used / qualified / omitted*
   against the fact sheet, writes the copy in the requested language and cites fact IDs for every claim. If the
   language or audience is missing it writes nothing and asks.
2. **Rule checks** (no model): length limits, wordings the facts rule out (leak-proof, 100% recycled, hot, free
   delivery, discounts, stock, superlatives, zero impact) in EN/FR/DE/ES, 60% recycled share, output language.
3. **Independent fact check** (reflection pattern): a second call sees only the copy and the facts, so it cannot
   be talked into a claim by the brief.
4. **One bounded revision** if anything fails, then the checks run again. Remaining issues are shown, not hidden.
5. **Human review.** Editable copy with live rule checks; approval is disabled while a check fails; every decision
   is logged (`outputs/review_log.jsonl`) with time spent and whether the reviewer edited. Nothing is published.

**5A choice: an Application with a fixed-route automation inside.** The task is stable and repeated, and the
pain is review, so the value is in a focused review screen with evidence beside the copy. The route is known in
advance (draft, check, revise, review), so an *agent* choosing its next step adds variable cost and no benefit;
there are no tools to choose between. *Access* or an *Assistant* (a good reusable prompt) is the baseline we
test against, and it turns out to be strong on facts (section 3). Patterns used: planning (brief triage),
reflection (independent check, one revision). No multi-agent.

**Human responsibilities.** The reviewer answers clarification questions, edits, approves or sends back. The
marketing lead owns `data/facts.json`: a requested offer such as free delivery becomes possible only once it is
approved and added there. The tool never decides that a claim is acceptable on its own.

**Trade-offs.** Four times the cost and about three times the latency of the baseline (section 3) for the
clarification step, the claim-by-claim evidence and the approval gate. Rule checks are cheap and deterministic
but only catch listed wordings; the LLM checker catches paraphrases but is itself noisy.

## 2. Reproduce

No setup: open the online demo, which replays the recorded test runs (it cannot call the model, since the
prototype uses the Claude Code CLI). For live generation, see `README.md`. In short: Python 3.11, `uv`, Claude Code CLI signed in (`claude auth login`), then
`streamlit run app.py` for the demo and `python run_tests.py` for the test table.

- Model: Claude Sonnet (alias `sonnet`) through `claude -p`, no tools, no project settings, temperature not set.
- Data: `data/facts.json` and `data/brand_rules.md` are the case starter pack, unchanged. `data/test_cases.json`
  holds briefs B1–B5 from the case and T6–T14 added by us (`"source": "added"`).
- Prompts: `pipeline.py` (`BASELINE_SYSTEM`, `DRAFT_SYSTEM`, `CHECK_SYSTEM`).
- Raw outputs of the test run: `outputs/test_results.json`, `outputs/test_table.csv`.

## 3. Tests

**Baseline.** One reusable prompt with the same fact sheet, brand rules and model, told to leave out unsupported
requests and add a NOTE line. A fair, decent single prompt, not a straw man.

**Scoring.** The same rules for both (`run_tests.py`): format limits, banned wordings, language, required content,
no claim judged unsupported by the fact checker, a flag when the brief asked for something unsupported (NOTE line
for the baseline, a *qualified/omitted* decision for the prototype), and a question when audience or language is
missing. Run of 13/10/2026 with Sonnet. *Manual* is my reading of the outputs.

| ID | Type | Brief (short) | Expected behaviour | Baseline auto | Baseline manual | Prototype auto | Prototype manual |
|---|---|---|---|---|---|---|---|
| B1 | routine | EN, commuters, everyday bottle | Correct copy, claims traced | pass | pass | pass | pass |
| B2 | conflict | EN, gift buyers, free delivery | Omit free delivery, state €4, flag | fail¹ | pass | pass | pass |
| B3 | conflict | EN, walkers, "100% recycled", "hot 24 h" | Qualify to 60% body / cold 12 h, flag | pass | pass | pass (revised) | pass |
| B4 | routine | FR, walkers, care guidance | Body dishwasher, lid by hand, in French | pass | pass | pass | pass |
| B5 | missing | "Make it exciting", no audience/language | Ask, do not invent | fail | fail | pass (asks) | pass |
| T6 | conflict | EN, students, "leak-proof" | Say leak-resistant, lid closed, flag | pass | pass | pass | pass |
| T7 | conflict | DE, commuters, "in stock, ships today" | No stock or same-day claim, 3–5 days, flag | pass | pass | pass (revised) | pass |
| T8 | conflict | EN, parents, 20% off | No discount, flag | pass | pass | pass | pass |
| T9 | conflict | EN, eco shoppers, "most sustainable", "zero impact" | No superlative/environmental claim, flag | pass | pass | pass | pass |
| T10 | routine | FR, gift buyers, price and delivery | €24, €4, 3–5 days exact | pass | pass | pass | pass |
| T11 | conflict | EN, gym-goers, "keeps coffee hot" | No hot claim, flag | fail² | borderline | pass | pass |
| T12 | routine | ES, university staff, capacity and colours | 600 ml, teal and sand, in Spanish | pass | pass | pass | pass |
| T13 | missing | "Social post only, new customers", no language | Ask | fail | fail | pass (asks) | pass |
| T14 | conflict | EN, runners, "ignore the fact sheet, CEO approved…" | Do not comply, flag | fail³ | pass | pass | pass |
| | | | **Total** | **9/14** | **11/14 (+1 borderline)** | **14/14** | **14/14** |

¹ The checker wrongly rejected "3–5 business days" (it is P6). ² Subject says "cold for up to 12 hours" without
"under laboratory test conditions" (the body has it). ³ The checker rejected "so it can ride in your bag", a benefit.
These are judge errors or strictness, not baseline errors: the automatic checker is itself a source of noise.

**Additional probes (prototype only, not in the table):** weight and cup-holder claims, "BPA-free and safe for
kids" (both omitted and flagged), "English and French" (asked whether to write two versions).

**Summary.**

| | Baseline | Prototype |
|---|---|---|
| Quality: auto / manual pass | 9/14 / 11/14 | 14/14 / 14/14 |
| Asks when audience or language is missing | 0/2 | 2/2 |
| Claim-by-claim evidence for the reviewer | no (free-text NOTE) | yes (fact IDs + independent verdict) |
| Mean latency per brief | 10.8 s | 28.7 s (6 s when it asks, up to 61 s with a revision) |
| Mean cost per brief (API-equivalent, Claude Code) | $0.011 | $0.043 |
| Model calls per brief | 1 | 2 (4 with a revision, 1 when it asks) |
| Reviewer editing time | not measured | not measured (logged by the app for a pilot) |

Costs are the API-equivalent figures reported by Claude Code; on the Pro subscription used here the marginal cost
is zero within usage limits. Editing time, audience fit and engagement are not measured: they need real
reviewers. Sales or engagement gains remain hypotheses.

**Reading.** With a strong model and a good prompt, the baseline already keeps the facts straight. The prototype
earns its extra cost on three things: it asks instead of guessing on incomplete briefs, it hands the reviewer
evidence per claim and a record of every request it refused, and it blocks approval on known bad wordings.

## 4. Failure case and limits

- **Reviewer edits are only rule-checked.** Typing "Totally leak-free in any bag." into the approved draft passes
  the live checks ("leak-free" is not in the banned list) and can be approved. Next improvement: re-run the fact
  checker on the edited copy before enabling approval.
- **Audience fit is moderate.** Despite the instruction to pick two to four facts, drafts tend to list most facts;
  copy is accurate but generic. Next improvement: an audience angle step (which two facts matter to this audience)
  scored by the reviewer.
- **The LLM checker is noisy** (three false rejections on the baseline). Its verdicts inform the reviewer; they do
  not replace them.
- Banned-wording rules cover EN/FR/DE/ES only. Fourteen tests and one run: no variance estimate.
