# Facilitator runbook

## Recommended 55-minute flow

| Time | Mode | Folder | Goal |
|---|---|---|---|
| 0–5 | I show | `03_voice` | Finished demo; interrupt it |
| 5–9 | You do | setup | Everyone reaches `READY` |
| 9–16 | Together | `00_start` → `01_basic` | Edit and test the instruction |
| 16–24 | Together | `02_tool` | Add and inspect a tool call |
| 24–34 | You do | `03_voice` | Speak, pause, correct, interrupt |
| 34–40 | I show | `05_custom_streaming` | Explain queue + concurrent loops |
| 40–46 | I show | `04_slow_failure` | Slow and failing tool |
| 46–53 | You do | any | Mini challenge |
| 53–55 | Together | wrap | One production takeaway |

For a 60-minute session, use minutes 55–60 to compare the servers in
`05_custom_streaming` and `06_production`. Highlight origin and payload checks,
session resumption, context compression, call budgets, safe logs, and cleanup.
Emphasize that production behavior comes from system controls, not prompt wording.

## Demo prompts

- “Find a room tomorrow afternoon.”
- Interrupt: “Actually—make it after three.”
- “Book it.” (The agent should clarify that this demo only finds rooms.)
- Failure demo: “Find a room after one p.m.”

Checkpoints 00–02 use `gemini-3.6-flash` through ADK Web's text/SSE path. Ask
participants not to start microphone/audio mode there: it opens `/run_live`,
which a text-only model cannot use. Checkpoint 03 switches to
`gemini-3.1-flash-live-preview` and introduces the microphone and native audio.

For checkpoint 04, “after one p.m.” means 13:00 and intentionally returns a
structured failure after five seconds. The agent should acknowledge the wait,
apologize briefly, and offer another time without exposing an exception or
retrying automatically.

## Key distribution

The safest option is participant-owned AI Studio keys. If sharing one workshop key:

1. Create a dedicated key immediately before the workshop.
2. Restrict the project quota to an amount you are comfortable spending.
3. Share it through a private attendee channel, never the repository.
4. Have participants place it only in `.env`.
5. Delete or rotate the key immediately after the workshop.

## 45-minute fallback

Skip live-coding the custom WebSocket server. Show its four highlighted functions and keep the voice exercise and slow-tool demo.
