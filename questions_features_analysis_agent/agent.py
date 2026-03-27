# adk dependencies
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import PlanReActPlanner
from google.adk.agents.sequential_agent import SequentialAgent
# project dependencies
from questions_features_analysis_agent.config import settings
from questions_features_analysis_agent.planner import FeaturesAnalysisAgentPlanner
from questions_features_analysis_agent.prompt import (
    questions_features_analysis_agent_description,
    questions_features_analysis_agent_instruction,
    converter_agent_description,
    converter_agent_instruction
)
from questions_features_analysis_agent.data_models import (
    QuestionsFeaturesAnalysisAgentInputSchema,
    QuestionsFeaturesAnalysisAgentOutputSchema
)
from tools.util_tools import validate_result
from utility.shared_info import (
    ANALYSIS_KEY
)

# Define litellm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_key=settings.llm_api_key,
    api_base=settings.llm_base_url
)
# Define agents
# Analysis agent
analysis_agent = LlmAgent(
    name="analysis_agent",
    model=llm,
    instruction=questions_features_analysis_agent_instruction,
    description=questions_features_analysis_agent_description,
    planner=FeaturesAnalysisAgentPlanner(),
    input_schema=QuestionsFeaturesAnalysisAgentInputSchema,
    output_schema=QuestionsFeaturesAnalysisAgentOutputSchema
)
# Converter agent
analysis_result_converter_agent = LlmAgent(
    name="analysis_result_converter_agent",
    model=llm,
    description=converter_agent_description,
    instruction=converter_agent_instruction,
    planner=PlanReActPlanner(),
    input_schema=QuestionsFeaturesAnalysisAgentOutputSchema,
    output_key=ANALYSIS_KEY,
    tools=[
        validate_result
    ]
)
# Final agent
questions_features_analysis_sequential_agent = SequentialAgent(
    name="questions_features_analysis_sequential_agent",
    description="Analyse the sample questions and store it into the state so that the validation result can be viewed by everyone",
    sub_agents=[
        analysis_agent,
        analysis_result_converter_agent
    ]
)
