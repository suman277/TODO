from google.adk.agents import Agent
from .agent_tools import agent_tools
from .get_model import get_model
from agents.instructions import ROOT_AGENT_INSTRUCTION
root_agent = Agent(
    name="weather_time_agent",
    model=get_model(),
    description=(
        "Agent to Perform CRUD Operations related to Todo ."
    ),
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=agent_tools,
)