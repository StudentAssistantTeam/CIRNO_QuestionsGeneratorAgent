from pydantic import BaseModel, Field
from typing import Optional, List


# Options Data structure
class Option(BaseModel):
    option_identifier: str = Field(
        description="The identifier of the option (e.g. the 'A' in 'A. George Washington'). "
    )
    option_description: str = Field(
        description="The text content of the option (e.g. the 'George Washington' in 'A. George Washington')"
    )
    is_correct: bool = Field(
        description="Whether this option is correct"
    )


# Questions Data Structure
class Question(BaseModel):
    stem: str = Field(
        description="The main part of the question."
    )
    options: Optional[List[Option]] = Field(
        description="The options of this question if this question is a mcq."
    )
    answer: Optional[str] = Field(
        description="The answer of the free_response question."
    )
    objective: List[str] = Field(
        description="""
The objectives of the question.
Each objective should be one of the three objectives: 
1. Procedural Fluency: Making the student able to solve problems using knowledge smoothly. 
2. Conceptual Understanding: Making the student able to understand 'why' behind the concepts. 
3. Real-world Application: Making the student able to apply the knowledge to real world circumstances. 
"""
    )
    reason: str = Field(
        description="The reason why this answer is the answer of the question."
    )
    core_knowledge_points: List[str] = Field(
        description="The directly mentioned knowledge points presented in this question"
    )
    secondary_knowledge_points: Optional[List[str]] = Field(
        description="The knowledge points that are not directly mentioned but needed to solve this question"
    )
    relative_material: Optional[str] = Field(
        description="The reading material, only type in if the questions is based on one material (e.g. the reading passage)."
    )


# Router agent input schema
class RouterAgentInputSchema(BaseModel):
    topic: str = Field(
        description="Topic of the question that will be generated"
    )
    has_sample_questions: bool = Field(
        description="Whether or not questions would be included"
    )
    sample_questions: Optional[List[Question]] = Field(
        description="The sample questions that show the style of the question generated"
    )
    questions_number: int = Field(
        description="The number of questions that will be generated"
    )
    difficulty_description: str = Field(
        description=
"""
describe the difficulty of the question that will be generated 
(e.g. the question should be suitable for high school students)
"""
    )
