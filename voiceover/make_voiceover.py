"""Generate the demo voice-over with macOS text-to-speech: one .m4a per segment plus the full track.

Usage: python voiceover/make_voiceover.py [--voice Daniel] [--rate 165]
"""

import argparse
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PAUSE_MS = 1200  # silence between segments in the full track


def render(text: str, out: Path, voice: str, rate: int):
    aiff = out.with_suffix(".aiff")
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(aiff), text], check=True)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", str(aiff), str(out)], check=True)
    aiff.unlink()


def duration(path: Path) -> float:
    info = subprocess.run(["afinfo", str(path)], capture_output=True, text=True).stdout
    return float(re.search(r"estimated duration: ([\d.]+)", info).group(1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default="Daniel")
    parser.add_argument("--rate", type=int, default=165)
    args = parser.parse_args()

    blocks = re.findall(r"^## (\S+) \| (.*?)\n(.*?)(?=^## |\Z)", (HERE / "narration.txt").read_text(), re.S | re.M)
    total = 0.0
    for name, screen, text in blocks:
        out = HERE / f"{name}.m4a"
        render(text.strip(), out, args.voice, args.rate)
        d = duration(out)
        print(f"{total // 60:.0f}:{total % 60:04.1f}  {name:<14} {d:5.1f}s  {screen}")
        total += d + PAUSE_MS / 1000

    full = f" [[slnc {PAUSE_MS}]] ".join(text.strip() for _, _, text in blocks)
    render(full, HERE / "voiceover_full.m4a", args.voice, args.rate)
    print(f"Full track: {duration(HERE / 'voiceover_full.m4a'):.0f}s")


if __name__ == "__main__":
    main()
