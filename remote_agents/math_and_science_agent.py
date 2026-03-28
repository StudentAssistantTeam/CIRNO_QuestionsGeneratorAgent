# adk dependencies
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
# project dependencies
from remote_agents.config import settings


# Science and math agent
def create_academics_agent():
    return RemoteA2aAgent(
        name="academics_agent",
        description="Expert in science, math, engineering, economics, history or geology",
        agent_card=(
            f"{settings.science_and_math_agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        )
    )
