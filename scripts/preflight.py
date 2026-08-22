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


check(
    (3, 11) <= sys.version_info[:2] < (3, 14),
    "Python 3.11–3.13",
    "install a supported Python version (3.11, 3.12, or 3.13)",
)
check(importlib.util.find_spec("google.adk") is not None, "Dependencies", "run: uv sync")

keys = [os.getenv("GEMINI_API_KEY", ""), os.getenv("GOOGLE_API_KEY", "")]
check(
    any(key and key != "replace_me" for key in keys),
    "API key configuration",
    "copy .env.example to .env and add an AI Studio key",
)
check(
    all(
        os.getenv(name, "FALSE").upper() in {"FALSE", "0"}
        for name in ("GOOGLE_GENAI_USE_ENTERPRISE", "GOOGLE_GENAI_USE_VERTEXAI")
    ),
    "AI Studio mode",
    "set GOOGLE_GENAI_USE_ENTERPRISE=FALSE and GOOGLE_GENAI_USE_VERTEXAI=FALSE",
)
check(
    os.getenv("TEXT_MODEL", "gemini-3.6-flash") == "gemini-3.6-flash",
    "Text model",
    "set TEXT_MODEL=gemini-3.6-flash in .env",
)
check(
    os.getenv("LIVE_MODEL", "gemini-3.1-flash-live-preview")
    == "gemini-3.1-flash-live-preview",
    "Live model",
    "set LIVE_MODEL=gemini-3.1-flash-live-preview in .env",
)

expected = [f"checkpoints/{name}" for name in [
    "00_start", "01_basic", "02_tool", "03_voice", "04_slow_failure",
    "05_custom_streaming", "06_production"
]]
check(all((ROOT / folder).is_dir() for folder in expected), "Workshop checkpoints", "re-clone repo")

print("READY")
