from utility.shared_info import (
    ANALYSIS_RAW
)

# Analysis Agent
# planner
questions_features_analysis_agent_planner_prompt = """
For each task, in planning process, you have to follow these steps in planning: 

---

<QUESTION_TYPE_AND_CONTEXT>
1. What is the question type? (MCQ / FRQ / other)
2. What subject area does these questions belong to? (e.g., mathematics, physics, literature, history)
3. Are there any special formats (e.g., “select all that apply”, multi‑part, data‑driven)?
4. Are there any special attributes (e.g. the number of options for mcq questions, the word count for frq questions).
</QUESTION_TYPE_AND_CONTEXT>

<KNOWLEDGE_AND_SKILLS>
1. What are the core knowledge points required? (List the 1–3 most important topics/concepts.)
2. What secondary knowledge points are implied? (Concepts that are not directly asked but needed for solution.)
3. Which cognitive skills are being assessed? (e.g., recall, application, analysis, evaluation – use Bloom’s taxonomy.)
4. Are the questions targeting procedural fluency, conceptual understanding, or problem‑solving?
</KNOWLEDGE_AND_SKILLS>

<STRUCTURE_AND_COMPONENTS>
1. Break down the questions into their logical components:
   - For MCQ:  
     * Stem (background / scenario)  
     * Question stem (what is being asked)  
     * Options (correct answer + distractors)
   - For FRQ:  
     * Scenario / data / prompt  
     * Sub‑questions (if any)  
     * Expected response type (calculation, explanation, diagram, etc.)
2. Identify all given information, constraints, and the exact target to be found.
3. Note any special instructions (e.g., “show your work”, “use two methods”, “justify”).
</STRUCTURE_AND_COMPONENTS>

<DIFFICULTY_AND_COMMON_PITFALLS>
1. Estimate difficulty of these questions on a scale of 1 (very easy) to 5 (very hard). Consider:
   - Number of steps required
   - Depth of reasoning
   - Presence of misleading information
   - Need for synthesis across multiple topics
2. Predict common student mistakes or misconceptions that might lead to wrong answers.
   - For MCQ: What plausible distractors could be built from these mistakes?
   - For FRQ: Which steps are most error‑prone?
3. Identify any potential “traps” in the wording, data, or options.
</DIFFICULTY_AND_COMMON_PITFALLS>

<SAMPLE_QUESTION_STRATEGY>
1. Decide which questions will be most helpful for the generator:
   - **Standard example**: A direct analog of the original question (same concept, different numbers/context)
   - **Common‑mistake example**: A question that explicitly highlights a frequent error
2. For each type, specify:
   - How many samples to provide (typically 1–2 per type)
   - Any special instructions (e.g., “include a step‑by‑step solution”, “provide distractors that mirror common errors”)
3. If the question is FRQ, note whether the sample should include a rubric or scoring guidelines.
</SAMPLE_QUESTION_STRATEGY>
"""
# Description
questions_features_analysis_agent_description = """
The agent that is responsible for analyzing the features of the sample questions. 
The questions setter agent can use the result of executing this agent to help it generate questions. 
"""
# Instruction
questions_features_analysis_agent_instruction = """
You are responsible for analyzing the features of questions. 

You have to follow the following guidelines: 
1. Planning before getting the final answer. 
    You must follow the planning instructions. 
2. The planning must be detailed
2. Review your results. 
3. Analysis you made should be clear and logical. 
"""
# Converter Agent
# Description
converter_agent_description = """
This agent will convert the result from the analysis agent to the string that can be parsed to json to store in the state. 
"""
# Instruction
converter_agent_instruction = ("""
You are responsible for converting the result of analysis agent to string that can be converted to json and correspond to analysis agent output schema. 
1. You must not alter the result in the original answer. 
2. You must use your tool to check the result until the tool returns that the validation is successful. 

---

Result of analysis: 

"""
+ "{" + ANALYSIS_RAW + "}"
)
# Sequential agent
sequential_agent_description = """
This agent will analyse the question and process it in sequence. 
The questions setter agent can use the result of executing this agent to help it generate questions. 
"""
