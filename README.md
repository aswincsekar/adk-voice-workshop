# Building Voice Agents with Google ADK

A guided Python workshop that goes from a tiny text agent to a real-time voice agent with tools, interruption, transcription, and failure handling.

## Workshop slides

- [PowerPoint deck](slides/google-adk-voice-agents-workshop.pptx) — downloadable/offline copy kept with the code
- [Live Google Slides](https://docs.google.com/presentation/d/1n0RPi-yYbqH_e_r23KlJAldgGFxdpRez7lVCUqkLLc0/edit) — presentation version for the workshop

## What participants build

1. A basic ADK agent
2. A room-finding function tool
3. A voice agent in the ADK development UI
4. A slow/failing tool experiment
5. An optional FastAPI + WebSocket streaming app

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
✓ Python
✓ Dependencies
✓ API key configuration
✓ Workshop checkpoints
READY
```

## Run a checkpoint

Text agent:

```bash
cd checkpoints/01_basic
uv run adk web
```

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

## Workshop map

| Folder | Moment | What changes |
|---|---|---|
| `00_start` | Start here | Minimal agent; edit the instruction |
| `01_basic` | Basic agent | Clear room-assistant behavior |
| `02_tool` | Add a tool | Agent can call `find_rooms` |
| `03_voice` | Enable voice | Switch to a Live API model |
| `04_slow_failure` | Break it | Slow tool, timeout, and failure experiment |
| `05_custom_streaming` | Look underneath | `run_live`, `LiveRequestQueue`, WebSocket, audio, events, transcription |

## Run the custom streaming app

This is the optional advanced checkpoint:

```bash
cd checkpoints/05_custom_streaming
uv run uvicorn server:app --reload --port 8001
```

Open [http://localhost:8001](http://localhost:8001), click **Connect microphone**, and use headphones.

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
- **Someone is behind:** move directly to the next completed checkpoint.

## Sources

- [ADK streaming quickstart](https://adk.dev/get-started/streaming/)
- [ADK Python streaming guide](https://adk.dev/live/get-started/streaming-python/)
- [Gemini Live API quickstart](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk)
- [Gemini 3.1 Flash Live model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview)
- [Latest Gemini text models](https://ai.google.dev/gemini-api/docs/latest-model)

`adk web` is a development and workshop UI, not a production deployment.
