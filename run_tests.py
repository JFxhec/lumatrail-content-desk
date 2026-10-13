"""Run every test brief through the baseline and the prototype, score both with the same checks.

Usage: python run_tests.py [--only B1 B2] [--model sonnet] [--workers 3]
"""

import argparse
import csv
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from llm import DEFAULT_MODEL
from pipeline import DATA, fact_check, rule_checks, run_baseline, run_prototype, totals

OUT = Path(__file__).parent / "outputs"


def score(expect: dict, status: str, subject: str, body: str, social: str, checked: list,
          flagged: bool, questions: list) -> tuple[bool, list[str]]:
    """Same pass/fail rules for baseline and prototype. Returns (passed, reasons for failure)."""
    if expect["status"] == "clarify":
        ok = status == "needs_clarification" and bool(questions)
        return ok, [] if ok else ["did not ask for the missing audience/language"]
    if status == "needs_clarification":
        return False, ["asked for clarification on a complete brief"]
    fails = [f"{c['check']}: {c['detail']}" for c in rule_checks(subject, body, social, expect["language"]) if not c["passed"]]
    copy = f"{subject}\n{body}\n{social}"
    fails += [f"missing required content /{p}/" for p in expect["required"] if not re.search(p, copy, re.I)]
    fails += [f"unsupported claim: {c['text']}" for c in checked if c.get("verdict") != "supported"]
    if expect["flag"] and not flagged:
        fails.append("unsupported request not flagged to the reviewer")
    return not fails, fails


def run_case(case: dict, model: str) -> dict:
    expect = case["expect"]

    base = run_baseline(case["brief"], model)
    base_status = "needs_clarification" if not (base["email_subject"] or base["email_body"]) else "draft"
    base_checked = []
    if base_status == "draft":  # evaluation-only fact check, not part of the baseline's cost
        base_checked, _ = fact_check(base["email_subject"], base["email_body"], base["social_post"], model)
    base_pass, base_fails = score(expect, base_status, base["email_subject"], base["email_body"], base["social_post"],
                                  base_checked, flagged=bool(base["note"]), questions=[base["raw"]] if base_status != "draft" else [])

    proto = run_prototype(case["brief"], model)
    d = proto["draft"]
    flagged = any(r.get("decision") in ("qualified", "omitted") for r in d.get("requests", []))
    proto_pass, proto_fails = score(expect, proto["status"], d.get("email_subject", ""), d.get("email_body", ""),
                                    d.get("social_post", ""), proto["checked_claims"], flagged, d.get("questions", []))
    if expect["status"] == "ready" and proto["status"] == "needs_attention" and proto_pass:
        proto_pass, proto_fails = False, ["left in 'needs attention' after revision"]

    return {
        "id": case["id"], "source": case["source"], "type": case["type"], "brief": case["brief"], "note": case["note"],
        "baseline": {**base, "checked_claims": base_checked, "pass": base_pass, "fails": base_fails, **totals(base["calls"])},
        "prototype": {**proto, "pass": proto_pass, "fails": proto_fails, **totals(proto["calls"])},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    cases = json.loads((DATA / "test_cases.json").read_text())
    if args.only:
        cases = [c for c in cases if c["id"] in args.only]

    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(lambda c: run_case(c, args.model), cases))
    for r in results:
        print(f"{r['id']:>4}  baseline {'PASS' if r['baseline']['pass'] else 'FAIL'}  "
              f"prototype {'PASS' if r['prototype']['pass'] else 'FAIL'}  ({r['prototype']['status']})")

    OUT.mkdir(exist_ok=True)
    meta = {"run_at": datetime.now().isoformat(timespec="seconds"), "model": args.model}
    (OUT / "test_results.json").write_text(json.dumps({"meta": meta, "results": results}, ensure_ascii=False, indent=1))

    rows = [{
        "id": r["id"], "source": r["source"], "type": r["type"], "brief": r["brief"], "expected": r["note"],
        "baseline_pass": r["baseline"]["pass"], "baseline_fails": "; ".join(r["baseline"]["fails"]),
        "baseline_latency_s": r["baseline"]["latency_s"], "baseline_cost_usd": r["baseline"]["cost_usd"],
        "prototype_status": r["prototype"]["status"], "prototype_pass": r["prototype"]["pass"],
        "prototype_fails": "; ".join(r["prototype"]["fails"]), "prototype_revised": r["prototype"]["revised"],
        "prototype_latency_s": r["prototype"]["latency_s"], "prototype_cost_usd": r["prototype"]["cost_usd"],
    } for r in results]
    with open(OUT / "test_table.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    n = len(rows)
    print(f"\nBaseline  {sum(r['baseline_pass'] for r in rows)}/{n} pass, "
          f"mean {sum(r['baseline_latency_s'] for r in rows) / n:.1f}s, ${sum(r['baseline_cost_usd'] for r in rows):.3f}")
    print(f"Prototype {sum(r['prototype_pass'] for r in rows)}/{n} pass, "
          f"mean {sum(r['prototype_latency_s'] for r in rows) / n:.1f}s, ${sum(r['prototype_cost_usd'] for r in rows):.3f}")


if __name__ == "__main__":
    main()
