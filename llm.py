"""Call Claude through the Claude Code CLI in headless mode (uses the Claude Pro subscription)."""

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

DEFAULT_MODEL = os.environ.get("LUMA_MODEL", "sonnet")


def find_claude() -> str:
    if os.environ.get("CLAUDE_BIN"):
        return os.environ["CLAUDE_BIN"]
    found = shutil.which("claude")
    if found:
        return found
    for candidate in [Path.home() / ".local/bin/claude", Path.home() / ".claude/local/claude"]:
        if candidate.exists():
            return str(candidate)
    raise RuntimeError("Claude Code CLI not found. Install it, run `claude auth login`, or set CLAUDE_BIN.")


def call_claude(system: str, prompt: str, model: str = DEFAULT_MODEL, timeout: int = 240) -> dict:
    """One model call, no tools, no project settings. Returns text, latency and cost."""
    cmd = [
        find_claude(), "-p",
        "--output-format", "json",
        "--model", model,
        "--system-prompt", system,
        "--tools", "",
        "--no-session-persistence",
        "--setting-sources", "",
        "--strict-mcp-config",
        "--disable-slash-commands",
    ]
    start = time.time()
    with tempfile.TemporaryDirectory() as tmp:  # empty cwd: no CLAUDE.md or project files leak in
        out = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=tmp)
    latency = time.time() - start
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Claude Code returned no JSON: {(out.stderr or out.stdout)[:500]}")
    if data.get("is_error"):
        raise RuntimeError(f"Claude Code error: {data.get('result')}")
    usage = data.get("usage", {})
    return {
        "text": data.get("result", ""),
        "latency_s": round(latency, 1),
        "cost_usd": data.get("total_cost_usd", 0.0),
        "input_tokens": usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }


def parse_json(text: str) -> dict:
    """Extract the JSON object from a model reply (tolerates code fences or stray text)."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object in reply: {text[:300]}")
    return json.loads(text[start:end + 1])
