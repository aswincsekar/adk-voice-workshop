from google.adk.agents import Agent

from adk_voice_workshop.config import text_model
from adk_voice_workshop.room_tools import find_rooms

root_agent = Agent(
    name="room_agent",
    model=text_model(),
    instruction=(
        "You help people find meeting rooms. Ask for missing time or capacity, then use "
        "find_rooms. Read times naturally. This demo finds rooms but never books them. "
        "Keep responses short."
    ),
    tools=[find_rooms],
)

