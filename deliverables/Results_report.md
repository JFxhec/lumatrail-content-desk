<div class="cover"><div class="kicker">MSc DSAIB · 2026–2027 · AI solution sprint</div><h1>Results: task success, latency and cost</h1><div class="case">LumaTrail content desk: on-brief, fact-checked product copy</div><table class="meta"><tr><td class="k">Author</td><td><b>Julian Fix</b> (solo project)</td></tr><tr><td class="k">Course</td><td>Generative and Agentic AI for Business · Prof. Shubin Yu</td></tr><tr><td class="k">Programme</td><td>MSc Data Science and AI for Business (DSAIB) · Year 2 · 2026–2027</td></tr><tr><td class="k">Case</td><td>Case 05 · Create product content that stays on brief</td></tr><tr><td class="k">Date</td><td>13 October 2026</td></tr><tr><td class="k">Links</td><td><a href="https://lumatrail-content-desk.streamlit.app">lumatrail-content-desk.streamlit.app</a> · <a href="https://github.com/JFxhec/lumatrail-content-desk">github.com/JFxhec/lumatrail-content-desk</a></td></tr></table></div>

## Tests

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


## Failure case and limits

- **Reviewer edits are only rule-checked.** Typing "Totally leak-free in any bag." into the approved draft passes
  the live checks ("leak-free" is not in the banned list) and can be approved. Next improvement: re-run the fact
  checker on the edited copy before enabling approval.
- **Audience fit is moderate.** Despite the instruction to pick two to four facts, drafts tend to list most facts;
  copy is accurate but generic. Next improvement: an audience angle step (which two facts matter to this audience)
  scored by the reviewer.
- **The LLM checker is noisy** (three false rejections on the baseline). Its verdicts inform the reviewer; they do
  not replace them.
- Banned-wording rules cover EN/FR/DE/ES only. Fourteen tests and one run: no variance estimate.
