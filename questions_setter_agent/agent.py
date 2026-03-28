# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
# project dependencies
from questions_setter_agent.config import settings
from questions_setter_agent.prompt import (
    questions_setter_agent_description,
    questions_setter_agent_instruction,
    generator_converter_instruction
)
from questions_setter_agent.data_model import (
    QuestionsSetterAgentOutputSchema,
    StartupSchema
)
from remote_agents.web_search_agent import web_search_agent
from remote_agents.math_and_science_agent import academics_agent
from utility.shared_info import QUESTIONS_KEY
from tools.util_tools import validate_result_questions_generation

# Defining llm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_base=settings.llm_base_url,
    api_key=settings.llm_api_key
)
# Defining Agent
# Converter Agent
generator_converter_agent = LlmAgent(
    model=llm,
    name="generator_converter_agent",
    instruction=generator_converter_instruction,
    input_schema=QuestionsSetterAgentOutputSchema,
    output_key=QUESTIONS_KEY,
    tools=[
        validate_result_questions_generation
    ]
)
# Questions generator
questions_generator_agent = LlmAgent(
    model=llm,
    name="questions_generator_agent",
    description=questions_setter_agent_description,
    instruction=questions_setter_agent_instruction,
    input_schema=StartupSchema,
    sub_agents=[
        web_search_agent,
        academics_agent,
        generator_converter_agent
    ],
    planner=PlanReActPlanner(),
)
# Investigator Agent
investigator_agent = LlmAgent(
    model=llm,
    name="investigator_agent",
)
