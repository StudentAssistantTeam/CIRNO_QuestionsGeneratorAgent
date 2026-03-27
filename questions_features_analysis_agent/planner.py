from typing import Optional, List
# Adk dependencies
from google.adk.planners import BasePlanner
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.models.llm_request import LlmRequest
from google.genai import types
# Project dependencies
from questions_features_analysis_agent.prompt import (
    questions_features_analysis_agent_planner_prompt
)


# Custom planner
class FeaturesAnalysisAgentPlanner(BasePlanner):
    # planner instruction
    def build_planning_instruction(
            self,
            readonly_context: ReadonlyContext,
            llm_request: LlmRequest,
    ) -> Optional[str]:
        return questions_features_analysis_agent_planner_prompt

    # Return responses
    def process_planning_response(
            self,
            callback_context: CallbackContext,
            response_parts: List[types.Part],
    ) -> Optional[List[types.Part]]:
        return response_parts
