"""
Parallel Agent Example: Multi-Topic Research System

This example demonstrates a ParallelAgent that runs multiple independent
research tasks concurrently, then aggregates the results.

Based on Day 1b notebook patterns.
"""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# Parallel Agents: These run simultaneously
# Tech Researcher: Focuses on AI and ML trends
tech_researcher = Agent(
    name="TechResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
    the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key="tech_research",  # The result will be stored in session state with this key
)

# Health Researcher: Focuses on medical breakthroughs
health_researcher = Agent(
    name="HealthResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
    their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="health_research",  # The result will be stored with this key
)

# Finance Researcher: Focuses on fintech trends
finance_researcher = Agent(
    name="FinanceResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research current fintech trends. Include 3 key trends,
    their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="finance_research",  # The result will be stored with this key
)

# Aggregator Agent: Runs AFTER the parallel step to synthesize the results
aggregator_agent = Agent(
    name="AggregatorAgent",
    model="gemini-2.5-flash-lite",
    # It uses placeholders to inject the outputs from the parallel agents
    instruction="""Combine these three research findings into a single executive summary:

    **Technology Trends:**
    {tech_research}
    
    **Health Breakthroughs:**
    {health_research}
    
    **Finance Innovations:**
    {finance_research}
    
    Your summary should highlight common themes, surprising connections, and the most important 
    key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary",  # This will be the final output of the entire system
)

# Parallel Agent: Runs all its sub-agents simultaneously
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher],
)

# Sequential Agent: Defines the high-level workflow
# First run the parallel team, then run the aggregator
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)

