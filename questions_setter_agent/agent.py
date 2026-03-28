# adk dependencies
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import (
    LlmAgent,
    LoopAgent,
    SequentialAgent
)
from google.adk.planners import PlanReActPlanner
# project dependencies
from questions_setter_agent.config import settings
from questions_setter_agent.prompt import (
    questions_setter_agent_description,
    questions_setter_agent_instruction,
    generator_converter_instruction,
    generator_converter_description,
    investigator_instruction,
    investigator_description,
    refractor_description,
    refractor_instruction,
    checking_agent_description,
    main_agent_description,
    questions_ordering_agent_description,
    questions_ordering_agent_instruction
)
from questions_setter_agent.data_model import (
    QuestionsSetterAgentOutputSchema,
    StartupSchema,
    FinalQuestionOutputSchema
)
from remote_agents.web_search_agent import create_web_search_agent
from remote_agents.math_and_science_agent import create_academics_agent
from utility.shared_info import (
    QUESTIONS_KEY,
    ERRORS_KEY
)
from tools.util_tools import (
    validate_result_questions_generation,
    exit_loop
)

# Defining llm
llm = LiteLlm(
    model=settings.llm_model_name,
    api_base=settings.llm_base_url,
    api_key=settings.llm_api_key
)


# Defining Agent
# Converter Agent
def create_generator_converter_agent():
    return LlmAgent(
        model=llm,
        name="generator_converter_agent",
        description=generator_converter_description,
        instruction=generator_converter_instruction,
        input_schema=QuestionsSetterAgentOutputSchema,
        output_key=QUESTIONS_KEY,
        tools=[
            validate_result_questions_generation
        ]
    )


# Questions generator
def create_questions_generator_agent():
    return LlmAgent(
        model=llm,
        name="questions_generator_agent",
        description=questions_setter_agent_description,
        instruction=questions_setter_agent_instruction,
        input_schema=StartupSchema,
        sub_agents=[
            create_web_search_agent(),
            create_academics_agent(),
            create_generator_converter_agent()
        ],
        planner=PlanReActPlanner(),
    )


# Investigator Agent
def create_investigator_agent():
    return LlmAgent(
        model=llm,
        name="investigator_agent",
        instruction=investigator_instruction,
        description=investigator_description,
        planner=PlanReActPlanner(),
        output_key=ERRORS_KEY,
        sub_agents=[
            create_web_search_agent(),
            create_academics_agent(),
        ],
        tools=[
            exit_loop
        ]
    )


# Refractor Agent
def create_refractor_agent():
    return LlmAgent(
        model=llm,
        name="refractor_agent",
        description=refractor_description,
        instruction=refractor_instruction,
        planner=PlanReActPlanner(),
        output_key=QUESTIONS_KEY,
        tools=[
            validate_result_questions_generation
        ]
    )


# Questions ordering agen
def create_questions_ordering_agent():
    return LlmAgent(
        model=llm,
        name="questions_ordering_agent",
        description=questions_ordering_agent_description,
        instruction=questions_ordering_agent_instruction,
        output_schema=FinalQuestionOutputSchema
    )


# Continuous checking
def create_checking_agent():
    return LoopAgent(
        name="checking_agent",
        description=checking_agent_description,
        sub_agents=[
            create_investigator_agent(),
            create_refractor_agent()
        ],
        max_iterations=5
    )


# Sequential agent
def create_questions_setter_agent():
    return SequentialAgent(
        name="questions_setter_agent",
        description=main_agent_description,
        sub_agents=[
            create_questions_generator_agent(),
            create_checking_agent,
            create_questions_ordering_agent()
        ]
    )
