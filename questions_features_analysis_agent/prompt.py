# Agent
# planner
questions_features_analysis_agent_planner_prompt = """
For each task, in planning process, you have to follow these steps in planning: 

---

<QUESTION_TYPE_AND_CONTEXT>
1. What is the question type? (MCQ / FRQ / other)
2. What subject area does it belong to? (e.g., mathematics, physics, literature, history)
3. What is the approximate grade level or difficulty band? (e.g., 9–10, 11–12)
4. Is there any special format (e.g., “select all that apply”, multi‑part, data‑driven)?
</QUESTION_TYPE_AND_CONTEXT>

<KNOWLEDGE_AND_SKILLS>
1. What are the core knowledge points required? (List the 1–3 most important topics/concepts.)
2. What secondary knowledge is implied? (Concepts that are not directly asked but needed for solution.)
3. Which cognitive skills are being assessed? (e.g., recall, application, analysis, evaluation – use Bloom’s taxonomy.)
4. Is the question targeting procedural fluency, conceptual understanding, or problem‑solving?
</KNOWLEDGE_AND_SKILLS>

<STRUCTURE_AND_COMPONENTS>
1. Break down the question into its logical components:
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
1. Estimate difficulty on a scale of 1 (very easy) to 5 (very hard). Consider:
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
1. Decide what kinds of sample questions will be most helpful for the generator:
   - **Standard example**: A direct analog of the original question (same concept, different numbers/context)
   - **Variation**: Change one parameter (e.g., reverse the question, add a constraint, change the representation)
   - **Edge / corner case**: A question that tests boundaries or special conditions
   - **Common‑mistake example**: A question that explicitly highlights a frequent error
2. For each type, specify:
   - How many samples to provide (typically 1–2 per type)
   - Any special instructions (e.g., “include a step‑by‑step solution”, “provide distractors that mirror common errors”)
3. If the question is FRQ, note whether the sample should include a rubric or scoring guidelines.
</SAMPLE_QUESTION_STRATEGY>
"""
