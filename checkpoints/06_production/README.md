# Checkpoint 06: harden the streaming web app

This checkpoint extends the FastAPI/WebSocket application from checkpoint 05.
It reuses the same browser UI so participants can compare server behavior
without learning another interface.

## Run it

```bash
cd checkpoints/06_production
uv run uvicorn server:app --reload --port 8002
```

Open [http://localhost:8002](http://localhost:8002), connect the microphone,
ask for a room, and interrupt the response.

## Improvements implemented here

- **Origin allowlist:** reject browser WebSockets from unexpected sites.
- **Message and audio limits:** bound JSON and decoded PCM chunk sizes.
- **Strict message parsing:** reject malformed JSON, Base64, MIME types, and event types.
- **Concurrency limit:** refuse excess sessions instead of exhausting Live API quota.
- **Session resumption:** request Gemini API resumption handles for reconnecting live sessions.
- **Context compression:** keep long sessions within a bounded context window.
- **Call budget:** cap model calls per session and bound the tool worker pool.
- **Privacy-aware logs:** log connection IDs and outcomes, not transcript content.
- **Safe errors:** give users a short reference ID while retaining server diagnostics.
- **Deterministic cleanup:** close the queue and cancel both streaming tasks on every exit.

Configuration is explicit and can be supplied through environment variables:

```text
WS_ALLOWED_ORIGINS=http://localhost:8002,http://127.0.0.1:8002
MAX_WS_MESSAGE_BYTES=32768
MAX_AUDIO_CHUNK_BYTES=16384
MAX_ACTIVE_SESSIONS=20
LOG_LEVEL=INFO
```

## Still required for real production

- Authenticate users and authorize every business action.
- Replace in-memory sessions with durable storage and define retention policies.
- Add timeouts, bounded retries, circuit breakers, and idempotency to external tools.
- Put the service behind TLS, a trusted reverse proxy, rate limits, and abuse controls.
- Export OpenTelemetry metrics and traces; alert on latency, errors, and interruption failures.
- Make transcript storage opt-in, redact sensitive data, and encrypt retained content.
- Replace the deprecated browser `ScriptProcessor` with an `AudioWorklet`.
- Load-test WebSocket fan-out, audio backpressure, reconnects, and provider quotas.
- Add conversation evals for corrections, failures, tool use, and adversarial requests.
- Keep API keys in managed server-side secrets; never expose them to browser JavaScript.

This remains a production-shaped teaching example. It is not an authenticated,
durable, internet-facing deployment.

It uses standard session resumption because the workshop authenticates with a
Gemini API key. In ADK, `SessionResumptionConfig(transparent=True)` is supported
only by the Vertex AI backend.
