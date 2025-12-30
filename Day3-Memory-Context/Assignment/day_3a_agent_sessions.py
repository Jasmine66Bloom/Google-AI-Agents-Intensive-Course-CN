"""
Day 3a: Memory Management - Part 1 - Sessions

This notebook covers:
- What sessions are and how to use them in your agent
- How to build stateful agents with sessions and events
- How to persist sessions in a database
- Context management practices such as context compaction
- Best practices for sharing session State

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
from typing import Any, Dict

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

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
# Configuration
# ============================================================================

APP_NAME = "default"
USER_ID = "default"
SESSION = "default"
MODEL_NAME = "gemini-2.5-flash-lite"

# Configure Retry Options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# Helper Functions
# ============================================================================


async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    """
    Helper function that manages a complete conversation session, handling session
    creation/retrieval, query processing, and response streaming.
    """
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


print("✅ Helper functions defined.")

# ============================================================================
# Section 2: Implementing Our First Stateful Agent
# ============================================================================


def section_2_stateful_agent():
    """Implementing a stateful agent with InMemorySessionService"""
    global session_service, runner

    # Step 1: Create the LLM Agent
    root_agent = Agent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot",
    )

    # Step 2: Set up Session Management
    session_service = InMemorySessionService()

    # Step 3: Create the Runner
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    print("✅ Stateful agent initialized!")
    print(f"   - Application: {APP_NAME}")
    print(f"   - User: {USER_ID}")
    print(f"   - Using: {session_service.__class__.__name__}")


# ============================================================================
# Section 3: Persistent Sessions with DatabaseSessionService
# ============================================================================


def section_3_persistent_sessions():
    """Implementing persistent sessions with DatabaseSessionService"""
    global session_service, runner

    # Step 1: Create the same agent (using LlmAgent this time)
    chatbot_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot with persistent memory",
    )

    # Step 2: Switch to DatabaseSessionService
    db_url = "sqlite:///my_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)

    # Step 3: Create a new runner with persistent storage
    runner = Runner(
        agent=chatbot_agent, app_name=APP_NAME, session_service=session_service
    )

    print("✅ Upgraded to persistent sessions!")
    print(f"   - Database: my_agent_data.db")
    print(f"   - Sessions will survive restarts!")


def inspect_database():
    """Inspect the SQLite database to see stored events"""
    import sqlite3

    with sqlite3.connect("my_agent_data.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)


# ============================================================================
# Section 4: Context Compaction
# ============================================================================


def section_4_context_compaction():
    """Implementing Context Compaction to reduce context size"""
    global session_service, research_runner_compacting

    chatbot_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot with persistent memory",
    )

    # Re-define our app with Events Compaction enabled
    research_app_compacting = App(
        name="research_app_compacting",
        root_agent=chatbot_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 invocations
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )

    db_url = "sqlite:///my_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)

    # Create a new runner for our upgraded app
    research_runner_compacting = Runner(
        app=research_app_compacting, session_service=session_service
    )

    print("✅ Research App upgraded with Events Compaction!")


async def verify_compaction(session_id: str):
    """Verify that compaction occurred by checking for summary event"""
    final_session = await session_service.get_session(
        app_name="research_app_compacting", user_id=USER_ID, session_id=session_id
    )

    print("--- Searching for Compaction Summary Event ---")
    found_summary = False
    for event in final_session.events:
        if event.actions and event.actions.compaction:
            print("\n✅ SUCCESS! Found the Compaction Event:")
            print(f"  Author: {event.author}")
            print(f"\n Compacted information: {event}")
            found_summary = True
            break

    if not found_summary:
        print(
            "\n❌ No compaction event found. Try increasing the number of turns in the demo."
        )


# ============================================================================
# Section 5: Working with Session State
# ============================================================================

# Define scope levels for state keys
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")


def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    Args:
        user_name: The username to store in session state
        country: The name of the user's country
    """
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country
    return {"status": "success"}


def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.
    """
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")
    return {"status": "success", "user_name": user_name, "country": country}


def section_5_session_state():
    """Creating an Agent with Session State Tools"""
    global session_service, runner

    # Create an agent with session state tools
    root_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="""A text chatbot.
        Tools for managing user context:
        * To record username and country when provided use `save_userinfo` tool.
        * To fetch username and country when required use `retrieve_userinfo` tool.
        """,
        tools=[save_userinfo, retrieve_userinfo],
    )

    # Set up session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, session_service=session_service, app_name="default"
    )

    print("✅ Agent with session state tools initialized!")


async def inspect_session_state(session_id: str):
    """Inspect the session state to see stored data"""
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )

    print("Session State Contents:")
    print(session.state)
    print("\n🔍 Notice the 'user:name' and 'user:country' keys storing our data!")


# ============================================================================
# Cleanup
# ============================================================================


def cleanup():
    """Clean up database files"""
    if os.path.exists("my_agent_data.db"):
        os.remove("my_agent_data.db")
    print("✅ Cleaned up old database files")


# ============================================================================
# Example Usage
# ============================================================================


async def main():
    """Example usage of the different sections"""

    # Section 2: Stateful Agent with InMemorySessionService
    print("\n" + "=" * 80)
    print("SECTION 2: Stateful Agent with InMemorySessionService")
    print("=" * 80)
    section_2_stateful_agent()

    await run_session(
        runner,
        [
            "Hi, I am Sam! What is the capital of United States?",
            "Hello! What is my name?",
        ],
        "stateful-agentic-session",
    )

    # Section 3: Persistent Sessions
    print("\n" + "=" * 80)
    print("SECTION 3: Persistent Sessions with DatabaseSessionService")
    print("=" * 80)
    section_3_persistent_sessions()

    await run_session(
        runner,
        [
            "Hi, I am Sam! What is the capital of the United States?",
            "Hello! What is my name?",
        ],
        "test-db-session-01",
    )

    # Inspect database
    print("\n--- Database Contents ---")
    inspect_database()

    # Section 4: Context Compaction
    print("\n" + "=" * 80)
    print("SECTION 4: Context Compaction")
    print("=" * 80)
    section_4_context_compaction()

    # Run multiple turns to trigger compaction
    await run_session(
        research_runner_compacting,
        "What is the latest news about AI in healthcare?",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "Are there any new developments in drug discovery?",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "Tell me more about the second development you found.",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "Who are the main companies involved in that?",
        "compaction_demo",
    )

    # Verify compaction
    await verify_compaction("compaction_demo")

    # Section 5: Session State
    print("\n" + "=" * 80)
    print("SECTION 5: Working with Session State")
    print("=" * 80)
    section_5_session_state()

    await run_session(
        runner,
        [
            "Hi there, how are you doing today? What is my name?",
            "My name is Sam. I'm from Poland.",
            "What is my name? Which country am I from?",
        ],
        "state-demo-session",
    )

    # Inspect session state
    await inspect_session_state("state-demo-session")

    # Test state isolation
    await run_session(
        runner,
        ["Hi there, how are you doing today? What is my name?"],
        "new-isolated-session",
    )

    # Cleanup
    cleanup()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
