from google.adk.agents import Agent

from adk_voice_workshop.config import live_model

root_agent = Agent(
    name="room_agent",
    model=live_model(),
    instruction=(
        "You help people find meeting rooms. Ask exactly one short follow-up question "
        "when the date, time, or capacity is missing. Do not claim a room is booked. "
        "Keep every response under three sentences."
    ),
)
