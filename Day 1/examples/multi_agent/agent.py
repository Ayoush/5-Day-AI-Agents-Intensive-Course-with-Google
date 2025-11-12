from google.adk.agents import Agent
from google.adk.tools import AgentTool

# Code Quality Agent - Analyzes code quality and best practices
code_quality_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='code_quality_agent',
    description='An agent that analyzes code quality, style, and best practices.',
    instruction='''You are a code quality expert. When asked to analyze code quality:
- Provide feedback on code style, readability, and organization
- Check for PEP 8 compliance
- Identify error handling patterns
- Suggest improvements for best practices
- Be specific and actionable in your feedback

Always provide a clear, detailed response with your analysis.''',
    output_key='code_quality_feedback'
)

# Architecture Agent - Analyzes system architecture
architecture_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='architecture_agent',
    description='An agent that analyzes system architecture and design patterns.',
    instruction='''You are an architecture expert. When asked to analyze architecture:
- Evaluate module organization and structure
- Identify design patterns used
- Assess separation of concerns
- Analyze dependencies between components
- Suggest architectural improvements

Always provide a clear, detailed response with your analysis.''',
    output_key='architecture_feedback'
)

# Performance Agent - Analyzes performance aspects
performance_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='performance_agent',
    description='An agent that analyzes code performance and optimization opportunities.',
    instruction='''You are a performance expert. When asked to analyze performance:
- Identify potential bottlenecks
- Evaluate data structures and algorithms
- Assess I/O operations
- Suggest performance optimizations
- Consider memory usage patterns

Always provide a clear, detailed response with your analysis.''',
    output_key='performance_feedback'
)

# Root Coordinator Agent - Orchestrates the other agents
root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='coordinator_agent',
    description='A coordinator agent that orchestrates code analysis by delegating to specialized agents.',
    instruction='''You are a coordinator agent that manages a team of specialized code analysis agents.

When asked to analyze a codebase or project:

1. First, call code_quality_agent to analyze code quality
2. Then, call architecture_agent to review the architecture  
3. Next, call performance_agent to evaluate performance

After all agents complete their analysis, provide a comprehensive summary that:
- Combines findings from all three agents
- Highlights the most important insights
- Provides actionable recommendations
- Organizes the information clearly

Make sure to wait for each agent to complete before calling the next one.''',
    tools=[
        AgentTool(code_quality_agent),
        AgentTool(architecture_agent),
        AgentTool(performance_agent)
    ]
)
