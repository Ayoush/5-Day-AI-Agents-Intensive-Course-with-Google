<!-- de5f110c-ebdb-4ad3-bb99-acd8a5ca395b 7b7aa70d-abf5-47a4-8e83-75faecf5d2db -->
# Travel Agent with Custom MCP Server - Learning Project

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Jupyter Notebook                        │
│  ┌────────────────────────────────────────────────┐    │
│  │         Travel Planning Agent (ADK)             │    │
│  │  - Custom function tools (budget calc, etc)     │    │
│  │  - MCP Toolset → Your Custom Server             │    │
│  │  - Approval workflow with feedback              │    │
│  └──────────────┬──────────────────────────────────┘    │
│                 │ stdio communication                    │
│  ┌──────────────▼──────────────────────────────────┐    │
│  │    Custom Python MCP Server (separate process)  │    │
│  │  - get_weather_forecast(destination, dates)     │    │
│  │  - get_destination_info(city)                   │    │
│  │  - search_attractions(city, category)           │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Phase 1: Build Custom Python MCP Server

### Understanding MCP Protocol

**Key concepts to learn:**

- MCP uses JSON-RPC 2.0 over stdio/SSE/HTTP
- Server advertises available tools via `tools/list` endpoint
- Client calls tools via `tools/call` with tool name and arguments
- Server returns structured responses

**MCP Python SDK:**

- Package: `mcp` (Model Context Protocol Python SDK)
- Install: `pip install mcp`
- Core components: Server, Tool, types

### File Structure

```
Day 2/examples/
  ├─ travel_mcp_server/
  │   ├─ __init__.py
  │   ├─ server.py          # Main MCP server
  │   ├─ tools/
  │   │   ├─ __init__.py
  │   │   ├─ weather.py     # Weather tool implementation
  │   │   ├─ destination.py # Destination info tool
  │   │   ├─ attractions.py # Attractions search tool
  │   ├─ requirements.txt
  │   └─ README.md
```

### Tools to Implement (2-3 tools)

**Tool 1: `get_weather_forecast`**

- Input: destination (str), travel_dates (str)
- Output: Temperature range, conditions, packing suggestions
- Mock data or use free weather API (OpenWeatherMap, WeatherAPI.com)

**Tool 2: `get_destination_info`**

- Input: city (str)
- Output: Country, timezone, currency, languages, visa requirements
- Mock structured data

**Tool 3: `search_attractions`**

- Input: city (str), category (str: "museums", "restaurants", "landmarks")
- Output: List of top attractions with ratings and brief descriptions
- Mock data

### Implementation Steps

**Step 1.1:** Setup MCP server structure

- Install `mcp` Python package
- Create server.py with basic MCP Server initialization
- Understand: Server context, tool registration

**Step 1.2:** Implement first tool (weather)

- Define tool schema (name, description, input schema)
- Implement tool handler function
- Register tool with server
- Add mock data or API integration

**Step 1.3:** Implement remaining tools

- Follow same pattern for destination_info and search_attractions
- Each tool needs: schema + handler + registration

**Step 1.4:** Add server entry point

- Create main() function to run server
- Handle stdio transport (for ADK integration)
- Add error handling and logging

**Step 1.5:** Test server independently

- Create test script that launches server
- Send JSON-RPC requests manually
- Verify tool responses

### Key Learning Resources

- MCP Python SDK docs: https://github.com/modelcontextprotocol/python-sdk
- MCP spec: https://spec.modelcontextprotocol.io/
- Example servers: https://github.com/modelcontextprotocol/servers

## Phase 2: Integrate MCP Server with ADK

### Create Integration Notebook

**File:** `Day 2/notebooks/local_exercise/day-2-comprehensive-project.ipynb`

**Cell sequence:**

**Setup cells:**

- Environment setup (API keys, imports)
- Retry config

**MCP Integration cell:**

- Create `McpToolset` with `StdioConnectionParams`
- Point to your Python server: `command="python"`, `args=["path/to/server.py"]`
- Test connection by listing available tools

**Verification cell:**

- Create simple test agent with only MCP tools
- Run debug query: "What's the weather in Paris?"
- Verify MCP tool execution

### Key Learning Points

- How ADK discovers MCP tools automatically
- Stdio communication between processes
- Tool schema translation (MCP → ADK)

## Phase 3: Build Custom Function Tools (Non-MCP)

**Tool 1: `search_flights(origin, destination, date)`**

- Mock flight database (dict with routes and prices)
- Return: List of flight options with airline, price, duration

**Tool 2: `search_accommodations(destination, checkin, checkout, budget)`**

- Mock hotel database
- Return: List of hotels with price per night, rating, amenities

**Tool 3: `calculate_trip_cost(flight_cost, accommodation_cost, days, meals_per_day)`**

- Option A: Regular function
- Option B: Agent-as-tool with BuiltInCodeExecutor (like day-2a)

**Tool 4: `get_currency_exchange(from_currency, to_currency)`**

- Use real API: exchangerate-api.com
- Return conversion rate

## Phase 4: Enhanced Human-in-the-Loop with Feedback

### Difference from Day-2b

Day-2b: Simple approve/reject

Your project: Approve/reject + optional feedback text

### Implementation

**Tool: `book_trip_with_feedback(trip_plan, tool_context)`**

**Logic flow:**

1. Auto-approve if total_cost < $1500
2. If total_cost >= $1500 and first call → request_confirmation with trip summary
3. If resumed → check confirmation status:

   - If confirmed: Proceed with booking
   - If rejected: Check if feedback provided
     - If feedback exists: Return status="needs_revision" + feedback text
     - If no feedback: Return status="cancelled"

**Key difference:** The tool returns feedback that the agent can use to revise the plan

### Workflow Function Enhancement

**`run_travel_workflow(query, auto_approve=True, feedback_text=None)`**

**Enhanced flow:**

1. Initial request → agent creates travel plan
2. Check for `adk_request_confirmation` event
3. If found:

   - Display trip summary to user
   - Get human decision (approve/reject/feedback)
   - If feedback provided:
     - Resume with rejection + feedback text
     - Agent receives feedback, revises plan
     - Loop back (agent may trigger approval again with new plan)
   - If simple approve:
     - Resume with confirmation
     - Agent completes booking

**Iterative loop:**

```
User request
    ↓
Agent creates Plan A (expensive)
    ↓
PAUSE for approval
    ↓
Human: "Reject - too expensive, find cheaper flights"
    ↓
Agent receives feedback → creates Plan B (cheaper)
    ↓
PAUSE for approval again
    ↓
Human: "Approve"
    ↓
Book and confirm
```

## Phase 5: Complete Travel Agent Assembly

### Main Agent Configuration

**Agent: `travel_planner_agent`**

- Model: Gemini 2.5 Flash Lite
- Tools array: [

search_flights,

search_accommodations,

get_currency_exchange,

AgentTool(budget_calculator_agent),  # if using agent-as-tool

mcp_travel_toolset,  # Your custom MCP server tools

FunctionTool(book_trip_with_feedback)

]

**Instructions:**

- Guide user through travel planning steps
- Use MCP tools for weather and destination info
- Use local tools for flights and accommodation
- Calculate total budget
- Call book_trip_with_feedback when ready
- If feedback received, revise the plan based on feedback
- Present revised plan to user

### Resumable App Setup

- Wrap agent in App with ResumabilityConfig
- Enable state persistence for pause/resume

### Session and Runner

- InMemorySessionService for session management
- Runner with app (not agent)

## Phase 6: Testing Scenarios

**Test 1: Simple cheap trip (no approval needed)**

Query: "Plan a weekend trip to Boston from New York"

Expected: Auto-approved, immediate itinerary

**Test 2: Expensive trip - approve**

Query: "Plan a 2-week luxury trip to Tokyo from London"

Expected: Pause → human approves → complete booking

**Test 3: Expensive trip - reject with feedback**

Query: "Plan a trip to Paris for 10 days"

Expected: Pause → human rejects with feedback "reduce to 5 days" → agent revises → pause again → approve

**Test 4: Multiple revision cycles**

Query: "Plan a trip to Bali"

Expected: Multiple feedback iterations before final approval

## Implementation Order Summary

1. Build MCP server with 2-3 tools (weather, destination, attractions)
2. Test MCP server independently
3. Create notebook and integrate MCP server with ADK
4. Add custom function tools (flights, accommodations, currency)
5. Build budget calculator (function or agent-as-tool)
6. Implement book_trip_with_feedback tool with ToolContext
7. Create helper functions for event handling (with feedback parsing)
8. Build enhanced workflow function with feedback loop
9. Create main travel agent with all tools
10. Wrap in resumable App
11. Test all scenarios

## Key Learning Outcomes

- MCP protocol and server implementation
- Tool schema design and registration
- Stdio transport for inter-process communication
- ADK MCP integration patterns
- Advanced human-in-the-loop patterns
- Iterative agent workflows with feedback
- State management across pause/resume cycles
- Event-driven architecture

## Resources and Commands

**Install MCP SDK:**

```bash
pip install mcp
```

**Run your MCP server (testing):**

```bash
python Day\ 2/examples/travel_mcp_server/server.py
```

**ADK Documentation:**

- MCP Tools: https://google.github.io/adk-docs/tools/mcp-tools/
- Function Tools: https://google.github.io/adk-docs/tools/function-tools/
- Apps and Resumability: https://google.github.io/adk-docs/runtime/

**MCP Resources:**

- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP Specification: https://spec.modelcontextprotocol.io/
- Example servers: https://github.com/modelcontextprotocol/servers

## Tips for Success

1. **Build incrementally** - Get each phase working before moving to next
2. **Test in isolation** - Test MCP server before ADK integration
3. **Use print statements** - Debug tool calls and event flow
4. **Start with mock data** - Add real APIs later once flow works
5. **Understand events** - Print all events to understand the flow
6. **Read MCP spec** - Understanding JSON-RPC protocol is crucial
7. **Check examples** - Look at existing MCP server implementations

## When You Get Stuck

Common issues and what to check:

- MCP server not connecting: Check stdio setup, command path
- Tools not appearing: Verify tool registration and schema
- Approval not working: Check event parsing and invocation_id
- Feedback not received: Verify FunctionResponse structure
- Agent ignoring feedback: Check instructions and response parsing

### To-dos

- [ ] Setup Python MCP server structure and install dependencies
- [ ] Implement 2-3 MCP tools (weather, destination info, attractions)
- [ ] Test MCP server independently before ADK integration
- [ ] Create McpToolset in notebook and connect to custom server
- [ ] Build non-MCP tools (flights, accommodations, currency)
- [ ] Implement book_trip_with_feedback tool with ToolContext and feedback handling
- [ ] Build enhanced workflow function with feedback loop and iteration support
- [ ] Assemble complete travel agent with all tools and resumability
- [ ] Test all scenarios including feedback iterations