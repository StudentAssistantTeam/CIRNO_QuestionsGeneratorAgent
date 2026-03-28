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


# Questions Data Structure
class Question(BaseModel):
    stem: str = Field(
        description="The main part of the question."
    )
    options: Optional[List[Option]] = Field(
        description="The options of this question if this question is a mcq."
    )
    answer: str = Field(
        description="The answer to the question. If this is a MCQ, type in the option identifier of the correct option."
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
    comment: str = Field(
        description="""
The comment of you to this question, including why you want to add this question. 
It can help the investigator agent understand why you want to make this question and why does it valuable. 
"""
    )
    core_knowledge_points: List[str] = Field(
        description="The directly mentioned knowledge points presented in this question"
    )
    secondary_knowledge_points: Optional[List[str]] = Field(
        description="The knowledge points that are not directly mentioned but needed to solve this question"
    )
    relative_material: Optional[str] = Field(
        description="The reading material, only type in if the question is based on one material (e.g. the reading passage)."
    )


# output schema
class QuestionsSetterAgentOutputSchema(BaseModel):
    questions: List[Question] = Field(
        description="The questions that are made by you"
    )


# Startup schema
class StartupSchema(BaseModel):
    question_numbers: int = Field(
        description="The number of questions that is going to be generated"
    )
    topic: str = Field(
        description="The topic of the questions that is going to be generated"
    ),
    difficulty_description: str = Field(
        description=
        """
        describe the difficulty of the question that will be generated 
        (e.g. the question should be suitable for high school students)
        """
    )


# Final ver Questions Data Structure
class FinalQuestion(BaseModel):
    stem: str = Field(
        description="The main part of the question."
    )
    options: Optional[List[Option]] = Field(
        description="The options of this question if this question is a mcq."
    )
    answer: str = Field(
        description="The answer to the question. If this is a MCQ, type in the option identifier of the correct option."
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


# Final question output schema
class FinalQuestionOutputSchema(BaseModel):
    question_numbers: List[FinalQuestion] = Field(
        description="The final version of the questions to be provided to user."
    )
