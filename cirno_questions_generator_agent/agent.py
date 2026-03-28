from logging import getLogger
# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import agent_tool
# project dependencies
from cirno_questions_generator_agent.config import settings
from cirno_questions_generator_agent.prompt import (
    router_agent_description
)
from cirno_questions_generator_agent.data_model import (
    RouterAgentInputSchema
)
from questions_features_analysis_agent.agent import create_analysis_sequential_agent
from questions_setter_agent.agent import create_questions_setter_agent
from utility.shared_info import ANALYSIS_KEY

logger = getLogger("Questions Setter Agent")


# --- Before Agent Callback ---
def update_initial_topic_state(callback_context: CallbackContext):
    callback_context.state[ANALYSIS_KEY] = callback_context.state.get(
        ANALYSIS_KEY,
        'No sample answer provided'
    )


# Agent
# Defining base llm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_base=settings.llm_base_url,
    api_key=settings.llm_api_key
)


# Defining base agent
def create_router_agent():
    # Creating agent tools
    analysis_agent = create_analysis_sequential_agent()
    analysis_agent_tool = agent_tool.AgentTool(analysis_agent)
    # return llm
    return LlmAgent(
        model=llm,
        name="questions_setter_router_agent",
        description=router_agent_description,
        input_schema=RouterAgentInputSchema,
        sub_agents=[
            create_questions_setter_agent()
        ],
        tools=[analysis_agent_tool],
        planner=PlanReActPlanner(),
        before_agent_callback=update_initial_topic_state
    )


root_agent = create_router_agent()
