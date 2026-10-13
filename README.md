# LumaTrail content desk (Case 05)

Generative and Agentic AI for Business, MSc DSAIB 2026–2027 (Shubin Yu). Solo project: Julian Fix.

A local Streamlit application that turns a short campaign brief and the approved fact sheet into an email
(subject and body) and a social post, traces every product claim to a fact ID, flags unsupported requests,
asks when the brief is incomplete, and keeps a human approval step before publication.

## Files

| Path | Content |
|---|---|
| `app.py` | Streamlit app: brief, checked draft, reviewer decision, baseline comparison, test results |
| `theme.py`, `.streamlit/config.toml` | Visual layer: "field notebook" art direction in the product colours (teal, sand) |
| `pipeline.py` | Prompts, baseline, prototype workflow, deterministic checks |
| `llm.py` | Model calls through the Claude Code CLI (headless mode) |
| `run_tests.py` | Runs every test brief through baseline and prototype, scores both with the same rules |
| `data/facts.json`, `data/brand_rules.md` | Starter pack from the case (unchanged) |
| `data/test_cases.json` | B1–B5 from the case, T6–T14 added for testing (labelled `"source": "added"`) |
| `outputs/` | `test_results.json`, `test_table.csv`, `review_log.jsonl` |
| `APPENDIX.md` / `APPENDIX.pdf` | Design rationale (EDGE / 5A), reproduction, test table, failure case |
| `docs/demo_script.md` | Timed narration for the demo video |

## Run

Requirements: Python 3.11+, `uv`, and the Claude Code CLI signed in with a Claude account
(the prototype uses `claude -p`, so a Claude Pro subscription is enough and no API key is needed).

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
claude auth login            # once
.venv/bin/streamlit run app.py
.venv/bin/python run_tests.py   # full test run, about 70 model calls
```

Environment variables: `CLAUDE_BIN` (path to the CLI if not on the PATH), `LUMA_MODEL` (default `sonnet`).

## Notes

- Model: Claude Sonnet through Claude Code, no tools, no project settings, empty working directory.
- Cost figures are the API-equivalent cost reported by Claude Code; on a Pro subscription the marginal cost is zero
  within usage limits.
- All company data is fictional teaching material from the case. Nothing is published; approval writes a log line.
