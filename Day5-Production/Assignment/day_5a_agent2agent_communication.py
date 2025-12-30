"""
Day 5a: Agent2Agent (A2A) Communication

This script covers:
- Understanding the A2A protocol and when to use it
- Common A2A architecture patterns (cross-framework, cross-language, cross-organization)
- Exposing an ADK agent via A2A using to_a2a()
- Consuming remote agents using RemoteA2aAgent
- Building a product catalog integration system

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
import json
import time
import subprocess
import requests
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ============================================================================
# Setup and Configuration
# ============================================================================

# Load environment variables from .env file
load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found in environment variables")
    print("   Please make sure you have a .env file with GOOGLE_API_KEY set")
    exit(1)

print("✅ ADK components imported successfully.")
print("✅ API key loaded from .env file")

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
# Section 1: Product Catalog Agent (To Be Exposed via A2A)
# ============================================================================


def get_product_info(product_name: str) -> str:
    """Get product information for a given product.

    Args:
        product_name: Name of the product (e.g., "iPhone 15 Pro", "MacBook Pro")

    Returns:
        Product information as a string
    """
    # Mock product catalog - in production, this would query a real database
    product_catalog = {
        "iphone 15 pro": "iPhone 15 Pro, $999, Low Stock (8 units), 128GB, Titanium finish",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, In Stock (31 units), 256GB, Phantom Black",
        "dell xps 15": 'Dell XPS 15, $1,299, In Stock (45 units), 15.6" display, 16GB RAM, 512GB SSD',
        "macbook pro 14": 'MacBook Pro 14", $1,999, In Stock (22 units), M3 Pro chip, 18GB RAM, 512GB SSD',
        "sony wh-1000xm5": "Sony WH-1000XM5 Headphones, $399, In Stock (67 units), Noise-canceling, 30hr battery",
        "ipad air": 'iPad Air, $599, In Stock (28 units), 10.9" display, 64GB',
        "lg ultrawide 34": 'LG UltraWide 34" Monitor, $499, Out of Stock, Expected: Next week',
    }

    product_lower = product_name.lower().strip()

    if product_lower in product_catalog:
        return f"Product: {product_catalog[product_lower]}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"Sorry, I don't have information for {product_name}. Available products: {available}"


def create_product_catalog_agent():
    """Create the Product Catalog Agent"""

    product_catalog_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="product_catalog_agent",
        description="External vendor's product catalog agent that provides product information and availability.",
        instruction="""
        You are a product catalog specialist from an external vendor.
        When asked about products, use the get_product_info tool to fetch data from the catalog.
        Provide clear, accurate product information including price, availability, and specs.
        If asked about multiple products, look up each one.
        Be professional and helpful.
        """,
        tools=[get_product_info],
    )

    print("✅ Product Catalog Agent created successfully!")
    print("   Model: gemini-2.5-flash-lite")
    print("   Tool: get_product_info()")
    print("   Ready to be exposed via A2A...")

    return product_catalog_agent


# ============================================================================
# Section 2: Expose Agent via A2A
# ============================================================================


def create_product_catalog_server_file():
    """Create a standalone Python file for the A2A server"""

    server_code = f'''
import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def get_product_info(product_name: str) -> str:
    """Get product information for a given product."""
    product_catalog = {{
        "iphone 15 pro": "iPhone 15 Pro, $999, Low Stock (8 units), 128GB, Titanium finish",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, In Stock (31 units), 256GB, Phantom Black",
        "dell xps 15": "Dell XPS 15, $1,299, In Stock (45 units), 15.6\\" display, 16GB RAM, 512GB SSD",
        "macbook pro 14": "MacBook Pro 14\\", $1,999, In Stock (22 units), M3 Pro chip, 18GB RAM, 512GB SSD",
        "sony wh-1000xm5": "Sony WH-1000XM5 Headphones, $399, In Stock (67 units), Noise-canceling, 30hr battery",
        "ipad air": "iPad Air, $599, In Stock (28 units), 10.9\\" display, 64GB",
        "lg ultrawide 34": "LG UltraWide 34\\" Monitor, $499, Out of Stock, Expected: Next week",
    }}

    product_lower = product_name.lower().strip()

    if product_lower in product_catalog:
        return f"Product: {{product_catalog[product_lower]}}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"Sorry, I don't have information for {{product_name}}. Available products: {{available}}"

product_catalog_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="product_catalog_agent",
    description="External vendor's product catalog agent that provides product information and availability.",
    instruction="""
    You are a product catalog specialist from an external vendor.
    When asked about products, use the get_product_info tool to fetch data from the catalog.
    Provide clear, accurate product information including price, availability, and specs.
    If asked about multiple products, look up each one.
    Be professional and helpful.
    """,
    tools=[get_product_info]
)

# Create the A2A app
app = to_a2a(product_catalog_agent, port=8001)
'''

    # Write to temp file
    server_file = "/tmp/product_catalog_server.py"
    with open(server_file, "w") as f:
        f.write(server_code)

    print(f"📝 Product Catalog server code saved to {server_file}")
    return server_file


def start_product_catalog_server():
    """Start the Product Catalog Agent server in the background"""

    # Create server file
    server_file = create_product_catalog_server_file()

    # Start uvicorn server in background
    print("\n🚀 Starting Product Catalog Agent server...")
    print("   Waiting for server to be ready...")

    server_process = subprocess.Popen(
        [
            "uvicorn",
            "product_catalog_server:app",
            "--host",
            "localhost",
            "--port",
            "8001",
        ],
        cwd="/tmp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ},
    )

    # Wait for server to start
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                "http://localhost:8001/.well-known/agent-card.json", timeout=1
            )
            if response.status_code == 200:
                print(f"\n✅ Product Catalog Agent server is running!")
                print(f"   Server URL: http://localhost:8001")
                print(
                    f"   Agent card: http://localhost:8001/.well-known/agent-card.json"
                )
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\n⚠️  Server may not be ready yet. Check manually if needed.")

    return server_process


def view_agent_card():
    """Fetch and display the agent card"""

    try:
        response = requests.get(
            "http://localhost:8001/.well-known/agent-card.json", timeout=5
        )

        if response.status_code == 200:
            agent_card = response.json()
            print("\n📋 Product Catalog Agent Card:")
            print(json.dumps(agent_card, indent=2))

            print("\n✨ Key Information:")
            print(f"   Name: {agent_card.get('name')}")
            print(f"   Description: {agent_card.get('description')}")
            print(f"   URL: {agent_card.get('url')}")
            print(
                f"   Skills: {len(agent_card.get('skills', []))} capabilities exposed"
            )
        else:
            print(f"❌ Failed to fetch agent card: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching agent card: {e}")


# ============================================================================
# Section 4: Create Customer Support Agent (Consumer)
# ============================================================================


def create_customer_support_agent():
    """Create the Customer Support Agent that consumes the Product Catalog Agent"""

    # Create a RemoteA2aAgent that connects to Product Catalog Agent
    remote_product_catalog_agent = RemoteA2aAgent(
        name="product_catalog_agent",
        description="Remote product catalog agent from external vendor that provides product information.",
        agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
    )

    print("\n✅ Remote Product Catalog Agent proxy created!")
    print(f"   Connected to: http://localhost:8001")
    print(f"   Agent card: http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}")
    print("   The Customer Support Agent can now use this like a local sub-agent!")

    # Create the Customer Support Agent
    customer_support_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="customer_support_agent",
        description="A customer support assistant that helps customers with product inquiries and information.",
        instruction="""
        You are a friendly and professional customer support agent.

        When customers ask about products:
        1. Use the product_catalog_agent sub-agent to look up product information
        2. Provide clear answers about pricing, availability, and specifications
        3. If a product is out of stock, mention the expected availability
        4. Be helpful and professional!

        Always get product information from the product_catalog_agent before answering customer questions.
        """,
        sub_agents=[remote_product_catalog_agent],
    )

    print("\n✅ Customer Support Agent created!")
    print("   Model: gemini-2.5-flash-lite")
    print("   Sub-agents: 1 (remote Product Catalog Agent via A2A)")
    print("   Ready to help customers!")

    return customer_support_agent


# ============================================================================
# Section 5: Test A2A Communication
# ============================================================================


async def test_a2a_communication(customer_support_agent, user_query: str):
    """Test the A2A communication"""

    # Setup session management
    session_service = InMemorySessionService()

    app_name = "support_app"
    user_id = "demo_user"
    session_id = f"demo_session_{uuid.uuid4().hex[:8]}"

    # Create session
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    # Create runner
    runner = Runner(
        agent=customer_support_agent,
        app_name=app_name,
        session_service=session_service,
    )

    # Create user message
    test_content = types.Content(parts=[types.Part(text=user_query)])

    # Display query
    print(f"\n👤 Customer: {user_query}")
    print(f"\n🎧 Support Agent response:")
    print("-" * 60)

    # Run the agent
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=test_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)

    print("-" * 60)


# ============================================================================
# Main Function
# ============================================================================


async def main():
    """Run the A2A communication demo"""

    print("\n" + "=" * 80)
    print("DAY 5A: AGENT2AGENT (A2A) COMMUNICATION")
    print("=" * 80)

    print("\n📚 What You'll Learn:")
    print("• Understanding the A2A protocol")
    print("• Exposing agents via A2A using to_a2a()")
    print("• Consuming remote agents using RemoteA2aAgent")
    print("• Building cross-organization agent systems")

    # Section 1: Create Product Catalog Agent
    print("\n" + "=" * 80)
    print("SECTION 1: Create Product Catalog Agent (To Be Exposed)")
    print("=" * 80)
    product_catalog_agent = create_product_catalog_agent()

    # Section 2 & 3: Expose via A2A and Start Server
    print("\n" + "=" * 80)
    print("SECTION 2 & 3: Expose via A2A and Start Server")
    print("=" * 80)
    server_process = start_product_catalog_server()

    # View the agent card
    view_agent_card()

    # Section 4: Create Customer Support Agent
    print("\n" + "=" * 80)
    print("SECTION 4: Create Customer Support Agent (Consumer)")
    print("=" * 80)
    customer_support_agent = create_customer_support_agent()

    # Section 5: Test A2A Communication
    print("\n" + "=" * 80)
    print("SECTION 5: Test A2A Communication")
    print("=" * 80)
    print("\n🧪 Testing A2A Communication...")

    # Test 1
    await test_a2a_communication(
        customer_support_agent, "Can you tell me about the iPhone 15 Pro? Is it in stock?"
    )

    # Test 2
    await test_a2a_communication(
        customer_support_agent,
        "I'm looking for a laptop. Can you compare the Dell XPS 15 and MacBook Pro 14 for me?",
    )

    # Test 3
    await test_a2a_communication(
        customer_support_agent,
        "Do you have the Sony WH-1000XM5 headphones? What's the price?",
    )

    # Cleanup
    print("\n" + "=" * 80)
    print("CLEANUP")
    print("=" * 80)
    print("\n🛑 Stopping Product Catalog server...")
    server_process.terminate()
    server_process.wait()
    print("✅ Server stopped")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\n🎯 Key Takeaways:")
    print("✅ A2A protocol enables cross-organization agent communication")
    print("✅ to_a2a() makes agents accessible with auto-generated agent cards")
    print("✅ RemoteA2aAgent consumes remote agents as local sub-agents")
    print("✅ Agent cards describe capabilities at /.well-known/agent-card.json")

    print("\n📊 A2A vs Local Sub-Agents:")
    print("Use A2A when:")
    print("   • Agents are in different codebases/organizations")
    print("   • Need cross-language/framework communication")
    print("   • Formal API contract required")
    print("\nUse Local Sub-Agents when:")
    print("   • Same codebase/internal to your team")
    print("   • Need low latency")
    print("   • Same language/framework")

    print("\n📚 Learn More:")
    print("• A2A Protocol: https://a2a-protocol.org/")
    print("• Exposing Agents: https://google.github.io/adk-docs/a2a/quickstart-exposing/")
    print("• Consuming Agents: https://google.github.io/adk-docs/a2a/quickstart-consuming/")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
