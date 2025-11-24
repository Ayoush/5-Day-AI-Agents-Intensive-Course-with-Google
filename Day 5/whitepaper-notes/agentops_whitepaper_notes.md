# Comprehensive Notes: Prototype to Production (AgentOps)

**Authors:** Sokratis Kartakis, Gabriela Hernandez Larios, Ran Li, Elia Secchi, Huang Xia  
**Date:** November 2025

---

## Executive Summary

This whitepaper addresses the "last mile" challenge in AI agent deployment: **80% of effort is spent on infrastructure, security, and validation** rather than core intelligence. It introduces **AgentOps** as a comprehensive operational discipline for transitioning agents from prototype to production-grade systems.

**Key Principle:** *"Building an agent is easy. Trusting it is hard."*

---

## Core Foundation: Three Pillars

AgentOps is built on three essential pillars:

1. **Automated Evaluation** - Quality gates before deployment
2. **Automated Deployment (CI/CD)** - Structured, safe release process
3. **Comprehensive Observability** - Real-time monitoring and insights

---

## 1. People and Process

### Traditional MLOps Teams

- **Cloud Platform Team**: Infrastructure, security, access control
- **Data Engineering Team**: Data pipelines, ingestion, quality
- **Data Science & MLOps Team**: Model training, ML pipeline automation
- **ML Governance**: Compliance, transparency, accountability

### New GenAI-Specific Roles

- **Prompt Engineers**: Craft prompts with domain expertise
- **AI Engineers**: Scale GenAI to production with RAG, guardrails, evaluation
- **DevOps/App Developers**: Frontend integration

**Key Insight:** Technology alone is insufficient; success requires orchestrated teams with specialized roles.

---

## 2. Pre-Production: The Journey to Production

### 2.1 Evaluation as a Quality Gate

Traditional software tests are **insufficient for agents** because:
- Agents reason and adapt dynamically
- Must evaluate entire reasoning trajectory, not just final output
- Need behavioral quality assessment, not just functional correctness

#### Two Implementation Approaches:

**Manual "Pre-PR" Evaluation:**
- Engineer runs evaluation suite locally
- Performance report linked in PR description
- Human reviewer assesses behavioral changes

**Automated In-Pipeline Gate:**
- Evaluation integrated into CI/CD
- Failing evaluation blocks deployment automatically
- Enforces predefined quality thresholds

**Reference:** Day 4 whitepaper covers evaluation specifics, golden datasets, LLM-as-a-judge techniques, and Vertex AI Evaluation.

---

### 2.2 The Automated CI/CD Pipeline

Agents are **composite systems**: code + prompts + tool definitions + configs. CI/CD manages this complexity through **three progressive phases:**

#### Phase 1: Pre-Merge Integration (CI)
- **Purpose:** Fast feedback to developers before merge
- **Actions:** Unit tests, linting, dependency scanning, quality evaluation
- **Benefit:** Catches issues before polluting main branch
- **Tool Example:** Cloud Build PR checks configuration

#### Phase 2: Post-Merge Validation in Staging (CD)
- **Purpose:** Validate operational readiness
- **Environment:** High-fidelity production replica
- **Actions:** Load testing, integration tests, internal user testing ("dogfooding")
- **Benefit:** Ensures system performs under production-like conditions

#### Phase 3: Gated Deployment to Production
- **Purpose:** Final release with human oversight
- **Process:** Product Owner approval → deploy validated artifact
- **Principle:** Human-in-the-loop for final sign-off

#### Supporting Technologies:

**Infrastructure as Code (IaC):**
- Tools like Terraform define environments programmatically
- Ensures identical, repeatable, version-controlled environments

**Automated Testing Frameworks:**
- Pytest handles agent-specific artifacts (conversation histories, tool logs, reasoning traces)

**Secrets Management:**
- Use Secret Manager for API keys
- Inject at runtime, never hardcode

---

### 2.3 Safe Rollout Strategies

**Never switch 100% of users at once.** Four proven patterns:

1. **Canary Deployment**
   - Start with 1% of users
   - Monitor for prompt injections, unexpected tool usage
   - Scale gradually or rollback instantly

2. **Blue-Green Deployment**
   - Run two identical production environments
   - Switch traffic instantly between versions
   - Zero downtime, instant recovery

3. **A/B Testing**
   - Compare versions on real business metrics
   - Data-driven decisions
   - Can use internal or external users

4. **Feature Flags**
   - Deploy code but control release dynamically
   - Test capabilities with select users first

**Critical Foundation:** Rigorous versioning of ALL components:
- Code, prompts, model endpoints, tool schemas, memory structures, evaluation datasets
- Enables instant rollback (production "undo" button)

**Tools:** Agent Engine or Cloud Run for deployment, Cloud Load Balancing for traffic management

---

### 2.4 Building Security from the Start

Agents face unique security challenges due to autonomous decision-making:

#### Key Risks:
- **Prompt Injection & Rogue Actions**: Users trick agents into unintended actions
- **Data Leakage**: Inadvertent exposure of sensitive information
- **Memory Poisoning**: False information corrupts future interactions

#### Three Layers of Defense (Google's Secure AI Agents):

**Layer 1: Policy Definition and System Instructions**
- Define desired/undesired behavior
- Engineer into System Instructions (agent's "constitution")

**Layer 2: Guardrails, Safeguards, and Filtering**
- **Input Filtering**: Perspective API to block malicious inputs
- **Output Filtering**: Vertex AI safety filters for harmful content, PII, policy violations
- **Human-in-the-Loop (HITL)**: Escalate high-risk actions for human review

**Layer 3: Continuous Assurance and Testing**
- **Rigorous Evaluation**: Re-run comprehensive tests on any change
- **RAI Testing**: Neutral Point of View (NPOV) and Parity evaluations
- **Red Teaming**: Proactive security testing with AI-driven personas

**Key Principle:** Safety is not one-time setup; requires constant evaluation and adaptation.

---

## 3. Operations In-Production

### The Operational Loop: Observe → Act → Evolve

Once live, focus shifts to maintaining reliability, cost-effectiveness, and safety through a continuous cycle.

---

### 3.1 Observe: Your Agent's Sensory System

Observability provides the foundation for effective operations through **three pillars:**

#### Logs
- Granular, factual diary of events
- Records every tool call, error, decision

#### Traces
- Narrative connecting individual logs
- Reveals causal path of agent actions
- Unique trace ID links entire request chain

#### Metrics
- Aggregated performance summary
- Cost, latency, operational health at scale
- Dashboard alerts for threshold violations

**Google Cloud Implementation:**
- Cloud Trace for distributed tracing
- Cloud Logging for detailed logs
- Cloud Monitoring for dashboards and alerts
- Agent Development Kit (ADK) provides built-in integration

---

### 3.2 Act: The Levers of Operational Control

Observations must drive **real-time interventions** to manage performance, cost, and safety.

**Distinction:**
- **Act** = Automated reflexes for real-time stability
- **Evolve** = Strategic learning for fundamental improvements

#### Managing System Health: Performance, Cost, Scale

**Designing for Scale:**

1. **Horizontal Scaling**
   - Design as stateless, containerized service
   - External state management
   - Any instance handles any request
   - Use Cloud Run or Vertex AI Agent Engine Runtime

2. **Asynchronous Processing**
   - Offload long-running tasks
   - Event-driven patterns (e.g., Pub/Sub)
   - Keeps agent responsive

3. **Externalized State Management**
   - LLMs are stateless; persist memory externally
   - Options: Vertex AI Agent Engine (built-in) or custom (AlloyDB, Cloud SQL)

**Balancing Competing Goals:**

- **Speed (Latency)**
  - Design for parallel execution
  - Aggressive caching
  - Use smaller models for routine tasks

- **Reliability (Handling Glitches)**
  - Automatic retry with exponential backoff
  - Design idempotent tools (safe-to-retry)
  - Prevents duplicate charges/actions

- **Cost**
  - Shorten prompts
  - Use cheaper models for easier tasks
  - Batch requests

#### Managing Risk: Security Response Playbook

**Three-Step Response to Threats:**

1. **Contain**: Circuit breaker to disable affected tool immediately
2. **Triage**: Route suspicious requests to HITL review queue
3. **Resolve**: Develop patch, deploy through CI/CD with full testing

---

### 3.3 Evolve: Learning from Production

Move from **reactive incidents** to **proactive improvements** by analyzing patterns and fixing root causes.

#### The Engine of Evolution: Automated CI/CD

**Why Speed Matters:** An insight is only valuable if you can act on it quickly. Fast path to production closes loop in hours/days, not weeks/months.

**The Automated Workflow:**

1. **Commit the Change**: Proposed improvement to version-controlled repo
2. **Trigger Automation**: CI/CD pipeline runs automatically
3. **Validate Rigorously**: Full test suite including quality evaluation
4. **Deploy Safely**: Use safe rollout strategy

#### The Evolution Workflow

**Step-by-Step Process:**

1. **Analyze Production Data**
   - Identify trends in user behavior
   - Review task success rates
   - Examine security incidents

2. **Update Evaluation Datasets**
   - Transform production failures into test cases
   - Augment golden dataset continuously

3. **Refine and Deploy**
   - Commit improvements (prompts, tools, guardrails)
   - Trigger automated pipeline
   - Deploy validated changes

**Example Evolution Loop:**
- Problem: 15% of users receive error for "similar products"
- Act: Create high-priority ticket
- Evolve: Create failing test case, refine prompt, add robust tool
- Result: Issue resolved in under 48 hours

#### Evolving Security: Production Feedback Loop

Security is **dynamic and continuous**, not static:

1. **Observe**: Detect new threat vectors (novel prompt injection, data leaks)
2. **Act**: Immediate containment
3. **Evolve**: 
   - Add attack to evaluation suite
   - Refine guardrails and filters
   - Deploy through CI/CD
   - Close vulnerability permanently

**Key Principle:** Every production incident makes the agent stronger and more resilient.

---

## 4. Beyond Single-Agent Operations: Interoperability

### The Problem

Organizations build dozens of specialized agents:
- Customer service agent
- Analytics forecasting system
- Fraud detection agent

**Challenge:** These agents can't communicate or collaborate, creating massive inefficiency and trapped insights.

---

### 4.1 Two Complementary Protocols

#### Model Context Protocol (MCP)
- **Purpose**: Universal standard for tool integration
- **Use Case**: Stateless functions with structured inputs/outputs
- **Examples**: Fetching weather data, querying databases
- **Analogy**: "Do this specific thing"

#### Agent-to-Agent Protocol (A2A)
- **Purpose**: Complex, stateful collaboration between intelligent agents
- **Use Case**: Delegate complex goals requiring reasoning, planning, state
- **Examples**: "Analyze customer churn and recommend strategies"
- **Analogy**: "Achieve this complex goal"

**Key Distinction:**
- **MCP** = Tools and resources (primitives)
- **A2A** = Other agents (autonomous systems)

---

### 4.2 A2A Protocol Implementation

#### Agent Cards
- Standardized JSON specifications
- Acts as "business card" for each agent
- Describes capabilities, security requirements, skills, URL
- Enables dynamic peer discovery

**Example Agent Card Contents:**
```
- name, version, description
- capabilities
- securitySchemes (OAuth 2.0)
- defaultInputModes / defaultOutputModes
- skills (with id, name, description, tags)
- url (endpoint for communication)
```

#### Implementing A2A with ADK

**Making an Agent A2A-Compatible:**
- Single function call: `to_a2a(root_agent, port=8001)`
- Automatically generates AgentCard
- Makes agent available on network

**Consuming a Remote Agent:**
- Use `RemoteA2aAgent` class
- Reference agent card URL
- Integrate into hierarchical compositions

#### Technical Requirements

**Non-Negotiable for A2A:**

1. **Distributed Tracing**
   - Every request carries unique trace ID
   - Essential for debugging across multiple agents
   - Maintains coherent audit trail

2. **Robust State Management**
   - A2A interactions are stateful
   - Requires sophisticated persistence layer
   - Tracks progress and ensures transactional integrity

**When to Use A2A:**
- Formal, cross-team integrations
- Requires durable service contract
- Complex, multi-step collaboration

**When to Use Local Sub-Agents:**
- Tightly coupled tasks within single application
- More efficient for simple delegation

---

### 4.3 How A2A and MCP Work Together

Most powerful systems use **both protocols in layered architecture**.

#### Auto Repair Shop Analogy

1. **User-to-Agent (A2A)**: Customer describes problem to Shop Manager agent
2. **Agent-to-Agent (A2A)**: Manager delegates to specialized Mechanic agent
3. **Agent-to-Tool (MCP)**: Mechanic uses tools via MCP:
   - `scan_vehicle_for_error_codes()`
   - `get_repair_procedure()`
   - `raise_platform()`
4. **Agent-to-Agent (A2A)**: Mechanic contacts Parts Supplier agent for parts

**Pattern:**
- **A2A**: High-level, conversational, task-oriented interactions
- **MCP**: Standardized plumbing for specific, structured tools

---

### 4.4 Registry Architectures

#### When to Build Registries

**The Scale Question:**
- 50 tools → Manual configuration works
- 5,000 tools → Need systematic discovery solution

#### Tool Registry (uses MCP)

**Purpose:** Catalog all tools (functions, APIs)

**Three Common Patterns:**
1. **Generalist agents**: Access full catalog (trades speed/accuracy for scope)
2. **Specialist agents**: Use predefined subsets (higher performance)
3. **Dynamic agents**: Query registry at runtime (adapts to new tools)

**Benefits:**
- Human discovery (search before building duplicates)
- Security auditing of tool access
- Product understanding of capabilities

#### Agent Registry (uses A2A AgentCards)

**Purpose:** Help teams discover and reuse existing agents

**Benefits:**
- Reduces redundant work
- Foundation for automated agent-to-agent delegation
- Centralized governance

#### Decision Framework

**Tool Registry:** Build when tool discovery becomes bottleneck or security requires centralized auditing

**Agent Registry:** Build when multiple teams need to discover/reuse specialized agents

**Start Without One:** Only build when ecosystem scale demands centralized management (cost of maintenance)

---

## 5. The AgentOps Lifecycle: Putting It All Together

### The Complete Flow

1. **Developer Inner Loop**
   - Rapid local testing and prototyping
   - Shape agent's core logic

2. **Pre-Production Engine**
   - Automated evaluation gates
   - Validate quality and safety against golden dataset

3. **Safe Rollouts**
   - Release to production with monitoring
   - Canary, blue-green, A/B testing, feature flags

4. **Production Operations**
   - Comprehensive observability captures real-world data
   - Observe → Act → Evolve loop

5. **Continuous Evolution**
   - Every insight becomes next improvement
   - Fast path to production (hours, not weeks)

### Reference Architecture Components

**Core Capabilities:**
- Evaluation framework
- CI/CD pipeline
- Observability stack
- Security layers
- State management
- Interoperability protocols

**Environments:**
- Development (local)
- Staging (production replica)
- Production (live users)

**Processes:**
- Quality gates
- Safe rollouts
- Incident response
- Continuous improvement

---

## 6. Key Takeaways

### The "Last Mile" Challenge

- **80% of effort** is infrastructure, security, validation (not core intelligence)
- Most agent projects fail here due to **underestimating operational complexity**
- Not just technology problem; requires organizational transformation

### AgentOps Core Principles

1. **Evaluation-Gated Deployment**: No agent reaches users without passing comprehensive quality checks
2. **Automated Everything**: CI/CD pipeline is the engine of evolution
3. **Continuous Loop**: Observe → Act → Evolve transforms static deployments into learning systems
4. **Security First**: Build in from start, evolve continuously based on production feedback
5. **Interoperability**: Standardized protocols transform isolated agents into collaborative ecosystem

### Unique Challenges of Agents vs Traditional Software

- **Dynamic Tool Orchestration**: Different behavior every time
- **Scalable State Management**: Remember across interactions
- **Unpredictable Cost & Latency**: Many paths to answers
- **Autonomous Decision-Making**: Can't pre-program every outcome

### Value Proposition

**Immediate Benefits:**
- Prevent security breaches
- Enable rapid rollbacks
- Maintain system reliability

**Long-Term Value:**
- Deploy improvements in hours (not weeks)
- Continuously evolving products
- Compounding value through agent collaboration

---

## 7. Your Path Forward

### If You're Starting Out:

**Focus on Fundamentals:**
1. Build first evaluation dataset
2. Implement CI/CD pipeline
3. Establish comprehensive monitoring

**Quick Start:** Use Agent Starter Pack for production-ready setup in minutes

### If You're Scaling:

**Elevate Your Practice:**
1. Automate feedback loop from insight to deployment
2. Standardize on interoperable protocols
3. Build cohesive ecosystem, not point solutions

### The Next Frontier

Not just building better individual agents, but **orchestrating sophisticated multi-agent systems** that learn and collaborate.

**Key Insight:** "Bridging the last mile is not the final step in a project, but the first step in creating value!"

---

## 8. Tools and Resources Mentioned

### Google Cloud Platform Tools

- **Agent Starter Pack**: Production-ready templates with CI/CD, Terraform, evaluation
- **Vertex AI Evaluation**: Service for agent quality assessment
- **Agent Engine**: Managed runtime with built-in session/memory
- **Cloud Run**: Serverless container platform
- **Cloud Build**: CI/CD automation
- **Cloud Trace**: Distributed tracing
- **Cloud Logging**: Centralized log management
- **Cloud Monitoring**: Dashboards and alerts
- **Secret Manager**: Secure credential storage
- **Pub/Sub**: Event-driven messaging
- **AlloyDB / Cloud SQL**: Database options
- **Cloud Load Balancing**: Traffic management

### Frameworks and Protocols

- **Agent Development Kit (ADK)**: Built-in observability and A2A support
- **Model Context Protocol (MCP)**: Tool integration standard
- **Agent-to-Agent Protocol (A2A)**: Agent interoperability (Linux Foundation)
- **Terraform**: Infrastructure as Code
- **Pytest**: Automated testing framework

### Security Frameworks

- **Google Secure AI Agents Approach**
- **Google Secure AI Framework (SAIF)**
- **Perspective API**: Input content filtering

---

## 9. Related Whitepapers

- **Day 4**: Agent Quality: Observability, Logging, Tracing, Evaluation, Metrics
- **Day 3** (implied): Agent Tools and Interoperability with MCP
- **Google's Approach for Secure AI Agents**
- **Google Secure AI Framework (SAIF)**

---

## 10. Critical Success Factors

### People
- Cross-functional teams with clear roles
- Coordination between AI Engineers, Prompt Engineers, MLOps, Security
- Human-in-the-loop for critical decisions

### Process
- Disciplined evaluation before every release
- Structured CI/CD with progressive validation
- Continuous learning from production

### Technology
- Automated evaluation pipelines
- Robust observability stack
- Secure, scalable infrastructure
- Standardized protocols for interoperability

**Remember:** Technology alone is insufficient. Success requires orchestrated teams, disciplined processes, and the right operational foundation.

---

*"The operational discipline of AgentOps is the foundation that makes sophisticated multi-agent systems possible."*