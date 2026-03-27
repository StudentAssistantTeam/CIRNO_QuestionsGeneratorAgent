from pydantic import BaseModel, Field
from typing import Optional, List

# Router agent input schema
class RouterAgentInputSchema(BaseModel):
    topic: str = Field(
        description="Topic of the question that will be generated"
    )
    has_sample_questions: bool = Field(
        description="Whether or not questions would be included"
    )
    sample_questions: Optional[List[str]] = Field(
        description="The sample questions that show the style of the question generated"
    )
