# Context Engineering: Sessions & Memory - Complete Notes

## Core Concepts

### What is Context Engineering?
- **Definition**: The process of dynamically assembling and managing information within an LLM's context window to enable stateful, intelligent agents
- **Evolution**: Moves beyond static Prompt Engineering to dynamic, state-aware context construction
- **Analogy**: Like a chef's mise en place - gathering all the right ingredients before cooking

### Key Components
1. **Sessions**: Container for entire conversation with chronological history and working memory
2. **Memory**: Long-term persistence mechanism capturing key information across multiple sessions

---

## Context Engineering Framework

### Three Types of Context

#### 1. Context to Guide Reasoning
- **System Instructions**: Agent's persona, capabilities, constraints
- **Tool Definitions**: APIs/functions the agent can use
- **Few-Shot Examples**: Curated examples for in-context learning

#### 2. Evidential & Factual Data
- **Long-Term Memory**: User/topic knowledge across sessions
- **External Knowledge**: RAG-retrieved information
- **Tool Outputs**: Data returned by tools
- **Sub-Agent Outputs**: Results from specialized agents
- **Artifacts**: Non-textual data (files, images)

#### 3. Immediate Conversational Information
- **Conversation History**: Turn-by-turn dialogue record
- **State/Scratchpad**: Temporary reasoning information
- **User's Prompt**: Immediate query

---

## Context Engineering Lifecycle

### The Continuous Cycle (Every Turn)

```
1. Fetch Context
   ↓
2. Prepare Context (Blocking)
   ↓
3. Invoke LLM and Tools (Iterative)
   ↓
4. Upload Context (Background)
```

### Key Principles
- **Fetch**: Retrieve memories, RAG docs, recent conversation events
- **Prepare**: Construct full prompt (blocking, hot-path process)
- **Invoke**: Iteratively call LLM and tools
- **Upload**: Persist new information (asynchronous)

---

## Sessions Deep Dive

### What is a Session?
- Self-contained record of a single, continuous conversation
- Tied to a specific user
- Contains: **Events** (chronological history) + **State** (working memory)

### Event Types
- **User Input**: Messages (text, audio, image)
- **Agent Response**: Agent's replies
- **Tool Call**: External tool/API usage
- **Tool Output**: Data returned from tools

### Session Storage
- **Development**: In-memory storage acceptable
- **Production**: Robust databases (e.g., Agent Engine Sessions)
- **Critical**: Agent runtimes are stateless - must persist sessions

---

## Multi-Agent Systems & Sessions

### Two Primary Approaches

#### 1. Shared, Unified History
- **All agents** read/write to same conversation log
- Single source of truth
- Best for: Tightly coupled, collaborative tasks
- Example: Multi-step problem-solving where output of one is input for next

#### 2. Separate, Individual Histories
- Each agent maintains private conversation history
- Communication through explicit messages only
- Implemented via:
  - **Agent-as-a-Tool**: One agent invokes another as a tool
  - **Agent-to-Agent (A2A) Protocol**: Structured messaging protocol

### Interoperability Challenge
- Framework-specific internal representations create isolation
- **A2A Protocol**: Enables message exchange but lacks rich contextual state
- **Solution**: Framework-agnostic data layer (Memory) for shared knowledge

---

## Production Considerations for Sessions

### Security & Privacy
- **Strict Isolation**: One user can NEVER access another's session (ACLs)
- **PII Redaction**: Remove before storing (use Model Armor)
- **Best Practice**: Never persist sensitive data

### Data Integrity
- **TTL Policies**: Auto-delete inactive sessions
- **Retention Policies**: Define storage duration
- **Deterministic Order**: Maintain chronological sequence

### Performance & Scalability
- Session data on "hot path" - must be extremely fast
- **Optimization**: Filter/compact history before transfer
- Reduce data size to mitigate latency

---

## Managing Long Context Conversations

### The Problem
1. **Context Window Limits**: Max text LLM can process
2. **API Costs**: More tokens = higher costs
3. **Latency**: More text = slower responses
4. **Quality**: Performance degrades with excessive tokens

### Compaction Strategies

#### Simple Approaches
- **Last N Turns**: Keep only recent N turns (sliding window)
- **Token-Based Truncation**: Include messages up to token limit

#### Sophisticated Approach
- **Recursive Summarization**: Replace older messages with AI-generated summaries

### Trigger Mechanisms
- **Count-Based**: Token size/turn count threshold
- **Time-Based**: After inactivity period (e.g., 15-30 min)
- **Event-Based**: Task/topic completion detected

### Critical Best Practices
- Perform expensive operations **asynchronously in background**
- **Persist results** to avoid redundant computation
- Track which events are in compacted summary

---

## Memory: The Game Changer

### Why Memory Matters

#### Key Capabilities Unlocked
1. **Personalization**: Remember preferences, facts, past interactions
2. **Context Window Management**: Compact history while preserving context
3. **Data Mining**: Extract insights across users
4. **Self-Improvement**: Learn from previous runs (procedural memories)

### Memory vs RAG: Critical Distinction

| Aspect | RAG Engines | Memory Managers |
|--------|-------------|-----------------|
| **Primary Goal** | Inject external factual knowledge | Create personalized, stateful experience |
| **Data Source** | Static external knowledge base | User-agent dialogue |
| **Isolation** | Shared (global) | Highly isolated (per-user) |
| **Information Type** | Static, factual, authoritative | Dynamic, user-specific |
| **Write Pattern** | Batch processing (offline) | Event-based (every turn/session) |
| **Read Pattern** | Tool-based retrieval | Tool-based OR static retrieval |
| **Data Format** | Natural language "chunk" | NL snippet or structured profile |
| **Data Prep** | Chunking and indexing | Extraction and consolidation |

**Key Insight**: RAG = Research Librarian (expert on facts), Memory = Personal Assistant (expert on user)

---

## Memory Architecture

### Components of a Memory System

1. **User**: Provides raw source data
2. **Agent (Developer Logic)**: Decides what/when to remember
3. **Agent Framework**: Provides tools for memory interaction
4. **Session Storage**: Stores turn-by-turn conversation
5. **Memory Manager**: Handles storage, retrieval, compaction

### Memory Structure
- **Content**: Extracted information (structured or unstructured)
  - **Structured**: Dictionary/JSON (e.g., `{"seat_preference": "Window"}`)
  - **Unstructured**: Natural language (e.g., "User prefers window seat")
- **Metadata**: Context about memory (ID, owner, labels)

---

## Types of Memory

### By Information Type
1. **Declarative Memory** ("knowing what")
   - Facts, figures, events
   - Semantic (world knowledge) and Episodic (user-specific)
   
2. **Procedural Memory** ("knowing how")
   - Skills and workflows
   - Guides actions and sequences

### Organization Patterns
1. **Collections**: Multiple self-contained memories per user
2. **Structured User Profile**: Core facts like contact card
3. **"Rolling" Summary**: Single evolving document

### Storage Architectures
1. **Vector Databases**: Semantic similarity search
2. **Knowledge Graphs**: Entity-relationship networks
3. **Hybrid**: Both relational and semantic search

### Creation Mechanisms
- **Explicit**: User directly commands to remember
- **Implicit**: Agent infers from conversation
- **Internal**: Built into framework
- **External**: Specialized service (Memory Bank, Mem0, Zep)

### Memory Scope
- **User-Level**: Continuous personalized experience
- **Session-Level**: Compaction of long conversations
- **Application-Level**: Shared context for all users (e.g., procedural)

---

## Multimodal Memory

### Two Approaches
1. **Memory FROM Multimodal Source**: 
   - Process images/audio/video
   - Store as **textual insights**
   - Most common implementation

2. **Memory WITH Multimodal Content**:
   - Store actual media files
   - More advanced, requires specialized infrastructure

---

## Memory Generation: The ETL Pipeline

### Overview
LLM-driven Extract, Transform, Load process

### Four Stages

#### 1. Ingestion
- Client provides raw data (conversation history)

#### 2. Extraction & Filtering
- LLM extracts meaningful content
- Only captures info matching **predefined topic definitions**
- No match = no memory created

#### 3. Consolidation (Most Critical)
LLM compares new info with existing memories:
- **Merge**: New insight into existing memory
- **Delete**: Invalidated memory
- **Create**: Novel topic

Addresses:
- Information duplication
- Conflicting information
- Information evolution
- Memory relevance decay

#### 4. Storage
- Persist to durable storage (vector DB or knowledge graph)

### Extraction Techniques

#### Topic Definition Methods
1. **Schema/Template-Based**: Predefined JSON schema
2. **Natural Language Descriptions**: Simple topic descriptions
3. **Few-Shot Prompting**: Learn from examples

### Consolidation Operations
- **UPDATE**: Modify existing memory
- **CREATE**: Add novel memory
- **DELETE/INVALIDATE**: Remove irrelevant memory

---

## Memory Provenance: Building Trust

### Why Provenance Matters
- Assess memory trustworthiness
- Critical for consolidation and inference decisions
- Track origin and history

### Source Type Hierarchy (High to Low Trust)
1. **Bootstrapped Data**: Pre-loaded from internal systems (CRM)
2. **User Input**: 
   - Explicit (forms) - high trust
   - Implicit (conversation) - lower trust
3. **Tool Output**: Generally discouraged (brittle, stale)

### Challenges Addressed
1. **Conflict Resolution**: Use trust hierarchy when sources contradict
2. **Derived Data Deletion**: Regenerate affected memories when source revoked

### Dynamic Confidence Scoring
- **Increases**: Corroboration from multiple sources
- **Decreases**: Time-based decay, contradictory info
- **Pruning**: Delete low-confidence memories

**Critical**: Memories + confidence scores injected into prompt for LLM reasoning

---

## Triggering Memory Generation

### Trigger Strategies
- **Session Completion**: End of multi-turn session
- **Turn Cadence**: Every N turns (e.g., every 5)
- **Real-Time**: After every single turn
- **Explicit Command**: User says "Remember this"

### Cost vs Fidelity Tradeoff
- **Frequent (Real-Time)**: High fidelity, high cost, potential latency
- **Infrequent (Session End)**: Cost-effective, lower fidelity

### Memory-as-a-Tool Pattern
- Agent decides when to create memory
- Memory generation exposed as tool (`create_memory`)
- Agent analyzes conversation and calls tool when meaningful

**Best Practice**: Run memory generation **asynchronously in background**

---

## Memory Retrieval

### Retrieval Strategy Dimensions

#### Three Scoring Dimensions
1. **Relevance**: Semantic similarity to current conversation
2. **Recency**: How recently created
3. **Importance**: Overall critical significance

**Critical Mistake**: Relying solely on vector similarity
**Best Practice**: Blended approach combining all three

### Advanced Techniques (High Latency)
- **Query Rewriting**: LLM improves search query
- **Reranking**: LLM re-evaluates candidate set
- **Specialized Retriever**: Fine-tuned model
- **Mitigation**: Caching layer for repeated queries

### Retrieval Timing

#### 1. Proactive Retrieval
- Auto-load at start of every turn
- Always available but unnecessary latency
- **Optimization**: Cache memories (static during turn)

#### 2. Reactive Retrieval (Memory-as-a-Tool)
- Agent decides when to retrieve
- More efficient, only when needed
- Higher latency but less frequent
- Requires additional LLM call

---

## Inference with Memories

### Placement Strategies

#### 1. System Instructions
**Method**: Append memories to system prompt

**Pros**:
- High authority
- Clean separation from dialogue
- Ideal for stable, global info (user profile)

**Cons**:
- Risk of over-influence
- Requires dynamic prompt construction
- Incompatible with Memory-as-a-Tool
- Poor for multimodal memories

#### 2. Conversation History
**Method**: Inject memories into dialogue

**Placement Options**:
- Before full conversation
- Right before latest query
- Via tool calls (in tool output)

**Pros**:
- Works with Memory-as-a-Tool
- Supports multimodal

**Cons**:
- Noisy (increases token costs)
- Risk of dialogue injection
- Must use correct perspective (1st person for user-level)

### Hybrid Strategy (Recommended)
- **System Prompt**: Stable, global memories (user profile)
- **Dialogue Injection/Tool**: Transient, episodic memories

---

## Procedural Memory: The Next Frontier

### Current State
- Most platforms focus on **declarative** memory (the "what")
- Procedural memory (the "how") requires separate lifecycle

### Procedural Memory Lifecycle
1. **Extraction**: Distill reusable strategy/playbook from successful interaction
2. **Consolidation**: Curate workflow itself
   - Integrate new methods with best practices
   - Patch flawed steps
   - Prune outdated procedures
3. **Retrieval**: Fetch plan to guide task execution

### Procedural vs Fine-Tuning
- **Fine-Tuning (RLHF)**: Slow, offline, alters model weights
- **Procedural Memory**: Fast, online, injects playbook via in-context learning

---

## Testing & Evaluation

### Memory Generation Quality

#### Metrics (Compare to Golden Set)
- **Precision**: % of created memories that are accurate/relevant
- **Recall**: % of relevant facts captured
- **F1-Score**: Harmonic mean of precision and recall

### Memory Retrieval Performance
- **Recall@K**: Correct memory in top K results
- **Latency**: Must be <200ms (hot path)

### End-to-End Task Success
- Agent performance on downstream tasks using memory
- LLM "judge" compares output to golden answer
- Ultimate measure of memory system value

### Continuous Improvement Process
1. Establish baseline
2. Analyze failures
3. Tune system (prompts, retrieval algorithms)
4. Re-evaluate and measure impact

---

## Production Architecture

### Decoupled Architecture Pattern

```
1. Agent pushes data (non-blocking API call)
   ↓
2. Memory manager queues task
   ↓
3. Background processing (LLM calls, consolidation)
   ↓
4. Persist memories to database
   ↓
5. Agent retrieves on-demand
```

### Scalability Requirements
- **Concurrency**: Prevent deadlocks/race conditions
- **Transactional Operations**: Optimistic locking
- **Message Queue**: Buffer high volumes
- **Failure Handling**: Retry with exponential backoff, dead-letter queue
- **Multi-Region**: Built-in replication for global apps

### Performance Considerations
- Generation/consolidation must be asynchronous
- Retrieval on hot path (sub-second latency budget)
- Throughput must match user demand

---

## Privacy & Security

### Data Isolation (Cardinal Rule)
- **Strict per-user/tenant isolation**
- Enforce with restrictive ACLs
- Users must have programmatic control (opt-out, deletion)

### Security Safeguards
1. **PII Redaction**: Before persistence (Model Armor)
2. **Memory Poisoning Prevention**: Validate/sanitize before committing
   - Guard against prompt injection attacks
   - Detect and discard malicious content
3. **Exfiltration Risk**: Anonymize shared memories (procedural)

### Analogy: Corporate Archivist
- Never mix confidential files
- Redact sensitive information
- Spot and discard forgeries
- Anonymize before company-wide sharing

---

## Key Takeaways & Game Changers

### Revolutionary Concepts

1. **Context Engineering ≠ Prompt Engineering**
   - Dynamic, state-aware vs static instructions
   - Orchestrates entire payload, not just system prompt

2. **Memory as Active System**
   - Not passive vector database
   - Intelligent extraction, consolidation, curation
   - LLM-driven ETL pipeline

3. **Memory vs RAG Distinction**
   - RAG: Expert on facts (research librarian)
   - Memory: Expert on user (personal assistant)
   - Both needed for truly intelligent agents

4. **Consolidation is Critical**
   - Self-editing process prevents noise
   - Handles conflicts, duplication, evolution
   - Enables "forgetting" outdated information

5. **Memory-as-a-Tool Pattern**
   - Agent decides when to remember/retrieve
   - More efficient than always-on
   - Requires proper tool description

6. **Provenance Drives Trust**
   - Track source type and history
   - Dynamic confidence scoring
   - Informs both consolidation and inference

7. **Asynchronous Processing Non-Negotiable**
   - Memory generation MUST be background
   - Never block user experience
   - Separate service architecture

8. **Procedural Memory = Self-Evolution**
   - Agent learns "how" not just "what"
   - Builds playbook of effective solutions
   - Fast, online adaptation vs slow fine-tuning

### Implementation Best Practices

#### Must-Do's
- ✅ Redact PII before persistence
- ✅ Run memory generation asynchronously
- ✅ Use hybrid retrieval (relevance + recency + importance)
- ✅ Implement strict data isolation
- ✅ Compact long sessions proactively
- ✅ Track memory provenance
- ✅ Use managed services (Memory Bank) when possible

#### Must-Avoid's
- ❌ Never store tool outputs as long-term memory
- ❌ Never rely solely on vector similarity
- ❌ Never block user for memory generation
- ❌ Never share memories across users without anonymization
- ❌ Never process same events multiple times

---

## Tools & Services Mentioned

### Google Cloud Products
- **Agent Engine Sessions**: Managed session storage
- **Agent Engine Memory Bank**: Managed memory service
- **Model Armor**: PII detection and redaction
- **Vertex AI**: LLM API access

### Agent Frameworks
- **ADK (Agent Development Kit)**: Google's framework
- **LangGraph**: Alternative framework with mutable state

### Third-Party Memory Managers
- **Mem0**: External memory service
- **Zep**: External memory service

---

## Code Pattern Examples

### Session Truncation (ADK)
```python
from google.adk.plugins.context_filter_plugin import ContextFilterPlugin

app = App(
    plugins=[
        ContextFilterPlugin(num_invocations_to_keep=10)
    ]
)
```

### Memory Generation (Memory Bank)
```python
client.agent_engines.memories.generate(
    name="projects/.../reasoningEngines/...",
    scope={"user_id": "123"},
    direct_contents_source={"events": [...]},
    config={"wait_for_completion": False}  # Background
)
```

### Memory Retrieval (ADK)
```python
# Proactive
agent = LlmAgent(
    tools=[PreloadMemoryTool()]
)

# Reactive (Memory-as-a-Tool)
def load_memory(query: str, tool_context: ToolContext):
    """Retrieves memories for the user."""
    return tool_context.search_memory(query).memories

agent = LlmAgent(tools=[load_memory])
```

---

## Further Reading

Key papers and resources referenced:
- RAG: https://cloud.google.com/use-cases/retrieval-augmented-generation
- In-context learning: https://arxiv.org/abs/2301.00234
- A2A Protocol: https://agent2agent.info/docs/concepts/message/
- Long context limitations: https://ai.google.dev/gemini-api/docs/long-context
- Memory types (cognitive science): https://huggingface.co/blog/Kseniase/memory
- RLHF: https://cloud.google.com/blog/products/ai-machine-learning/rlhf-on-google-cloud

---

*Notes compiled from "Context Engineering: Sessions, Memory" whitepaper by Kimberly Milam and Antonio Gulli, November 2025*