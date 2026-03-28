# adk dependencies
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import PlanReActPlanner
# project dependencies
from questions_features_analysis_agent.config import settings
from questions_features_analysis_agent.planner import FeaturesAnalysisAgentPlanner
from questions_features_analysis_agent.prompt import (
    questions_features_analysis_agent_description,
    questions_features_analysis_agent_instruction,
    converter_agent_description,
    converter_agent_instruction
)
from questions_features_analysis_agent.data_model import (
    QuestionsFeaturesAnalysisAgentInputSchema,
    QuestionsFeaturesAnalysisAgentOutputSchema
)
from tools.util_tools import validate_result_questions_generation
from utility.shared_info import (
    ANALYSIS_KEY,
    ANALYSIS_RAW
)

# Define litellm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_key=settings.llm_api_key,
    api_base=settings.llm_base_url
)


# Define agents
# Converter agent
def create_analysis_result_converter_agent():
    return LlmAgent(
        name="analysis_result_converter_agent",
        model=llm,
        description=converter_agent_description,
        instruction=converter_agent_instruction,
        planner=PlanReActPlanner(),
        input_schema=QuestionsFeaturesAnalysisAgentOutputSchema,
        output_key=ANALYSIS_KEY,
        tools=[
            validate_result_questions_generation
        ]
    )
# Analysis agent
def create_analysis_agent():
    return LlmAgent(
        name="analysis_agent",
        model=llm,
        instruction=questions_features_analysis_agent_instruction,
        description=questions_features_analysis_agent_description,
        planner=FeaturesAnalysisAgentPlanner(),
        input_schema=QuestionsFeaturesAnalysisAgentInputSchema,
        output_key=ANALYSIS_RAW
    )
