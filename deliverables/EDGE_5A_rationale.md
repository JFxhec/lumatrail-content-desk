<div class="cover"><div class="kicker">MSc DSAIB · 2026–2027 · AI solution sprint</div><h1>EDGE / 5A design rationale</h1><div class="case">LumaTrail content desk: on-brief, fact-checked product copy</div><table class="meta"><tr><td class="k">Author</td><td><b>Julian Fix</b> (solo project)</td></tr><tr><td class="k">Course</td><td>Generative and Agentic AI for Business · Prof. Shubin Yu</td></tr><tr><td class="k">Programme</td><td>MSc Data Science and AI for Business (DSAIB) · Year 2 · 2026–2027</td></tr><tr><td class="k">Case</td><td>Case 05 · Create product content that stays on brief</td></tr><tr><td class="k">Date</td><td>13 October 2026</td></tr><tr><td class="k">Links</td><td><a href="https://lumatrail-content-desk.streamlit.app">lumatrail-content-desk.streamlit.app</a> · <a href="https://github.com/JFxhec/lumatrail-content-desk">github.com/JFxhec/lumatrail-content-desk</a></td></tr></table></div>


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
test against, and it turns out to be strong on facts (see the results report). Patterns used: planning (brief triage),
reflection (independent check, one revision). No multi-agent.

**Human responsibilities.** The reviewer answers clarification questions, edits, approves or sends back. The
marketing lead owns `data/facts.json`: a requested offer such as free delivery becomes possible only once it is
approved and added there. The tool never decides that a claim is acceptable on its own.

**Trade-offs.** Four times the cost and about three times the latency of the baseline (see the results report) for the
clarification step, the claim-by-claim evidence and the approval gate. Rule checks are cheap and deterministic
but only catch listed wordings; the LLM checker catches paraphrases but is itself noisy.

