from google.adk.agents import Agent

from adk_voice_workshop.config import live_model
from adk_voice_workshop.room_tools import slow_find_rooms

root_agent = Agent(
    name="room_agent",
    model=live_model(),
    instruction=(
        "You are a concise voice assistant. Before calling slow_find_rooms, briefly tell the "
        "user that you are checking. If its result has status error, apologize without exposing "
        "technical details and offer to try another time. Do not retry automatically. Never "
        "claim to book a room."
    ),
    tools=[slow_find_rooms],
)
