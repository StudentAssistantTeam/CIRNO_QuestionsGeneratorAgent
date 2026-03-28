import json
from logging import getLogger
from pydantic import ValidationError
# adk dependencies
from google.adk.tools.tool_context import ToolContext
# project dependencies
from questions_features_analysis_agent.data_model import QuestionsFeaturesAnalysisAgentOutputSchema
from questions_setter_agent.data_model import QuestionsSetterAgentOutputSchema

# logger
logger = getLogger("util_tools")


def validate_result_features_analysis(converted_result: str) -> dict:
    """Validate the result converted to see whether it is a valid output schema and can be parsed as json.

    Args:
        converted_result (str): The result converted by you.

    Returns:
        dict: Whether validation is successful and the result of validation.
    """
    logger.info("Start validating the result for the storer subagent")
    try:
        json_result = json.loads(converted_result)
        try:
            QuestionsFeaturesAnalysisAgentOutputSchema.model_validate(json_result)
            return {
                "success": True,
                "result": "Validated successfully"
            }
        except ValidationError as err:
            return {
                "success": False,
                "result": f"""
The result converted by you is not correspond to the output schema of the analysis agent
, reason: {err}
                """
            }
    except json.JSONDecodeError:
        return {
            "success": False,
            "result": "The result converted by you is not a valid json"
        }


def validate_result_questions_generation(converted_result: str) -> dict:
    """Validate the result converted to see whether it is a valid output schema and can be parsed as json.

    Args:
        converted_result (str): The result converted by you.

    Returns:
        dict: Whether validation is successful and the result of validation.
    """
    logger.info("Start validating the result for the storer subagent")
    try:
        json_result = json.loads(converted_result)
        try:
            QuestionsSetterAgentOutputSchema.model_validate(json_result)
            return {
                "success": True,
                "result": "Validated successfully"
            }
        except ValidationError as err:
            return {
                "success": False,
                "result": f"""
The result converted by you is not correspond to the output schema of the analysis agent
, reason: {err}
                """
            }
    except json.JSONDecodeError:
        return {
            "success": False,
            "result": "The result converted by you is not a valid json"
        }


# exit loop
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}
