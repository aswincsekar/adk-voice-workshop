# Building Voice Agents with Google ADK

A guided Python workshop that goes from a tiny typed-prompt agent to a real-time voice agent with tools, interruption, transcription, and failure handling.

## Workshop slides

- [PowerPoint deck](slides/google-adk-voice-agents-workshop.pptx) — downloadable/offline copy kept with the code
- [Live Google Slides](https://docs.google.com/presentation/d/1n0RPi-yYbqH_e_r23KlJAldgGFxdpRez7lVCUqkLLc0/edit) — presentation version for the workshop

## What participants build

1. A basic ADK agent
2. A room-finding function tool
3. A voice agent in the ADK development UI
4. A slow/failing tool experiment
5. An optional FastAPI + WebSocket streaming app
6. A production-hardening pass on the custom streaming web app

Every stage has a runnable checkpoint. If you get stuck, jump to the next folder and continue.

## Before the workshop

You need:

- Python 3.11–3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Chrome or another Chromium browser
- Headphones and a microphone
- A Google AI Studio API key

## Fast setup

```bash
git clone <WORKSHOP_REPO_URL>
cd adk-voice-workshop
cp .env.example .env
# Put the workshop key in GEMINI_API_KEY (or GOOGLE_API_KEY) in .env.
# Never commit or paste it in chat.
uv sync
uv run python scripts/preflight.py
```

Expected result:

```text
✓ Python 3.11–3.13
✓ Dependencies
✓ API key configuration
✓ AI Studio mode
✓ Text model
✓ Live model
✓ Workshop checkpoints
READY
```

## Run a checkpoint

Typed-prompt checkpoint:

```bash
cd checkpoints/01_basic
uv run adk web
```

Checkpoints 00–02 use the stable text model `gemini-3.6-flash`. Type prompts
with the send button; do not start the microphone/audio mode, because that
opens `/run_live` and text-only models do not support the Live API. Checkpoint
03 switches to `gemini-3.1-flash-live-preview` for microphone input and native
audio.

Tool agent:

```bash
cd checkpoints/02_tool
uv run adk web
```

Voice agent:

```bash
cd checkpoints/03_voice
export SSL_CERT_FILE="$(uv run python -m certifi)"
uv run adk web
```

Open the printed local URL, select `room_agent`, allow microphone access, and say:

> Find a room after three.

The native-audio model is voice-first. Use the microphone rather than the text box in the voice checkpoints.

Slow/failure demo:

```bash
cd checkpoints/04_slow_failure
uv run adk web
```

Ask for a room after three to hear the deliberate five-second delay. Ask for a
room after one p.m. (13:00), or set `ROOM_TOOL_FAIL=1`, to trigger the friendly
failure path. The tool returns a structured error; the agent should not expose a
Python exception or retry without asking.

## Workshop map

| Folder | Moment | What changes |
|---|---|---|
| `00_start` | Start here | Minimal agent; edit the instruction |
| `01_basic` | Basic agent | Clear room-assistant behavior |
| `02_tool` | Add a tool | Agent can call `find_rooms` |
| `03_voice` | Enable voice | Switch to the Live API model and use the microphone |
| `04_slow_failure` | Break it | Slow tool, timeout, and failure experiment |
| `05_custom_streaming` | Look underneath | `run_live`, `LiveRequestQueue`, WebSocket, audio, events, transcription |
| `06_production` | Harden it | Add WebSocket controls, session resilience, budgets, and safe logging |

## Run the custom streaming app

This is the optional advanced checkpoint:

```bash
cd checkpoints/05_custom_streaming
uv run uvicorn server:app --reload --port 8001
```

Open [http://localhost:8001](http://localhost:8001), click **Connect microphone**, and use headphones.

## Run the production-hardening checkpoint

```bash
cd checkpoints/06_production
uv run uvicorn server:app --reload --port 8002
```

Open [http://localhost:8002](http://localhost:8002). This checkpoint hardens
the custom streaming server from checkpoint 05. See
[`checkpoints/06_production/README.md`](checkpoints/06_production/README.md) for
the implemented controls and the infrastructure still required before a real deployment.

## API-key safety for a workshop

- Never commit the key. `.env` is ignored by Git. Both `GEMINI_API_KEY` and
  `GOOGLE_API_KEY` are accepted by the workshop.
- Prefer a dedicated workshop key and project, with the smallest practical quota.
- Give the key only to registered participants and rotate/delete it immediately after the session.
- Expect preview Live API models to have tighter quotas than text models.
- If attendees can create their own AI Studio keys, that is safer and avoids one shared quota bottleneck.

## Troubleshooting

- **No microphone:** allow browser microphone permission, reload, and use `localhost`.
- **Certificate error on macOS:** set `SSL_CERT_FILE` using the command above.
- **Quota/rate limit:** pair participants or switch to a participant-owned AI Studio key.
- **Model not found:** verify `LIVE_MODEL` in `.env` against the current Live API model list. Preview model names can change.
- **`not supported for bidiGenerateContent` in checkpoints 00–02:** microphone/audio mode was started with the text model. Start a new session and submit prompts with the text send button, or move to checkpoint 03 for voice.
- **Someone is behind:** move directly to the next completed checkpoint.

## Sources

- [ADK streaming quickstart](https://adk.dev/get-started/streaming/)
- [ADK Python streaming guide](https://adk.dev/live/get-started/streaming-python/)
- [Gemini Live API quickstart](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk)
- [Gemini 3.1 Flash Live model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview)
- [Latest Gemini text models](https://ai.google.dev/gemini-api/docs/latest-model)

`adk web` is a development and workshop UI, not a production deployment.
