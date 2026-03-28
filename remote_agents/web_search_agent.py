# adk dependencies
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
# project dependencies
from remote_agents.config import settings


# Web search agent
def create_web_search_agent():
    return RemoteA2aAgent(
        name="web_search_agent",
        description="This agent can search in the internet or data commons to get the statistic or simple facts and return it in the answer to you.",
        agent_card=(
            f"{settings.web_search_agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        )
    )
