from pydantic import BaseModel, Field
from typing import List, Optional


# Option
class Option(BaseModel):
    option_identifier: str = Field(
        description="The identifier of the option (e.g. the 'A' in 'A. George Washington'). "
    )
    option_description: str = Field(
        description="The text content of the option (e.g. the 'George Washington' in 'A. George Washington')"
    )


# Question
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
    comment: str = Field(
        description="Your comment on this question and why do you want to choose this question as an example."
    )
    core_knowledge_points: List[str] = Field(
        description="The directly mentioned knowledge points presented in this question"
    )
    secondary_knowledge_points: Optional[List[str]] = Field(
        description="The knowledge points that are not directly mentioned but needed to solve this question"
    )


# Agent input schema
class QuestionsFeaturesAnalysisAgentInputSchema(BaseModel):
    sample_questions: List[Question] = Field(
        description="The sample questions provided to you to analyse the features"
    )


# Basic Metadata
class QuestionsMetadata(BaseModel):
    question_type: str = Field(
        description="The type of sample questions (e.g. multiple-choice/free-response/fill-in-the-blank)"
    )
    subject_area: str = Field(
        description="The subject area (e.g. mathematics, physics, etc.)"
    )
    reading_material: Optional[str] = Field(
        description="The reading material, only type in if the questions are all based on one passage."
    )
    special_formats: List[str] = Field(
        description="""
Descriptions of different kinds of special formats of questions appear in sample questions.
Describe these special formats (e.g. more than one answer choice is valid, etc.). 
        """
    )
    special_attributes: List[str] = Field(
        description="""
Descriptions of different special attributes of questions appear in sample questions. 
Describe these special attributes (e.g. 5 options for each question, 250 minimum word count each question, An article needed, etc.)
        """
    )


# Cognitive skill
class CognitiveSkill(BaseModel):
    name: str = Field(
        description="""
The name of the cognitive skill (Based on cognitive domain of Bloom's Taxonomy). 
This name can only be one of the following cognitive skills: 
- Remembering
    Definition: Require recalling facts or basic concepts. 
- Understanding
    Definition: Require understanding of ideas or concepts. 
- Applying
    Definition: Require using information and knowledge in new situations. 
- Analyzing
    Definition: Require breaking information into parts to explore understanding or relationship. 
- Evaluating
    Definition: Require justifying a decision or course of action. 
- Creating
    Definition: Require producing new or original work.
        """
    )
    question: Question = Field(
        description="A typical question that requires this cognitive skill."
    )


# Traps
class Trap(BaseModel):
    description: str = Field(
        description="Description of how this kind of trap would make the student struggle with it."
    )
    question: Question = Field(
        description="A typical question that contain this trap."
    )


# Knowledge and skills required
class QuestionsKnowledgeAndSkill(BaseModel):
    cognitive_skill_assessed: List[CognitiveSkill] = Field(
        description="The cognitive skills required to solve these questions."
    )
    traps: List[Trap] = Field(
        description="The traps appeared in these questions."
    )


# Example Questions
class ExampleQuestions(BaseModel):
    basic_examples: List[Question] = Field(
        description="A list of basic example questions that can represent the normal questions of these questions."
    )
    common_mistake_examples: List[Question] = Field(
        description="A list of example questions that contain errors that can be frequent for high school students. "
    )


# Output schema
class QuestionsFeaturesAnalysisAgentOutputSchema(BaseModel):
    questions_type_and_content: QuestionsMetadata = Field(
        description="The type and content of the questions."
    )
    knowledge_and_skills: QuestionsKnowledgeAndSkill = Field(
        description="The knowledge and skills assessed by the questions."
    )
    example_questions: List[ExampleQuestions] = Field(
        description="A list of example questions that can be useful for the question generation. "
    )
