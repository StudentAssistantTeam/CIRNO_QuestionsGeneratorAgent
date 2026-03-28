# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
# project dependencies
from questions_setter_agent.config import settings
from questions_setter_agent.prompt import (
    questions_setter_agent_description,
    questions_setter_agent_instruction
)
from questions_setter_agent.data_model import (
    QuestionsSetterAgentOutputSchema, QuestionsSetterAgentInputSchema
)
from remote_agents.web_search_agent import web_search_agent
from remote_agents.math_and_science_agent import academics_agent

# Defining llm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_base=settings.llm_base_url,
    api_key=settings.llm_api_key
)
# Defining Agent
questions_setter_agent = LlmAgent(
    model=llm,
    name="questions_setter_agent",
    description=questions_setter_agent_description,
    instruction=questions_setter_agent_instruction,
    input_schema=QuestionsSetterAgentInputSchema,
    output_schema=QuestionsSetterAgentOutputSchema,
    sub_agents=[
        web_search_agent,
        academics_agent
    ],
    planner=PlanReActPlanner(),
)
