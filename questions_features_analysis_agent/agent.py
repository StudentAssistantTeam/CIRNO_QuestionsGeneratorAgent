# adk dependencies
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
# project dependencies
from questions_features_analysis_agent.config import settings
from questions_features_analysis_agent.planner import FeaturesAnalysisAgentPlanner
from questions_features_analysis_agent.prompt import (
    questions_features_analysis_agent_description,
    questions_features_analysis_agent_instruction
)
from questions_features_analysis_agent.data_models import (
    QuestionsFeaturesAnalysisAgentInputSchema,
    QuestionsFeaturesAnalysisAgentOutputSchema
)

# Define litellm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_key=settings.llm_api_key,
    api_base=settings.llm_base_url
)
# Define agents
analysis_agent = LlmAgent(
    name="question_analysis_agent",
    model=llm,
    instruction=questions_features_analysis_agent_instruction,
    description=questions_features_analysis_agent_description,
    planner=FeaturesAnalysisAgentPlanner(),
    input_schema=QuestionsFeaturesAnalysisAgentInputSchema,
    output_schema=QuestionsFeaturesAnalysisAgentOutputSchema
)
