from logging import getLogger
# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
# project dependencies
from cirno_questions_generator_agent.config import settings
from cirno_questions_generator_agent.prompt import (
    router_agent_description
)
from cirno_questions_generator_agent.data_model import (
    RouterAgentInputSchema
)
from questions_features_analysis_agent.agent import questions_features_analysis_sequential_agent

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
            input_schema=RouterAgentInputSchema,
            sub_agents=[
                questions_features_analysis_sequential_agent
            ],
            planner=PlanReActPlanner()
        )
