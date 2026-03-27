from logging import getLogger
# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
# project dependencies
from cirno_questions_generator_agent.config import settings
from cirno_questions_generator_agent.prompt import (
    router_agent_description
)
from cirno_questions_generator_agent.data_model import (
    RouterAgentInputSchema
)

logger = getLogger("Questions Setter Agent")


# Agent
class agent:
    def __init__(self):
        # Defining base llm
        self.llm = LiteLlm(
            model=settings.llm_model_name,
            api_base=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        # Defining base agent
        self.router_agent = LlmAgent(
            model=self.llm,
            name="questions_setter_router_agent",
            description=router_agent_description,
            input_schema=RouterAgentInputSchema
        )
