# Multi-Agent System Examples

This folder contains examples of different multi-agent workflow patterns from Day 1b.

Each example is a complete ADK project with its own folder containing:
- `agent.py` - The agent definitions
- `__init__.py` - Package initialization
- `.env` - Environment configuration

## Examples

### 1. Sequential Agent (`sequential_agent/`)
**Pattern:** Fixed Pipeline / Assembly Line

**Use Case:** When tasks must run in a specific order, where each step builds on the previous one.

**Example:** Blog Post Creation Pipeline
- Outline Agent → Writer Agent → Editor Agent
- Each agent's output becomes the input for the next

**To run:**
```python
from sequential_agent import agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent.root_agent)
response = await runner.run_debug("Write a blog post about the benefits of Python programming")
```

Or use ADK web:
```bash
cd sequential_agent
adk web
```

---

### 2. Parallel Agent (`parallel_agent/`)
**Pattern:** Concurrent Execution

**Use Case:** When you have independent tasks that can run simultaneously to speed up the workflow.

**Example:** Multi-Topic Research System
- Tech Researcher, Health Researcher, Finance Researcher (run in parallel)
- Aggregator Agent (combines results after parallel execution)

**To run:**
```python
from parallel_agent import agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent.root_agent)
response = await runner.run_debug("Run the daily executive briefing on Tech, Health, and Finance")
```

Or use ADK web:
```bash
cd parallel_agent
adk web
```

---

### 3. Loop Agent (`loop_agent/`)
**Pattern:** Iterative Refinement

**Use Case:** When you need to repeatedly improve output through cycles of feedback and revision.

**Example:** Story Refinement System
- Initial Writer Agent (creates first draft)
- Loop: Critic Agent → Refiner Agent (repeats until approved)
- Exits when critic says "APPROVED"

**To run:**
```python
from loop_agent import agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent.root_agent)
response = await runner.run_debug("Write a short story about a robot learning to paint")
```

Or use ADK web:
```bash
cd loop_agent
adk web
```

---

## Main Agent (`agent.py`)

The main `agent.py` file contains a simple coordinator pattern using `AgentTool`:
- Code Quality Agent
- Architecture Agent  
- Performance Agent
- Coordinator Agent (orchestrates the others)

This demonstrates the LLM-based orchestration pattern where an agent decides which sub-agents to call.

---

## Key Concepts

### Output Keys
Agents use `output_key` to store their results in session state. Other agents can reference these values using `{output_key}` placeholders in their instructions.

### AgentTool vs Workflow Agents
- **AgentTool**: Wraps an agent as a tool for another agent (LLM decides when to call it)
- **SequentialAgent**: Guaranteed order, deterministic execution
- **ParallelAgent**: Concurrent execution for independent tasks
- **LoopAgent**: Iterative cycles with exit conditions

---

## When to Use Which Pattern?

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Sequential** | Order matters, linear pipeline | Outline → Write → Edit |
| **Parallel** | Independent tasks, speed matters | Research 3 topics simultaneously |
| **Loop** | Iterative improvement needed | Write → Critique → Refine (repeat) |
| **AgentTool** | Dynamic decisions needed | LLM decides which agents to call |

