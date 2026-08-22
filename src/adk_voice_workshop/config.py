from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")


def live_model() -> str:
    return os.getenv("LIVE_MODEL", "gemini-3.1-flash-live-preview")
