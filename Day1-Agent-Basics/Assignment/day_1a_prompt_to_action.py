"""
Day 1a: From Prompt to Action
This script demonstrates building your first AI Agent using Google ADK.
The agent can use tools like Google Search to answer questions.

Prerequisites:
- pip install google-adk python-dotenv
- Create a .env file with your GOOGLE_API_KEY
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
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
    """
    Configure retry options for handling transient errors.
    """
    return types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,  # Initial delay before first retry (in seconds)
        http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
    )


def create_basic_agent(retry_config):
    """
    Create a basic agent with Google Search tool.

    The agent can:
    - Answer questions
    - Use Google Search when it needs current information
    - Provide up-to-date responses
    """
    agent = Agent(
        name="helpful_assistant",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        description="A simple agent that can answer general questions.",
        instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
        tools=[google_search],
    )
    print("✅ Agent created with Google Search tool.")
    return agent


async def run_agent_query(agent, query):
    """
    Run a query through the agent.

    Args:
        agent: The Agent instance
        query: The question to ask the agent
    """
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(query)

    print(f"\n{'='*60}")
    print("Response received!")
    print(f"{'='*60}\n")


async def main():
    """
    Main function demonstrating the agent's capabilities.
    """
    print("\n" + "="*60)
    print("Day 1a: From Prompt to Action")
    print("Building Your First AI Agent")
    print("="*60 + "\n")

    # Setup
    setup_api_key()
    retry_config = create_retry_config()
    agent = create_basic_agent(retry_config)

    # Example 1: Query about ADK
    print("\n--- Example 1: Asking about Agent Development Kit ---")
    await run_agent_query(
        agent,
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )

    # Example 2: Query requiring current information
    print("\n--- Example 2: Asking for current information ---")
    await run_agent_query(
        agent,
        "What's the weather in London?"
    )

    # Example 3: Your custom query
    print("\n--- Example 3: Try your own query ---")
    custom_query = input("\nEnter your question (or press Enter to skip): ").strip()
    if custom_query:
        await run_agent_query(agent, custom_query)

    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60 + "\n")

    print("Key Takeaways:")
    print("- The agent doesn't just respond—it REASONS and ACTS")
    print("- It knows when to use tools like Google Search")
    print("- It can provide up-to-date information")
    print("\nNext: Check out day_1b_agent_architectures.py for multi-agent systems!")


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
