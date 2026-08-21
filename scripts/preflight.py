from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def check(ok: bool, label: str, help_text: str) -> None:
    if ok:
        print(f"✓ {label}")
        return
    print(f"✗ {label}: {help_text}")
    raise SystemExit(1)


check(sys.version_info >= (3, 11), "Python", "install Python 3.11 or newer")
check(importlib.util.find_spec("google.adk") is not None, "Dependencies", "run: uv sync")

key = os.getenv("GOOGLE_API_KEY", "")
check(bool(key and key != "replace_me"), "API key configuration", "copy .env.example to .env")
check(
    os.getenv("GOOGLE_GENAI_USE_ENTERPRISE", "FALSE").upper() == "FALSE",
    "AI Studio mode",
    "set GOOGLE_GENAI_USE_ENTERPRISE=FALSE",
)

expected = [f"checkpoints/{name}" for name in [
    "00_start", "01_basic", "02_tool", "03_voice", "04_slow_failure", "05_custom_streaming"
]]
check(all((ROOT / folder).is_dir() for folder in expected), "Workshop checkpoints", "re-clone repo")

print("READY")

