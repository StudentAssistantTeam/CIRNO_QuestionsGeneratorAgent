import json
from logging import getLogger
from pydantic import ValidationError
# project dependencies
from questions_features_analysis_agent.data_models import QuestionsFeaturesAnalysisAgentOutputSchema

# logger
logger = getLogger("util_tools")


def validate_result(converted_result: str) -> dict:
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
