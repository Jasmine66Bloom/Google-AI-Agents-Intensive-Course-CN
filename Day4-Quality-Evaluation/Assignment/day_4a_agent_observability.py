"""
Day 4a: Agent Observability - Logs, Traces & Metrics

This notebook covers:
- Understanding what agent observability is and why it's important
- Using ADK web UI for interactive debugging
- Implementing LoggingPlugin for production observability
- Creating custom plugins and callbacks
- Understanding logs, traces, and metrics

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.genai import types
from typing import List

# ============================================================================
# Setup and Configuration
# ============================================================================

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found in environment variables")
    print("   Please make sure you have a .env file with GOOGLE_API_KEY set")
    exit(1)

print("✅ ADK components imported successfully.")
print("✅ API key loaded from .env file")

# ============================================================================
# Configure Logging
# ============================================================================


def setup_logging():
    """Set up logging configuration with DEBUG level"""
    # Clean up any previous logs
    for log_file in ["logger.log", "web.log", "tunnel.log"]:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"🧹 Cleaned up {log_file}")

    # Configure logging with DEBUG log level
    logging.basicConfig(
        filename="logger.log",
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
    )

    print("✅ Logging configured")


# ============================================================================
# Configure Retry Options
# ============================================================================

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# Section 2: Research Paper Finder Agent (Intentionally Broken)
# ============================================================================


def count_papers_broken(papers: str):
    """
    This function counts the number of papers in a list of strings.

    INTENTIONAL BUG: Takes str instead of List[str]

    Args:
      papers: A list of strings, where each string is a research paper.
    Returns:
      The number of papers in the list.
    """
    return len(papers)


def count_papers_fixed(papers: List[str]):
    """
    This function counts the number of papers in a list of strings.

    FIXED: Now correctly takes List[str]

    Args:
      papers: A list of strings, where each string is a research paper.
    Returns:
      The number of papers in the list.
    """
    return len(papers)


def create_research_agent_broken():
    """Create a research agent with intentional bug for debugging practice"""

    # Google Search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="""Use the google_search tool to find information on the given topic.
        Return the raw search results.
        If the user asks for a list of papers, then give them the list of research papers
        you found and not the summary.""",
        tools=[google_search],
    )

    # Root agent with BROKEN count_papers tool
    root_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Your task is to find research papers and count them.

        You MUST ALWAYS follow these steps:
        1) Find research papers on the user provided topic using the 'google_search_agent'.
        2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
        3) Return both the list of research papers and the total number of papers.
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers_broken],
    )

    return root_agent


def create_research_agent_fixed():
    """Create a research agent with the bug fixed"""

    # Google Search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="""Use the google_search tool to find information on the given topic.
        Return the raw search results.
        If the user asks for a list of papers, then give them the list of research papers
        you found and not the summary.""",
        tools=[google_search],
    )

    # Root agent with FIXED count_papers tool
    root_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Your task is to find research papers and count them.

        You MUST ALWAYS follow these steps:
        1) Find research papers on the user provided topic using the 'google_search_agent'.
        2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
        3) Return both the list of research papers and the total number of papers.
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers_fixed],
    )

    return root_agent


# ============================================================================
# Section 3: Custom Plugin Example
# ============================================================================


class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1
        logging.info(f"[Plugin] Agent run count: {self.agent_count}")
        print(f"[CountPlugin] Agent invocation #{self.agent_count}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        logging.info(f"[Plugin] LLM request count: {self.llm_request_count}")
        print(f"[CountPlugin] LLM request #{self.llm_request_count}")


# ============================================================================
# Section 3: Using LoggingPlugin for Production
# ============================================================================


def create_agent_with_logging_plugin():
    """Create research agent with LoggingPlugin for comprehensive observability"""

    # Google search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="Use the google_search tool to find information on the given topic. Return the raw search results.",
        tools=[google_search],
    )

    # Root agent with FIXED tool
    research_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Your task is to find research papers and count them.

       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'.
       2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
       3) Return both the list of research papers and the total number of papers.
       """,
        tools=[AgentTool(agent=google_search_agent), count_papers_fixed],
    )

    # Create runner with LoggingPlugin
    runner = InMemoryRunner(
        agent=research_agent,
        plugins=[LoggingPlugin()],  # Handles standard Observability logging
    )

    return runner


# ============================================================================
# Demonstration Functions
# ============================================================================


async def demo_broken_agent():
    """Demonstrate the broken agent for debugging practice"""
    print("\n" + "=" * 80)
    print("DEMO: Broken Agent (for debugging practice)")
    print("=" * 80)
    print("\n🐛 This agent has an intentional bug in the count_papers tool")
    print("The tool expects a 'str' but should accept 'List[str]'")
    print("\n👉 In a real scenario, you would:")
    print("   1. Run 'adk web --log_level DEBUG' to start the web UI")
    print("   2. Test the agent with: 'Find latest quantum computing papers'")
    print("   3. Use the Events tab and Traces to find the bug")
    print("   4. Look at the function_call to see incorrect parameter types")

    agent = create_research_agent_broken()
    runner = InMemoryRunner(agent=agent)

    print("\n⚠️  Note: This is a demo script. To actually debug:")
    print("   - Create an agent folder: adk create research-agent")
    print("   - Copy the agent definition to agent.py")
    print("   - Run: adk web --log_level DEBUG")
    print("   - Use the web UI to interact and debug")


async def demo_logging_plugin():
    """Demonstrate LoggingPlugin for production observability"""
    print("\n" + "=" * 80)
    print("DEMO: Research Agent with LoggingPlugin")
    print("=" * 80)

    setup_logging()

    runner = create_agent_with_logging_plugin()

    print("\n🚀 Running agent with LoggingPlugin...")
    print("📊 Watch the comprehensive logging output:\n")

    response = await runner.run_debug("Find recent papers on quantum computing")

    print("\n✅ Agent execution complete!")
    print("\n📋 Key Observations:")
    print("• LoggingPlugin automatically captured all agent activity")
    print("• Logs include: user messages, agent responses, tool calls, timing data")
    print("• Check logger.log file for detailed DEBUG logs")
    print("• This approach scales for production systems")


async def demo_custom_plugin():
    """Demonstrate creating and using a custom plugin"""
    print("\n" + "=" * 80)
    print("DEMO: Custom Plugin (CountInvocationPlugin)")
    print("=" * 80)

    setup_logging()

    # Create agent with custom plugin
    agent = create_research_agent_fixed()
    custom_plugin = CountInvocationPlugin()

    runner = InMemoryRunner(
        agent=agent,
        plugins=[custom_plugin],
    )

    print("\n🎯 Running agent with custom CountInvocationPlugin...")
    print("This plugin counts agent invocations and LLM requests\n")

    response = await runner.run_debug("Find papers on machine learning")

    print("\n📊 Custom Plugin Statistics:")
    print(f"   • Agent invocations: {custom_plugin.agent_count}")
    print(f"   • LLM requests: {custom_plugin.llm_request_count}")
    print("\n💡 Custom plugins allow you to add any observability logic you need!")


# ============================================================================
# Main Function
# ============================================================================


async def main():
    """Run all observability demonstrations"""

    print("\n" + "=" * 80)
    print("DAY 4A: AGENT OBSERVABILITY")
    print("=" * 80)

    print("\n📚 What You'll Learn:")
    print("• Debugging agents with ADK web UI and DEBUG logs")
    print("• Using LoggingPlugin for production observability")
    print("• Creating custom plugins for specialized needs")
    print("• Understanding logs, traces, and metrics")

    # Demo 1: Broken Agent
    await demo_broken_agent()

    # Demo 2: LoggingPlugin
    await demo_logging_plugin()

    # Demo 3: Custom Plugin
    await demo_custom_plugin()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n❓ When to use which type of logging?")
    print("1. Development debugging → Use 'adk web --log_level DEBUG'")
    print("2. Common production observability → Use LoggingPlugin()")
    print("3. Custom requirements → Build Custom Callbacks and Plugins")

    print("\n🎯 Key Takeaways:")
    print("✅ Core debugging pattern: symptom → logs → root cause → fix")
    print("✅ ADK web UI provides interactive debugging with traces")
    print("✅ LoggingPlugin handles standard observability automatically")
    print("✅ Custom plugins enable specialized monitoring")

    print("\n📚 Learn More:")
    print("• ADK Observability: https://google.github.io/adk-docs/observability/logging/")
    print("• Custom Plugins: https://google.github.io/adk-docs/plugins/")
    print("• Cloud Trace Integration: https://google.github.io/adk-docs/observability/cloud-trace/")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
