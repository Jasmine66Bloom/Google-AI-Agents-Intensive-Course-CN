"""
Day 1b: Multi-Agent Systems & Workflow Patterns
This script demonstrates building multi-agent systems with different workflow patterns:
- LLM-based orchestration (dynamic decisions)
- Sequential workflows (fixed pipeline)
- Parallel workflows (concurrent execution)
- Loop workflows (iterative refinement)

Prerequisites:
- pip install google-adk python-dotenv
- Create a .env file with your GOOGLE_API_KEY
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types


def setup_api_key():
    """
    Configure the Gemini API key from .env file.
    Looks for .env file in the project root directory.
    """
    # Load .env file from project root (one level up from Day-1 folder)
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please:\n"
            "1. Copy .env.example to .env in the project root\n"
            "2. Add your API key to the .env file\n"
            "3. Get an API key from: https://aistudio.google.com/app/api-keys"
        )
    print("✅ Gemini API key loaded from .env file.")
    return api_key


def create_retry_config():
    """Configure retry options for handling transient errors."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )


# ============================================================================
# Pattern 1: LLM-Based Orchestration (Dynamic Workflow)
# ============================================================================

def create_llm_orchestrated_system(retry_config):
    """
    Create a multi-agent system with LLM-based orchestration.
    The root agent decides which sub-agents to call and in what order.
    """
    print("\n--- Creating LLM-Orchestrated System ---")

    # Research Agent: Uses google_search tool
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic
        and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    # Summarizer Agent: Summarizes research findings
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    # Root Coordinator: Orchestrates the workflow
    root_agent = Agent(
        name="ResearchCoordinator",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a research coordinator. Your goal is to answer the user's query.
        1. First, you MUST call the `ResearchAgent` tool to find relevant information.
        2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool.
        3. Finally, present the final summary clearly to the user as your response.""",
        tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    )

    print("✅ LLM-orchestrated system created (Research + Summarization)")
    return root_agent


# ============================================================================
# Pattern 2: Sequential Workflow (Fixed Pipeline)
# ============================================================================

def create_sequential_blog_pipeline(retry_config):
    """
    Create a sequential multi-agent system for blog post creation.
    Agents run in a fixed order: Outline -> Write -> Edit
    """
    print("\n--- Creating Sequential Blog Pipeline ---")

    # Outline Agent
    outline_agent = Agent(
        name="OutlineAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline
        2. An introduction hook
        3. 3-5 main sections with 2-3 bullet points for each
        4. A concluding thought""",
        output_key="blog_outline",
    )

    # Writer Agent
    writer_agent = Agent(
        name="WriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )

    # Editor Agent
    editor_agent = Agent(
        name="EditorAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Edit this draft: {blog_draft}
        Fix grammatical errors, improve flow and sentence structure, and enhance clarity.""",
        output_key="final_blog",
    )

    # Sequential pipeline
    root_agent = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )

    print("✅ Sequential pipeline created (Outline -> Write -> Edit)")
    return root_agent


# ============================================================================
# Pattern 3: Parallel Workflow (Concurrent Execution)
# ============================================================================

def create_parallel_research_system(retry_config):
    """
    Create a parallel multi-agent system for multi-topic research.
    Multiple research agents run concurrently, then an aggregator combines results.
    """
    print("\n--- Creating Parallel Research System ---")

    # Tech Researcher
    tech_researcher = Agent(
        name="TechResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
        the main companies involved, and the potential impact. Keep it concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )

    # Health Researcher
    health_researcher = Agent(
        name="HealthResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research recent medical breakthroughs. Include 3 significant advances,
        their practical applications, and estimated timelines. Keep it concise (100 words).""",
        tools=[google_search],
        output_key="health_research",
    )

    # Finance Researcher
    finance_researcher = Agent(
        name="FinanceResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research current fintech trends. Include 3 key trends,
        their market implications, and the future outlook. Keep it concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",
    )

    # Aggregator Agent
    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Combine these three research findings into a single executive summary:

        **Technology Trends:** {tech_research}
        **Health Breakthroughs:** {health_research}
        **Finance Innovations:** {finance_research}

        Highlight common themes, surprising connections, and key takeaways.
        The final summary should be around 200 words.""",
        output_key="executive_summary",
    )

    # Parallel research team
    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    # Sequential wrapper to run parallel team first, then aggregator
    root_agent = SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_research_team, aggregator_agent],
    )

    print("✅ Parallel research system created (Tech + Health + Finance -> Aggregator)")
    return root_agent


# ============================================================================
# Pattern 4: Loop Workflow (Iterative Refinement)
# ============================================================================

def create_loop_story_refinement_system(retry_config):
    """
    Create a loop-based multi-agent system for iterative story refinement.
    A writer creates a draft, a critic reviews it, and a refiner improves it.
    The loop continues until the critic approves or max iterations are reached.
    """
    print("\n--- Creating Loop Story Refinement System ---")

    # Initial Writer Agent
    initial_writer_agent = Agent(
        name="InitialWriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Based on the user's prompt, write the first draft of a short story
        (around 100-150 words). Output only the story text, with no introduction or explanation.""",
        output_key="current_story",
    )

    # Critic Agent
    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a constructive story critic. Review the story provided below.
        Story: {current_story}

        Evaluate the story's plot, characters, and pacing.
        - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",
    )

    # Exit loop function
    def exit_loop():
        """Call this function when the critique is 'APPROVED'."""
        return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

    # Refiner Agent
    refiner_agent = Agent(
        name="RefinerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a story refiner. You have a story draft and critique.

        Story Draft: {current_story}
        Critique: {critique}

        - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
        - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

    # Loop Agent
    story_refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, refiner_agent],
        max_iterations=2,
    )

    # Sequential wrapper to run initial writer first, then loop
    root_agent = SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_writer_agent, story_refinement_loop],
    )

    print("✅ Loop refinement system created (Writer -> [Critic -> Refiner] loop)")
    return root_agent


# ============================================================================
# Main Execution
# ============================================================================

async def run_example(agent, query, title):
    """Run a single example with the given agent and query."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    print(f"\nQuery: {query}\n")

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(query)

    print("\n✅ Example completed!")


async def main():
    """Main function demonstrating all workflow patterns."""
    print("\n" + "="*80)
    print("  Day 1b: Multi-Agent Systems & Workflow Patterns")
    print("="*80)

    # Setup
    setup_api_key()
    retry_config = create_retry_config()

    # Choose which examples to run
    print("\nAvailable workflow patterns:")
    print("1. LLM-Based Orchestration (Research + Summarization)")
    print("2. Sequential Pipeline (Blog Post: Outline -> Write -> Edit)")
    print("3. Parallel Execution (Multi-Topic Research)")
    print("4. Loop Refinement (Iterative Story Improvement)")
    print("5. Run all examples")

    choice = input("\nSelect an option (1-5) or press Enter for all: ").strip()

    if choice in ["1", "5", ""]:
        # Example 1: LLM-Based Orchestration
        agent = create_llm_orchestrated_system(retry_config)
        await run_example(
            agent,
            "What are the latest advancements in quantum computing and what do they mean for AI?",
            "Example 1: LLM-Based Orchestration"
        )

    if choice in ["2", "5", ""]:
        # Example 2: Sequential Workflow
        agent = create_sequential_blog_pipeline(retry_config)
        await run_example(
            agent,
            "Write a blog post about the benefits of multi-agent systems for software developers",
            "Example 2: Sequential Workflow (Blog Pipeline)"
        )

    if choice in ["3", "5", ""]:
        # Example 3: Parallel Workflow
        agent = create_parallel_research_system(retry_config)
        await run_example(
            agent,
            "Run the daily executive briefing on Tech, Health, and Finance",
            "Example 3: Parallel Workflow (Multi-Topic Research)"
        )

    if choice in ["4", "5", ""]:
        # Example 4: Loop Workflow
        agent = create_loop_story_refinement_system(retry_config)
        await run_example(
            agent,
            "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map",
            "Example 4: Loop Workflow (Iterative Story Refinement)"
        )

    print("\n" + "="*80)
    print("  ✅ All selected examples completed!")
    print("="*80)

    print("\n📚 Key Takeaways:")
    print("- LLM Orchestration: Dynamic, flexible, but potentially unpredictable")
    print("- Sequential: Deterministic order, perfect for pipelines")
    print("- Parallel: Concurrent execution for speed with independent tasks")
    print("- Loop: Iterative refinement for quality improvement")
    print("\n🎯 Choose the right pattern based on your use case!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n\n⏸️  Script interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise
