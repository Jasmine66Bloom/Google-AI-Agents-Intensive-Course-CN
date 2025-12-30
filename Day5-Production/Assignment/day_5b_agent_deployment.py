"""
Day 5b: Deploy ADK Agent to Production

This script covers:
- Building a production-ready ADK agent
- Understanding deployment options (Agent Engine, Cloud Run, GKE)
- Creating deployment configuration files
- Deploying to Vertex AI Agent Engine using ADK CLI
- Testing deployed agents
- Understanding Memory Bank for long-term memory
- Cost management and cleanup

Note: This script demonstrates the concepts and provides code examples.
Actual deployment requires a Google Cloud Platform account with billing enabled.

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
import json
from dotenv import load_dotenv

# ============================================================================
# Setup and Configuration
# ============================================================================

# Load environment variables from .env file
load_dotenv()

print("✅ Imports completed successfully")
print("✅ Environment variables loaded from .env file")

# ============================================================================
# Agent Code Template
# ============================================================================

AGENT_CODE_TEMPLATE = '''"""
Production Weather Assistant Agent

This agent provides weather information for cities using a mock database.
In production, this would integrate with a real weather API.
"""

from google.adk.agents import Agent
import vertexai
import os

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

def get_weather(city: str) -> dict:
    """
    Returns weather information for a given city.

    This is a TOOL that the agent can call when users ask about weather.
    In production, this would call a real weather API (e.g., OpenWeatherMap).
    For this demo, we use mock data.

    Args:
        city: Name of the city (e.g., "Tokyo", "New York")

    Returns:
        dict: Dictionary with status and weather report or error message
    """
    # Mock weather database with structured responses
    weather_data = {
        "san francisco": {"status": "success", "report": "The weather in San Francisco is sunny with a temperature of 72°F (22°C)."},
        "new york": {"status": "success", "report": "The weather in New York is cloudy with a temperature of 65°F (18°C)."},
        "london": {"status": "success", "report": "The weather in London is rainy with a temperature of 58°F (14°C)."},
        "tokyo": {"status": "success", "report": "The weather in Tokyo is clear with a temperature of 70°F (21°C)."},
        "paris": {"status": "success", "report": "The weather in Paris is partly cloudy with a temperature of 68°F (20°C)."}
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available_cities = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available. Try: {available_cities}"
        }

root_agent = Agent(
    name="weather_assistant",
    model="gemini-2.5-flash-lite",  # Fast, cost-effective Gemini model
    description="A helpful weather assistant that provides weather information for cities.",
    instruction="""
    You are a friendly weather assistant. When users ask about the weather:

    1. Identify the city name from their question
    2. Use the get_weather tool to fetch current weather information
    3. Respond in a friendly, conversational tone
    4. If the city isn't available, suggest one of the available cities

    Be helpful and concise in your responses.
    """,
    tools=[get_weather]
)
'''

REQUIREMENTS_TXT = """google-adk
opentelemetry-instrumentation-google-genai"""

ENV_FILE = '''# https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#global-endpoint
GOOGLE_CLOUD_LOCATION="global"

# Set to 1 to use Vertex AI, or 0 to use Google AI Studio
GOOGLE_GENAI_USE_VERTEXAI=1'''

AGENT_ENGINE_CONFIG = '''{
    "min_instances": 0,
    "max_instances": 1,
    "resource_limits": {"cpu": "1", "memory": "1Gi"}
}'''

# ============================================================================
# Helper Functions
# ============================================================================


def create_agent_directory():
    """Create the agent directory structure"""
    agent_dir = "sample_agent"

    print(f"\n📁 Creating agent directory: {agent_dir}/")

    # Create directory
    os.makedirs(agent_dir, exist_ok=True)

    # Create agent.py
    with open(f"{agent_dir}/agent.py", "w") as f:
        f.write(AGENT_CODE_TEMPLATE)
    print(f"   ✅ Created {agent_dir}/agent.py")

    # Create requirements.txt
    with open(f"{agent_dir}/requirements.txt", "w") as f:
        f.write(REQUIREMENTS_TXT)
    print(f"   ✅ Created {agent_dir}/requirements.txt")

    # Create .env
    with open(f"{agent_dir}/.env", "w") as f:
        f.write(ENV_FILE)
    print(f"   ✅ Created {agent_dir}/.env")

    # Create .agent_engine_config.json
    with open(f"{agent_dir}/.agent_engine_config.json", "w") as f:
        f.write(AGENT_ENGINE_CONFIG)
    print(f"   ✅ Created {agent_dir}/.agent_engine_config.json")

    print(f"\n✅ Agent directory created successfully!")
    print(f"   Directory structure:")
    print(f"   {agent_dir}/")
    print(f"   ├── agent.py                  # The agent logic")
    print(f"   ├── requirements.txt          # The libraries")
    print(f"   ├── .env                      # The configuration")
    print(f"   └── .agent_engine_config.json # The hardware specs")

    return agent_dir


def explain_deployment_options():
    """Explain different deployment options"""
    print("\n" + "=" * 80)
    print("DEPLOYMENT OPTIONS")
    print("=" * 80)

    print("\n🔷 Vertex AI Agent Engine (This Tutorial)")
    print("   • Fully managed service for AI agents")
    print("   • Auto-scaling with built-in session management")
    print("   • Easy deployment using adk deploy command")
    print("   • Free tier: 10 agents per account")
    print("   📚 Guide: https://google.github.io/adk-docs/deploy/agent-engine/")

    print("\n🔷 Cloud Run")
    print("   • Serverless, easiest to start")
    print("   • Perfect for demos and small-to-medium workloads")
    print("   • Auto-scales to zero when not in use")
    print("   📚 Guide: https://google.github.io/adk-docs/deploy/cloud-run/")

    print("\n🔷 Google Kubernetes Engine (GKE)")
    print("   • Full control over containerized deployments")
    print("   • Best for complex multi-agent systems")
    print("   • Advanced orchestration capabilities")
    print("   📚 Guide: https://google.github.io/adk-docs/deploy/gke/")


def explain_deployment_steps():
    """Explain the deployment process"""
    print("\n" + "=" * 80)
    print("DEPLOYMENT PROCESS")
    print("=" * 80)

    print("\n📋 Prerequisites:")
    print("   1. Google Cloud Platform account")
    print("   2. Billing enabled (Free tier available)")
    print("   3. Enable required APIs:")
    print("      • Vertex AI API")
    print("      • Cloud Storage API")
    print("      • Cloud Logging API")
    print("      • Cloud Monitoring API")
    print("      • Cloud Trace API")
    print("      • Telemetry API")

    print("\n🚀 Deployment Steps:")
    print("\n   Step 1: Set your PROJECT_ID")
    print("   ```bash")
    print("   export GOOGLE_CLOUD_PROJECT='your-project-id'")
    print("   ```")

    print("\n   Step 2: Authenticate with Google Cloud")
    print("   ```bash")
    print("   gcloud auth login")
    print("   gcloud config set project your-project-id")
    print("   ```")

    print("\n   Step 3: Deploy the agent")
    print("   ```bash")
    print("   adk deploy agent_engine \\")
    print("     --project=$GOOGLE_CLOUD_PROJECT \\")
    print("     --region=us-east4 \\")
    print("     sample_agent \\")
    print("     --agent_engine_config_file=sample_agent/.agent_engine_config.json")
    print("   ```")

    print("\n   Step 4: Wait for deployment (2-5 minutes)")
    print("   You'll receive a resource name like:")
    print("   projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID")

    print("\n   Step 5: Test the deployed agent")
    print("   Use the Python SDK or REST API to send queries")


def explain_testing():
    """Explain how to test deployed agents"""
    print("\n" + "=" * 80)
    print("TESTING DEPLOYED AGENTS")
    print("=" * 80)

    print("\n📝 Python SDK Example:")
    print("""
import vertexai
from vertexai import agent_engines

# Initialize Vertex AI
vertexai.init(project='your-project-id', location='us-east4')

# Get the deployed agent
agents_list = list(agent_engines.list())
remote_agent = agents_list[0]  # Get most recent

# Test the agent
async for item in remote_agent.async_stream_query(
    message="What is the weather in Tokyo?",
    user_id="user_42",
):
    print(item)
""")

    print("\n🔍 What You'll See:")
    print("   1. Function call event - Agent calls get_weather tool")
    print("   2. Function response event - Weather data returned")
    print("   3. Final response event - Agent's natural language answer")


def explain_memory_bank():
    """Explain Vertex AI Memory Bank"""
    print("\n" + "=" * 80)
    print("VERTEX AI MEMORY BANK")
    print("=" * 80)

    print("\n🧠 What is Memory Bank?")
    print("   Memory Bank gives your agent long-term memory across sessions.")

    print("\n📊 Session Memory vs Memory Bank:")
    print("   ┌─────────────────┬────────────────────┐")
    print("   │ Session Memory  │ Memory Bank        │")
    print("   ├─────────────────┼────────────────────┤")
    print("   │ Single conv.    │ All conversations  │")
    print("   │ Forgets at end  │ Remembers forever  │")
    print("   │ 'What did I say'│ 'My favorite city' │")
    print("   └─────────────────┴────────────────────┘")

    print("\n💡 How It Works:")
    print("   1. During conversations: Agent uses memory tools to search past facts")
    print("   2. After conversations: System extracts key information")
    print("   3. Next session: Agent automatically recalls information")

    print("\n🔧 Enabling Memory Bank:")
    print("   1. Add memory tools to your agent (PreloadMemoryTool)")
    print("   2. Add callback to save conversations")
    print("   3. Redeploy your agent")

    print("\n📚 Learn More:")
    print("   • ADK Memory: https://google.github.io/adk-docs/sessions/memory/")
    print("   • Memory Tools: https://google.github.io/adk-docs/tools/built-in-tools/")


def explain_cleanup():
    """Explain cleanup process"""
    print("\n" + "=" * 80)
    print("CLEANUP & COST MANAGEMENT")
    print("=" * 80)

    print("\n⚠️  IMPORTANT: Always delete resources when done testing!")

    print("\n🧹 Delete Deployed Agent:")
    print("   ```python")
    print("   from vertexai import agent_engines")
    print("   ")
    print("   agent_engines.delete(")
    print("       resource_name=remote_agent.resource_name,")
    print("       force=True")
    print("   )")
    print("   ```")

    print("\n💰 Cost Management:")
    print("   • Free Tier: 10 agents per account")
    print("   • This Demo: Usually stays within free tier if cleaned up")
    print("   • If Left Running: Can incur costs")
    print("   • Best Practice: Delete immediately after testing")

    print("\n📊 Monitor Costs:")
    print("   • Google Cloud Console: https://console.cloud.google.com/billing")
    print("   • Set up billing alerts to avoid surprises")
    print("   • Check Agent Engine Console regularly")


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run the deployment guide"""

    print("\n" + "=" * 80)
    print("DAY 5B: DEPLOY ADK AGENT TO PRODUCTION")
    print("=" * 80)

    print("\n📚 What You'll Learn:")
    print("• Building production-ready ADK agents")
    print("• Understanding deployment options")
    print("• Deploying to Vertex AI Agent Engine")
    print("• Testing deployed agents")
    print("• Understanding Memory Bank")
    print("• Cost management and cleanup")

    # Section 1: Deployment Options
    explain_deployment_options()

    # Section 2: Create Agent Directory
    print("\n" + "=" * 80)
    print("SECTION 2: CREATE PRODUCTION AGENT")
    print("=" * 80)
    agent_dir = create_agent_directory()

    # Section 3: Deployment Process
    explain_deployment_steps()

    # Section 4: Testing
    explain_testing()

    # Section 5: Memory Bank
    explain_memory_bank()

    # Section 6: Cleanup
    explain_cleanup()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\n🎯 Key Takeaways:")
    print("✅ Agent Engine provides fully managed agent hosting")
    print("✅ Deploy with 'adk deploy agent_engine' command")
    print("✅ Test deployed agents with Python SDK or REST API")
    print("✅ Memory Bank enables long-term memory across sessions")
    print("✅ Always clean up resources to manage costs")

    print("\n📁 Files Created:")
    print(f"   • {agent_dir}/agent.py - Agent logic")
    print(f"   • {agent_dir}/requirements.txt - Dependencies")
    print(f"   • {agent_dir}/.env - Configuration")
    print(f"   • {agent_dir}/.agent_engine_config.json - Hardware specs")

    print("\n🚀 Next Steps:")
    print("   1. Get a Google Cloud account (free credits available)")
    print("   2. Enable required APIs in GCP Console")
    print("   3. Run 'adk deploy agent_engine' with your project ID")
    print("   4. Test your deployed agent")
    print("   5. Clean up resources when done")

    print("\n📚 Learn More:")
    print("   • ADK Deploy Guide: https://google.github.io/adk-docs/deploy/")
    print("   • Agent Engine Docs: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview")
    print("   • Cloud Run Deploy: https://google.github.io/adk-docs/deploy/cloud-run/")
    print("   • GKE Deploy: https://google.github.io/adk-docs/deploy/gke/")

    print("\n🎓 Course Complete!")
    print("   Congratulations on completing the 5-Day AI Agents course!")
    print("   You now have the skills to build, test, and deploy production agents.")

    print("\n⭐ Share Your Projects:")
    print("   • Kaggle Discord: https://discord.com/invite/kaggle")
    print("   • ADK Documentation: https://google.github.io/adk-docs/")


if __name__ == "__main__":
    main()
