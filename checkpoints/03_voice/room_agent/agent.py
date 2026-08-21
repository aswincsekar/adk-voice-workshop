from google.adk.agents import Agent

from adk_voice_workshop.config import live_model
from adk_voice_workshop.room_tools import find_rooms

root_agent = Agent(
    name="room_agent",
    model=live_model(),
    instruction=(
        "You are a concise voice assistant for finding meeting rooms. Ask only one question "
        "at a time. Use find_rooms after you know the time and capacity. If the speaker "
        "corrects themselves, use the newest information. Never claim to book a room."
    ),
    tools=[find_rooms],
)

