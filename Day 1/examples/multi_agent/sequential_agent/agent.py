"""
Sequential Agent Example: Blog Post Creation Pipeline

This example demonstrates a SequentialAgent that creates a blog post through
a fixed pipeline: Outline → Write → Edit

Based on Day 1b notebook patterns.
"""

from google.adk.agents import Agent, SequentialAgent

# Step 1: Outline Agent - Creates the initial blog post outline
outline_agent = Agent(
    name="OutlineAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",  # The result will be stored in session state with this key
)

# Step 2: Writer Agent - Writes the full blog post based on the outline
writer_agent = Agent(
    name="WriterAgent",
    model="gemini-2.5-flash-lite",
    # The {blog_outline} placeholder automatically injects the state value from the previous agent's output
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",  # The result will be stored with this key
)

# Step 3: Editor Agent - Edits and polishes the draft
editor_agent = Agent(
    name="EditorAgent",
    model="gemini-2.5-flash-lite",
    # This agent receives the {blog_draft} from the writer agent's output
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, 
    improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",  # This is the final output of the entire pipeline
)

# Sequential Agent: Runs agents in the exact order listed
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)

