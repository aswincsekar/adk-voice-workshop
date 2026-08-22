import base64
import importlib.util
import json
import sys
from pathlib import Path

import pytest

PRODUCTION_DIR = Path(__file__).resolve().parents[1] / "checkpoints" / "06_production"
sys.path.insert(0, str(PRODUCTION_DIR))
spec = importlib.util.spec_from_file_location("production_server", PRODUCTION_DIR / "server.py")
assert spec and spec.loader
production_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(production_server)
sys.path.pop(0)


def test_production_server_validates_audio_messages():
    audio = b"\x00\x01\x02\x03"
    raw_message = json.dumps(
        {
            "type": "audio",
            "mime_type": "audio/pcm;rate=16000",
            "data": base64.b64encode(audio).decode("ascii"),
        }
    )
    message = production_server.parse_client_message(raw_message)
    assert production_server.decode_audio(message) == audio


def test_production_server_rejects_unknown_message_types():
    with pytest.raises(production_server.ClientMessageError):
        production_server.parse_client_message('{"type":"admin"}')


def test_production_run_config_has_session_guards():
    run_config = production_server.build_run_config()
    assert run_config.max_llm_calls == 100
    assert run_config.session_resumption is not None
    assert run_config.session_resumption.transparent is None
    assert run_config.context_window_compression.trigger_tokens == 100_000
    assert run_config.context_window_compression.sliding_window.target_tokens == 80_000
    assert run_config.tool_thread_pool_config.max_workers == 4
