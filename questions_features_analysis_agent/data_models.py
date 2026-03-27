from pydantic import BaseModel, Field
from typing import List

# Agent input schema
class QuestionsFeaturesAnalysisAgent(BaseModel):
    sample_questions: List[str] = Field(
        description="The sample questions provided to you to analyse the features"
    )
