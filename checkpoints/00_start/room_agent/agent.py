from google.adk.agents import Agent

from adk_voice_workshop.config import text_model

root_agent = Agent(
    name="room_agent",
    model=text_model(),
    # YOU DO: make the agent ask exactly one follow-up question.
    instruction="You help people find meeting rooms. Keep answers short.",
)

