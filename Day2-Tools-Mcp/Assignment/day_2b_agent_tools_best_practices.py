"""
Day 2b: Agent Tools Best Practices
This script demonstrates advanced agent tool patterns:
- Model Context Protocol (MCP) integration
- Long-Running Operations with human-in-the-loop
- Resumable workflows with state management

Prerequisites:
- pip install google-adk python-dotenv
- Node.js and npx installed (for MCP server demos)
- Create a .env file with your GOOGLE_API_KEY

Note: MCP examples require Node.js. Long-running operations work standalone.
"""

import os
import uuid
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.adk.tools.function_tool import FunctionTool
from google.adk.apps.app import App, ResumabilityConfig
from google.genai import types


def setup_api_key():
    """Configure the Gemini API key from .env file."""
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
# Example 1: Model Context Protocol (MCP) Integration
# ============================================================================

def demonstrate_mcp_concept():
    """Explain MCP concept (actual MCP server requires Node.js/npx)."""
    print("\n--- Model Context Protocol (MCP) ---")
    print("""
📡 What is MCP?

MCP is an open standard that lets agents connect to external services
without writing custom integration code.

Architecture:
    ┌──────────────────┐
    │   Your Agent     │
    │   (MCP Client)   │
    └────────┬─────────┘
             │
             │ Standard MCP Protocol
             │
        ┌────┴────┬────────┬────────┐
        │         │        │        │
        ▼         ▼        ▼        ▼
    ┌────────┐ ┌─────┐ ┌──────┐ ┌─────┐
    │ GitHub │ │Slack│ │ Maps │ │ ... │
    │ Server │ │ MCP │ │ MCP  │ │     │
    └────────┘ └─────┘ └──────┘ └─────┘

How to use MCP in ADK:

1. Install MCP server (e.g., via npx)
2. Create McpToolset with connection parameters
3. Add toolset to your agent
4. Agent can now use MCP tools!

Example (requires Node.js):
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
    from mcp import StdioServerParameters

    mcp_server = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-everything"],
                tool_filter=["getTinyImage"],
            ),
            timeout=30,
        )
    )

    agent = LlmAgent(
        model=Gemini(...),
        tools=[mcp_server],  # Add MCP tools to agent
    )

Available MCP Servers:
- Kaggle: Dataset and notebook operations
- GitHub: Repository and PR/issue management
- Google Maps: Location and directions
- Slack: Team communication
- Many more at: modelcontextprotocol.io/examples

""")
    print("✅ MCP concept explained\n")


# ============================================================================
# Example 2: Long-Running Operations (Human-in-the-Loop)
# ============================================================================

# Configuration
LARGE_ORDER_THRESHOLD = 5


def place_shipping_order(
    num_containers: int, destination: str, tool_context: ToolContext
) -> dict:
    """Places a shipping order. Requires approval if ordering more than 5 containers.

    This demonstrates a long-running operation that can pause for human approval.

    Args:
        num_containers: Number of containers to ship
        destination: Shipping destination
        tool_context: ADK provides this automatically

    Returns:
        Dictionary with order status
    """

    # SCENARIO 1: Small orders (≤5 containers) auto-approve
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }

    # SCENARIO 2: First call - Large order needs approval - PAUSE here
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination},
        )
        return {
            "status": "pending",
            "message": f"Order for {num_containers} containers requires approval",
        }

    # SCENARIO 3: Resumed call - Handle approval response - RESUME here
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} containers to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}",
        }


def create_shipping_system(retry_config):
    """Create a resumable shipping agent with approval workflow."""
    print("\n--- Creating Long-Running Operation System ---")

    # Create shipping agent with pausable tool
    shipping_agent = LlmAgent(
        name="shipping_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a shipping coordinator assistant.

        When users request to ship containers:
        1. Use the place_shipping_order tool
        2. If status is 'pending', inform user that approval is required
        3. After receiving the final result, provide a clear summary including:
           - Order status (approved/rejected)
           - Order ID (if available)
           - Number of containers and destination
        4. Keep responses concise but informative
        """,
        tools=[FunctionTool(func=place_shipping_order)],
    )

    # Wrap in resumable app - THIS IS KEY FOR LONG-RUNNING OPERATIONS!
    shipping_app = App(
        name="shipping_coordinator",
        root_agent=shipping_agent,
        resumability_config=ResumabilityConfig(is_resumable=True),
    )

    print("✅ Resumable shipping system created")
    print("🔧 Features:")
    print("  • Auto-approves small orders (≤5 containers)")
    print("  • Pauses for approval on large orders (>5 containers)")
    print("  • Maintains state across pause/resume")

    return shipping_app


# ============================================================================
# Helper Functions for Long-Running Operations
# ============================================================================

def check_for_approval(events):
    """Check if events contain an approval request.

    Returns:
        dict with approval details or None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None


def print_agent_response(events):
    """Print agent's text responses from events."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent > {part.text}")


def create_approval_response(approval_info, approved):
    """Create approval response message.

    Args:
        approval_info: Dict containing approval_id and invocation_id
        approved: Boolean indicating approval decision

    Returns:
        Content object with approval response
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )


# ============================================================================
# Workflow Function for Long-Running Operations
# ============================================================================

async def run_shipping_workflow(
    shipping_runner, session_service, query: str, auto_approve: bool = True
):
    """Runs a shipping workflow with approval handling.

    This demonstrates the complete pause/resume workflow:
    1. Send initial request
    2. Detect if agent paused for approval
    3. Resume with human decision

    Args:
        shipping_runner: The Runner instance
        session_service: Session service for state management
        query: User's shipping request
        auto_approve: Whether to auto-approve (simulates human decision)
    """

    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session
    await session_service.create_session(
        app_name="shipping_coordinator", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # STEP 1: Send initial request to agent
    async for event in shipping_runner.run_async(
        user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # STEP 2: Check if agent paused for approval
    approval_info = check_for_approval(events)

    # STEP 3: Handle approval workflow
    if approval_info:
        print(f"⏸️  Pausing for approval...")
        print(f"🤔 Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # Resume with approval decision
        async for event in shipping_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(approval_info, auto_approve),
            invocation_id=approval_info["invocation_id"],  # Critical: same ID to RESUME
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent > {part.text}")
    else:
        # No approval needed - order completed immediately
        print_agent_response(events)

    print(f"{'='*60}\n")


# ============================================================================
# Main Execution
# ============================================================================

async def test_mcp_concept():
    """Demonstrate MCP concepts (no actual MCP server needed)."""
    demonstrate_mcp_concept()


async def test_long_running_operations(retry_config):
    """Test long-running operations with approval workflow."""
    print("\n" + "="*80)
    print("  Example: Long-Running Operations (Human-in-the-Loop)")
    print("="*80)

    # Create the system
    shipping_app = create_shipping_system(retry_config)
    session_service = InMemorySessionService()
    shipping_runner = Runner(
        app=shipping_app,
        session_service=session_service,
    )

    print("\n📋 Testing Three Scenarios:\n")

    # Scenario 1: Small order - auto-approved
    print("1️⃣ Small Order (3 containers) - Auto-approve:")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 3 containers to Singapore"
    )

    # Scenario 2: Large order - approved
    print("2️⃣ Large Order (10 containers) - Approval Required - APPROVE:")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 10 containers to Rotterdam",
        auto_approve=True
    )

    # Scenario 3: Large order - rejected
    print("3️⃣ Large Order (8 containers) - Approval Required - REJECT:")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 8 containers to Los Angeles",
        auto_approve=False
    )

    print("✅ All long-running operation scenarios completed!")


async def main():
    """Main function demonstrating advanced agent tool patterns."""
    print("\n" + "="*80)
    print("  Day 2b: Agent Tools Best Practices")
    print("="*80)

    # Setup
    setup_api_key()
    retry_config = create_retry_config()

    print("\n📚 Advanced Patterns:")
    print("1. MCP Integration - Connect to external services")
    print("2. Long-Running Operations - Human-in-the-loop approvals")
    print("3. Resumable Workflows - Pause and resume with state management")

    # Example 1: MCP Concept (explanation only)
    await test_mcp_concept()

    # Example 2: Long-Running Operations
    await test_long_running_operations(retry_config)

    print("\n" + "="*80)
    print("  ✅ All examples completed!")
    print("="*80)

    print("\n📖 Key Takeaways:")
    print("- MCP: Connect to external services without custom integration")
    print("- LRO: Pause workflows for human approval or long-running tasks")
    print("- Resumability: Maintain state across conversation breaks")
    print("- Tool Context: Access approval status and request confirmation")

    print("\n🔑 When to Use Each Pattern:")
    print("┌───────────────────────┬──────────────────────────────────────────┐")
    print("│ Pattern               │ Use Case                                 │")
    print("├───────────────────────┼──────────────────────────────────────────┤")
    print("│ MCP Integration       │ Connect to external, standardized        │")
    print("│                       │ services (GitHub, databases, etc.)       │")
    print("├───────────────────────┼──────────────────────────────────────────┤")
    print("│ Long-Running Ops      │ Human approvals, compliance checks,      │")
    print("│                       │ or operations spanning time              │")
    print("└───────────────────────┴──────────────────────────────────────────┘")

    print("\n🎯 Next: Day 3 will cover State and Memory Management!")


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
