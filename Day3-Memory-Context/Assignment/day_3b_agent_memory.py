"""
Day 3b: Memory Management - Part 2 - Memory

This notebook covers:
- Initialize MemoryService and integrate with your agent
- Transfer session data to memory storage
- Search and retrieve memories
- Automate memory storage and retrieval
- Understand memory consolidation (conceptual overview)

What is Memory?
- Session = Short-term memory (single conversation)
- Memory = Long-term knowledge (across multiple conversations)

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
from typing import Any, Dict

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
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

APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

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
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default"
):
    """Helper function to run queries in a session and display responses."""
    print(f"\n### Session: {session_id}")

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    for query in user_queries:
        print(f"\nUser > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")


print("✅ Helper functions defined.")

# ============================================================================
# Section 3: Initialize MemoryService
# ============================================================================


def section_3_initialize_memory():
    """Initialize Memory Service and create an agent with memory support"""
    global memory_service, session_service, user_agent, runner

    # Step 1: Initialize Memory Service
    memory_service = InMemoryMemoryService()

    # Step 2: Create agent
    user_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="MemoryDemoAgent",
        instruction="Answer user questions in simple words.",
    )

    # Step 3: Create Session Service
    session_service = InMemorySessionService()

    # Step 4: Create runner with BOTH services
    runner = Runner(
        agent=user_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent and Runner created with memory support!")


# ============================================================================
# Section 4: Ingest Session Data into Memory
# ============================================================================


async def section_4_ingest_session():
    """Demonstrate how to ingest session data into memory"""

    # Have a conversation
    await run_session(
        runner,
        "My favorite color is blue-green. Can you write a Haiku about it?",
        "conversation-01",
    )

    # Verify the conversation was captured
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )

    print("\n📝 Session contains:")
    for event in session.events:
        text = (
            event.content.parts[0].text[:60]
            if event.content and event.content.parts
            else "(empty)"
        )
        print(f"  {event.content.role}: {text}...")

    # Transfer session to memory
    await memory_service.add_session_to_memory(session)
    print("\n✅ Session added to memory!")


# ============================================================================
# Section 5: Enable Memory Retrieval in Your Agent
# ============================================================================


def section_5_enable_retrieval():
    """Create an agent with load_memory tool for reactive retrieval"""
    global user_agent, runner

    # Create agent with load_memory tool
    user_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="MemoryDemoAgent",
        instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
        tools=[load_memory],
    )

    # Create a new runner with the updated agent
    runner = Runner(
        agent=user_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent with load_memory tool created.")


async def test_manual_memory_workflow():
    """Complete manual workflow test: ingest → store → retrieve"""

    # Test 1: Save birthday information
    await run_session(runner, "My birthday is on March 15th.", "birthday-session-01")

    # Manually save the session to memory
    birthday_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01"
    )
    await memory_service.add_session_to_memory(birthday_session)
    print("\n✅ Birthday session saved to memory!")

    # Test 2: Retrieve in a NEW session
    await run_session(runner, "When is my birthday?", "birthday-session-02")


async def manual_memory_search():
    """Demonstrate direct memory search from code"""

    # Search for color preferences
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="What is the user's favorite color?"
    )

    print("\n🔍 Search Results:")
    print(f"  Found {len(search_response.memories)} relevant memories")
    print()

    for memory in search_response.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{memory.author}]: {text}...")


# ============================================================================
# Section 6: Automating Memory Storage
# ============================================================================


async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


def section_6_automatic_memory():
    """Create an agent with automatic memory saving using callbacks"""
    global auto_memory_agent, auto_runner

    # Agent with automatic memory saving
    auto_memory_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="AutoMemoryAgent",
        instruction="Answer user questions.",
        tools=[preload_memory],
        after_agent_callback=auto_save_to_memory,
    )

    # Create a runner for the auto-save agent
    auto_runner = Runner(
        agent=auto_memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent created with automatic memory saving!")


async def test_automatic_memory():
    """Test automatic memory storage and retrieval"""

    # Test 1: Tell the agent about a gift
    await run_session(
        auto_runner,
        "I gifted a new toy to my nephew on his 1st birthday!",
        "auto-save-test",
    )

    # Test 2: Ask about the gift in a NEW session
    await run_session(
        auto_runner,
        "What did I gift my nephew?",
        "auto-save-test-2",
    )


# ============================================================================
# Example Usage
# ============================================================================


async def main():
    """Example usage of the different sections"""

    # Section 3: Initialize Memory
    print("\n" + "=" * 80)
    print("SECTION 3: Initialize MemoryService")
    print("=" * 80)
    section_3_initialize_memory()

    # Section 4: Ingest Session Data
    print("\n" + "=" * 80)
    print("SECTION 4: Ingest Session Data into Memory")
    print("=" * 80)
    await section_4_ingest_session()

    # Section 5: Enable Memory Retrieval
    print("\n" + "=" * 80)
    print("SECTION 5: Enable Memory Retrieval in Your Agent")
    print("=" * 80)
    section_5_enable_retrieval()

    # Test with color query
    await run_session(runner, "What is my favorite color?", "color-test")

    # Complete manual workflow
    print("\n--- Complete Manual Workflow Test ---")
    await test_manual_memory_workflow()

    # Manual memory search
    print("\n--- Manual Memory Search ---")
    await manual_memory_search()

    # Section 6: Automating Memory Storage
    print("\n" + "=" * 80)
    print("SECTION 6: Automating Memory Storage")
    print("=" * 80)
    section_6_automatic_memory()

    # Test automatic memory
    await test_automatic_memory()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
