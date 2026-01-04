✅ Imports completed successfully
✅ Environment variables loaded from .env file

================================================================================
DAY 5B: DEPLOY ADK AGENT TO PRODUCTION
================================================================================

📚 What You'll Learn:
• Building production-ready ADK agents
• Understanding deployment options
• Deploying to Vertex AI Agent Engine
• Testing deployed agents
• Understanding Memory Bank
• Cost management and cleanup

================================================================================
DEPLOYMENT OPTIONS
================================================================================

🔷 Vertex AI Agent Engine (This Tutorial)
   • Fully managed service for AI agents
   • Auto-scaling with built-in session management
   • Easy deployment using adk deploy command
   • Free tier: 10 agents per account
   📚 Guide: https://google.github.io/adk-docs/deploy/agent-engine/

🔷 Cloud Run
   • Serverless, easiest to start
   • Perfect for demos and small-to-medium workloads
   • Auto-scales to zero when not in use
   📚 Guide: https://google.github.io/adk-docs/deploy/cloud-run/

🔷 Google Kubernetes Engine (GKE)
   • Full control over containerized deployments
   • Best for complex multi-agent systems
   • Advanced orchestration capabilities
   📚 Guide: https://google.github.io/adk-docs/deploy/gke/

================================================================================
SECTION 2: CREATE PRODUCTION AGENT
================================================================================

📁 Creating agent directory: sample_agent/
   ✅ Created sample_agent/agent.py
   ✅ Created sample_agent/requirements.txt
   ✅ Created sample_agent/.env
   ✅ Created sample_agent/.agent_engine_config.json

✅ Agent directory created successfully!
   Directory structure:
   sample_agent/
   ├── agent.py                  # The agent logic
   ├── requirements.txt          # The libraries
   ├── .env                      # The configuration
   └── .agent_engine_config.json # The hardware specs

================================================================================
DEPLOYMENT PROCESS
================================================================================

📋 Prerequisites:
   1. Google Cloud Platform account
   2. Billing enabled (Free tier available)
   3. Enable required APIs:
      • Vertex AI API
      • Cloud Storage API
      • Cloud Logging API
      • Cloud Monitoring API
      • Cloud Trace API
      • Telemetry API

🚀 Deployment Steps:

   Step 1: Set your PROJECT_ID
   ```bash
   export GOOGLE_CLOUD_PROJECT='your-project-id'
   ```

   Step 2: Authenticate with Google Cloud
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

   Step 3: Deploy the agent
   ```bash
   adk deploy agent_engine \
     --project=$GOOGLE_CLOUD_PROJECT \
     --region=us-east4 \
     sample_agent \
     --agent_engine_config_file=sample_agent/.agent_engine_config.json
   ```

   Step 4: Wait for deployment (2-5 minutes)
   You'll receive a resource name like:
   projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID

   Step 5: Test the deployed agent
   Use the Python SDK or REST API to send queries

================================================================================
TESTING DEPLOYED AGENTS
================================================================================

📝 Python SDK Example:

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


🔍 What You'll See:
   1. Function call event - Agent calls get_weather tool
   2. Function response event - Weather data returned
   3. Final response event - Agent's natural language answer

================================================================================
VERTEX AI MEMORY BANK
================================================================================

🧠 What is Memory Bank?
   Memory Bank gives your agent long-term memory across sessions.

📊 Session Memory vs Memory Bank:
   ┌─────────────────┬────────────────────┐
   │ Session Memory  │ Memory Bank        │
   ├─────────────────┼────────────────────┤
   │ Single conv.    │ All conversations  │
   │ Forgets at end  │ Remembers forever  │
   │ 'What did I say'│ 'My favorite city' │
   └─────────────────┴────────────────────┘

💡 How It Works:
   1. During conversations: Agent uses memory tools to search past facts
   2. After conversations: System extracts key information
   3. Next session: Agent automatically recalls information

🔧 Enabling Memory Bank:
   1. Add memory tools to your agent (PreloadMemoryTool)
   2. Add callback to save conversations
   3. Redeploy your agent

📚 Learn More:
   • ADK Memory: https://google.github.io/adk-docs/sessions/memory/
   • Memory Tools: https://google.github.io/adk-docs/tools/built-in-tools/

================================================================================
CLEANUP & COST MANAGEMENT
================================================================================

⚠️  IMPORTANT: Always delete resources when done testing!

🧹 Delete Deployed Agent:
   ```python
   from vertexai import agent_engines
   
   agent_engines.delete(
       resource_name=remote_agent.resource_name,
       force=True
   )
   ```

💰 Cost Management:
   • Free Tier: 10 agents per account
   • This Demo: Usually stays within free tier if cleaned up
   • If Left Running: Can incur costs
   • Best Practice: Delete immediately after testing

📊 Monitor Costs:
   • Google Cloud Console: https://console.cloud.google.com/billing
   • Set up billing alerts to avoid surprises
   • Check Agent Engine Console regularly

================================================================================
SUMMARY
================================================================================

🎯 Key Takeaways:
✅ Agent Engine provides fully managed agent hosting
✅ Deploy with 'adk deploy agent_engine' command
✅ Test deployed agents with Python SDK or REST API
✅ Memory Bank enables long-term memory across sessions
✅ Always clean up resources to manage costs

📁 Files Created:
   • sample_agent/agent.py - Agent logic
   • sample_agent/requirements.txt - Dependencies
   • sample_agent/.env - Configuration
   • sample_agent/.agent_engine_config.json - Hardware specs

🚀 Next Steps:
   1. Get a Google Cloud account (free credits available)
   2. Enable required APIs in GCP Console
   3. Run 'adk deploy agent_engine' with your project ID
   4. Test your deployed agent
   5. Clean up resources when done

📚 Learn More:
   • ADK Deploy Guide: https://google.github.io/adk-docs/deploy/
   • Agent Engine Docs: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview
   • Cloud Run Deploy: https://google.github.io/adk-docs/deploy/cloud-run/
   • GKE Deploy: https://google.github.io/adk-docs/deploy/gke/

🎓 Course Complete!
   Congratulations on completing the 5-Day AI Agents course!
   You now have the skills to build, test, and deploy production agents.

⭐ Share Your Projects:
   • Kaggle Discord: https://discord.com/invite/kaggle
   • ADK Documentation: https://google.github.io/adk-docs/