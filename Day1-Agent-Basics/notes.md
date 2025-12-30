# Day 1: Introduction to AI Agents

## Overview
Day 1 consists of two pre-livestream notebooks that introduce the fundamentals of AI agents and multi-agent architectures using Google's Agent Development Kit (ADK).

---

## Part A: From Prompt to Action

### What is an AI Agent?
**Traditional LLM:** `Prompt -> LLM -> Text`
**AI Agent:** `Prompt -> Agent -> Thought -> Action -> Observation -> Final Answer`

An agent goes beyond simple text responses - it can **take actions** (like searching Google) to find information and accomplish tasks.

### Core ADK Components

1. **Agent** - The main building block
   - `name`: Identifier for the agent
   - `description`: What the agent does
   - `model`: LLM to use (e.g., "gemini-2.5-flash-lite")
   - `instruction`: The agent's guiding prompt/behavior
   - `tools`: List of tools the agent can use (e.g., google_search)

2. **Runner** - Orchestrates agent execution
   - `InMemoryRunner`: Manages conversation and agent responses
   - `.run_debug()`: Quick method for prototyping (abstracts session creation)

3. **Tools** - Actions the agent can perform
   - `google_search`: Built-in tool for web searches
   - `FunctionTool`: Wrapper for custom Python functions
   - `AgentTool`: Wrapper to make sub-agents callable as tools

### Key Setup Steps
```python
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    instruction="You are a helpful assistant...",
    tools=[google_search]
)

runner = InMemoryRunner(agent=agent)
response = await runner.run_debug("Your question here")
```

### ADK Web Interface
- Built-in UI for testing and debugging agents
- Created with `adk create` command
- Launched with `adk web` command
- Great for visualizing agent's thought process and tool usage

---

## Part B: Multi-Agent Systems & Workflow Patterns

### Why Multi-Agent Systems?

**Problem with Monolithic Agents:**
- Long, confusing instructions
- Hard to debug (which part failed?)
- Difficult to maintain
- Unreliable results

**Multi-Agent Solution:**
- Team of specialized agents
- Each agent has one clear job
- Easier to build, test, and maintain
- More reliable through collaboration

### State Management
**`output_key`** - Stores agent output in session state for other agents to use
```python
research_agent = Agent(
    name="ResearchAgent",
    instruction="...",
    output_key="research_findings"
)

summarizer_agent = Agent(
    name="SummarizerAgent",
    instruction="Summarize: {research_findings}",  # References previous output
    output_key="final_summary"
)
```

### Four Workflow Patterns

#### 1. LLM-Based Orchestration (Dynamic)
**When to use:** Need flexible, dynamic decision-making
**How it works:** Root agent has sub-agents as tools via `AgentTool`
**Caveat:** Can be unpredictable - LLM decides the order

```python
root_agent = Agent(
    name="Coordinator",
    instruction="First call ResearchAgent, then SummarizerAgent",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)]
)
```

#### 2. Sequential Workflow (Assembly Line)
**When to use:** Order matters, need predictable pipeline
**How it works:** Runs agents in exact order listed
**Pattern:** A -> B -> C (each waits for previous)

```python
root_agent = SequentialAgent(
    name="Pipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent]
)
```

**Example Use Case:** Blog creation (Outline -> Write -> Edit)

#### 3. Parallel Workflow (Concurrent)
**When to use:** Independent tasks that can run simultaneously
**How it works:** All sub-agents run at once, results combined after
**Benefit:** Dramatically speeds up workflow

```python
parallel_team = ParallelAgent(
    name="ResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher]
)

# Often combined with Sequential for aggregation
root_agent = SequentialAgent(
    sub_agents=[parallel_team, aggregator_agent]
)
```

**Example Use Case:** Multi-topic research that gets combined into one report

#### 4. Loop Workflow (Iterative Refinement)
**When to use:** Need quality improvement through feedback cycles
**How it works:** Repeats agents until condition met or max iterations reached
**Key:** Needs exit condition (e.g., calling `exit_loop` function)

```python
def exit_loop():
    """Called when refinement is complete"""
    return {"status": "approved"}

critic_agent = Agent(name="Critic", ...)
refiner_agent = Agent(
    name="Refiner",
    instruction="If critique is APPROVED, call exit_loop. Otherwise, improve.",
    tools=[FunctionTool(exit_loop)]
)

loop = LoopAgent(
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3
)
```

**Example Use Case:** Story writing with critique and revision cycles

### Decision Tree: Choosing the Right Pattern

| Pattern | When to Use | Key Feature | Example |
|---------|-------------|-------------|---------|
| **LLM Orchestrator** | Dynamic decisions needed | LLM chooses what to call | Research + Summarize |
| **Sequential** | Order matters, linear pipeline | Deterministic order | Outline -> Write -> Edit |
| **Parallel** | Independent tasks, speed critical | Concurrent execution | Multi-topic research |
| **Loop** | Iterative improvement needed | Repeated refinement cycles | Writer + Critic |

### Combining Patterns
You can nest workflows for complex systems:
- Sequential containing Parallel (research in parallel, then aggregate)
- Sequential containing Loop (initial draft, then refinement loop)
- Mix and match as needed

---

## Key Takeaways

- **Agents vs LLMs:** Agents can take actions and observe results, not just generate text
- **Specialization wins:** Multiple simple agents > one complex agent
- **State management:** Use `output_key` to pass data between agents
- **Pattern selection matters:** Choose Sequential for order, Parallel for speed, Loop for quality
- **ADK is flexible:** Supports both dynamic (LLM-orchestrated) and deterministic (workflow agents) patterns

## Important Links

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Quickstart](https://google.github.io/adk-docs/get-started/python/)
- [ADK Agents Overview](https://google.github.io/adk-docs/agents/)
- [Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [Parallel Agents](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
- [Tools Overview](https://google.github.io/adk-docs/tools/)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Get API Key](https://aistudio.google.com/app/api-keys)

## Installation & Setup

```bash
pip install google-adk
```

**API Key Setup:**
1. Get API key from Google AI Studio
2. Add to Kaggle Secrets as `GOOGLE_API_KEY`
3. Set environment variables:
   - `GOOGLE_API_KEY`
   - `GOOGLE_GENAI_USE_VERTEXAI=FALSE`

## Next Steps for Day 2

- Custom functions and tools
- MCP (Model Context Protocol) tools integration
- Long-running operations management
- Advanced tool creation patterns

## Quick Reference: Common Patterns

### Single Agent with Tool
```python
agent = Agent(
    name="assistant",
    model="gemini-2.5-flash-lite",
    instruction="Use Google Search for current info",
    tools=[google_search]
)
```

### Sequential Pipeline
```python
SequentialAgent(sub_agents=[agent1, agent2, agent3])
```

### Parallel Execution + Aggregation
```python
SequentialAgent(
    sub_agents=[
        ParallelAgent(sub_agents=[agent1, agent2, agent3]),
        aggregator_agent
    ]
)
```

### Loop with Exit Condition
```python
LoopAgent(
    sub_agents=[critic, refiner_with_exit_tool],
    max_iterations=3
)
```

## Questions & Notes

- Sessions are covered in detail on Day 3
- ADK is model-agnostic but optimized for Gemini
- Available in Python, Go, Java (more languages coming)
- Use `adk web` for visual debugging during development
