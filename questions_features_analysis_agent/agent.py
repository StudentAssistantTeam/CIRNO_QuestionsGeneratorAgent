# adk dependencies
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
# project dependencies
from questions_features_analysis_agent.config import settings

# Define litellm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_key=settings.llm_api_key,
    api_base=settings.llm_base_url
)
# Define agent
agent = LlmAgent(
    name="question_analysis_agent",
    model=llm
)
