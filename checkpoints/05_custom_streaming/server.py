from __future__ import annotations

import asyncio
import base64
import contextlib
import logging
from pathlib import Path
from uuid import uuid4

from agent import root_agent
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import InMemoryRunner
from google.genai import errors as genai_errors
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-workshop")

APP_NAME = "adk-voice-workshop"
STATIC_DIR = Path(__file__).with_name("static")
runner = InMemoryRunner(app_name=APP_NAME, agent=root_agent)

app = FastAPI(title="ADK Voice Workshop")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def is_normal_close(exc: Exception) -> bool:
    return isinstance(exc, genai_errors.APIError) and exc.status_code == 1000


def transcript_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return getattr(value, "text", None)


async def browser_to_agent(websocket: WebSocket, queue: LiveRequestQueue) -> None:
    """Upstream loop: browser audio/control messages -> LiveRequestQueue."""
    while True:
        message = await websocket.receive_json()
        message_type = message.get("type")
        if message_type == "audio":
            queue.send_realtime(
                types.Blob(
                    data=base64.b64decode(message["data"]),
                    mime_type=message.get("mime_type", "audio/pcm;rate=16000"),
                )
            )
        elif message_type == "activity_start":
            queue.send_activity_start()
        elif message_type == "activity_end":
            queue.send_activity_end()
        elif message_type == "audio_stream_end":
            queue.send_audio_stream_end()


async def agent_to_browser(websocket: WebSocket, events) -> None:
    """Downstream loop: run_live Event stream -> browser messages."""
    async for event in events:
        input_text = transcript_text(getattr(event, "input_transcription", None))
        output_text = transcript_text(getattr(event, "output_transcription", None))
        if input_text:
            await websocket.send_json({"type": "transcript", "speaker": "you", "text": input_text})
        if output_text:
            await websocket.send_json(
                {"type": "transcript", "speaker": "agent", "text": output_text}
            )

        for part in (event.content.parts if event.content and event.content.parts else []):
            mime_type = part.inline_data.mime_type if part.inline_data else None
            if part.inline_data and mime_type and mime_type.startswith("audio/pcm"):
                await websocket.send_json(
                    {
                        "type": "audio",
                        "mime_type": mime_type,
                        "data": base64.b64encode(part.inline_data.data).decode("ascii"),
                    }
                )
            if part.function_call:
                await websocket.send_json(
                    {"type": "tool", "phase": "call", "name": part.function_call.name}
                )
            if part.function_response:
                await websocket.send_json(
                    {"type": "tool", "phase": "result", "name": part.function_response.name}
                )

        if event.interrupted:
            await websocket.send_json({"type": "interrupted"})
        if event.turn_complete:
            await websocket.send_json({"type": "turn_complete"})


@app.websocket("/ws")
async def voice_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    user_id = f"workshop-{uuid4().hex[:8]}"
    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=user_id)
    queue = LiveRequestQueue()  # A fresh queue for every streaming session.
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=[types.Modality.AUDIO],
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
    )
    events = runner.run_live(
        user_id=user_id,
        session_id=session.id,
        live_request_queue=queue,
        run_config=run_config,
    )

    upstream = asyncio.create_task(browser_to_agent(websocket, queue))
    downstream = asyncio.create_task(agent_to_browser(websocket, events))
    try:
        done, pending = await asyncio.wait(
            {upstream, downstream}, return_when=asyncio.FIRST_COMPLETED
        )
        for task in done:
            with contextlib.suppress(WebSocketDisconnect):
                task.result()
        for task in pending:
            task.cancel()
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        if not is_normal_close(exc):
            logger.exception("Live session failed")
            with contextlib.suppress(Exception):
                await websocket.send_json({"type": "error", "message": "Live session ended"})
    finally:
        queue.close()
        for task in (upstream, downstream):
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task
