# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
# project dependencies
from questions_setter_agent.config import settings
from questions_setter_agent.prompt import agent_description

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
    description=agent_description
)
