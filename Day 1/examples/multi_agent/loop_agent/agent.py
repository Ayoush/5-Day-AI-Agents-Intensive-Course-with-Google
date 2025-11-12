"""
Loop Agent Example: Iterative Story Refinement

This example demonstrates a LoopAgent that iteratively refines a story
through cycles of critique and revision until it's approved.

Based on Day 1b notebook patterns.
"""

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import FunctionTool

# Exit function: Called when the story is approved
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', 
    indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

# Initial Writer Agent: Runs ONCE at the beginning to create the first draft
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key="current_story",  # Stores the first draft in the state
)

# Critic Agent: Provides feedback or approval signal
critic_agent = Agent(
    name="CriticAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}
    
    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique",  # Stores the feedback in the state
)

# Refiner Agent: Refines the story based on critique OR calls exit_loop
refiner_agent = Agent(
    name="RefinerAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story",  # It overwrites the story with the new, refined version
    tools=[FunctionTool(exit_loop)],  # The tool allows the agent to exit the loop
)

# Loop Agent: Contains the agents that will run repeatedly: Critic -> Refiner
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3,  # Prevents infinite loops (adjust as needed)
)

# Sequential Agent: Defines the overall workflow
# Initial Write -> Refinement Loop
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)

