from pathlib import Path


def test_no_real_key_is_committed():
    root = Path(__file__).resolve().parents[1]
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".py", ".md", ".toml", ".example", ".js", ".html", ".css"}:
            continue
        text = path.read_text(errors="ignore")
        key_prefix = "AI" + "za"
        assert key_prefix not in text, f"Possible Google API key in {path}"
