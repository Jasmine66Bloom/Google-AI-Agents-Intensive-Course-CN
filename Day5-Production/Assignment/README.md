# Day 5 - Agent2Agent Communication & Production Deployment

This folder contains Python scripts based on the Day 5 Jupyter notebooks from the Kaggle 5-day Agents course - the final day!

## Scripts Overview

### 1. `day_5a_agent2agent_communication.py`
**Agent2Agent (A2A) Communication**

This script demonstrates:
- Understanding the A2A protocol and when to use it vs local sub-agents
- Common A2A architecture patterns (cross-framework, cross-language, cross-organization)
- Exposing an ADK agent via A2A using `to_a2a()`
- Consuming remote agents using `RemoteA2aAgent`
- Building a product catalog integration system

**Key Concepts:**
- **A2A Protocol**: Standard for agent-to-agent communication across networks
- **Agent Cards**: JSON documents describing agent capabilities
- **to_a2a()**: Exposes agents with auto-generated agent cards
- **RemoteA2aAgent**: Client-side proxy for consuming remote agents
- **Cross-Organization Integration**: Agents from different teams/companies

**Example Use Cases:**
- Integrating with external vendor services
- Microservices architectures with agent specialization
- Cross-language agent communication (Python ↔ Java)
- Third-party agent marketplace integration

### 2. `day_5b_agent_deployment.py`
**Deploy ADK Agents to Production**

This script demonstrates:
- Building production-ready ADK agents
- Understanding deployment options (Agent Engine, Cloud Run, GKE)
- Creating deployment configuration files
- Deploying to Vertex AI Agent Engine using ADK CLI
- Testing deployed agents with Python SDK
- Understanding Vertex AI Memory Bank for long-term memory
- Cost management and cleanup best practices

**Key Concepts:**
- **Vertex AI Agent Engine**: Fully managed service for hosting agents
- **Deployment Configuration**: Hardware specs and scaling settings
- **Production Architecture**: Separating code, config, and secrets
- **Memory Bank**: Long-term memory across sessions
- **Cost Management**: Free tier, scaling, and cleanup

**Example Use Cases:**
- Deploying customer support agents to production
- Scaling agents with auto-scaling infrastructure
- Building multi-session agents with persistent memory
- Managing agent fleets in enterprise environments

## Prerequisites

Make sure you've completed the setup from the project root:

```bash
# From the project root directory
source venv/bin/activate  # Activate virtual environment
```

If you haven't set up the project yet, run:

```bash
cd ..  # Go to project root
./setup.sh
source venv/bin/activate
```

### Additional Prerequisites for Day 5b (Deployment)

**For production deployment, you'll need:**
- Google Cloud Platform account ([Sign up here](https://cloud.google.com/free))
- Billing enabled (Free tier includes $300 credits for 90 days)
- Required APIs enabled (Vertex AI, Cloud Storage, Logging, etc.)

**Note:** The deployment script provides guidance but doesn't perform actual deployment. To deploy, follow the instructions in the script output.

## Running the Scripts

### Run Script 5a (A2A Communication)

```bash
# Make sure you're in the Day-5 directory and venv is activated
python day_5a_agent2agent_communication.py
```

**What it does:**
1. **Section 1**: Creates a Product Catalog Agent with product lookup tool
2. **Section 2 & 3**: Exposes the agent via A2A and starts server on localhost:8001
3. **Views Agent Card**: Fetches and displays the auto-generated agent card
4. **Section 4**: Creates Customer Support Agent that consumes the Product Catalog Agent
5. **Section 5**: Tests A2A communication with multiple queries
6. **Cleanup**: Stops the server

**Note:** This script starts a background server. The script handles cleanup automatically, but you can manually stop it with Ctrl+C if needed.

### Run Script 5b (Deployment Guide)

```bash
python day_5b_agent_deployment.py
```

**What it does:**
1. **Explains Deployment Options**: Agent Engine, Cloud Run, GKE
2. **Creates Agent Directory**: Generates production-ready agent files
3. **Explains Deployment Process**: Step-by-step deployment instructions
4. **Explains Testing**: How to test deployed agents
5. **Explains Memory Bank**: Long-term memory concepts
6. **Explains Cleanup**: Cost management and resource deletion

**Note:** This script is educational and creates template files. Actual deployment requires Google Cloud credentials and the `adk deploy` command.

## Understanding the Output

### Day 5a Output (A2A Communication)

**Agent Creation:**
```
✅ Product Catalog Agent created successfully!
   Model: gemini-2.5-flash-lite
   Tool: get_product_info()
   Ready to be exposed via A2A...
```

**Server Startup:**
```
🚀 Starting Product Catalog Agent server...
   Waiting for server to be ready...
.....
✅ Product Catalog Agent server is running!
   Server URL: http://localhost:8001
   Agent card: http://localhost:8001/.well-known/agent-card.json
```

**Agent Card:**
```json
{
  "name": "product_catalog_agent",
  "description": "External vendor's product catalog agent...",
  "url": "http://localhost:8001",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "id": "product_catalog_agent-get_product_info",
      "name": "get_product_info",
      "description": "Get product information for a given product."
    }
  ]
}
```

**A2A Communication Test:**
```
👤 Customer: Can you tell me about the iPhone 15 Pro? Is it in stock?

🎧 Support Agent response:
------------------------------------------------------------
The iPhone 15 Pro is available for $999. We currently have low stock,
with only 8 units remaining. It features a 128GB storage capacity and
a titanium finish.
------------------------------------------------------------
```

### Day 5b Output (Deployment Guide)

**Directory Creation:**
```
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
```

**Deployment Instructions:**
```
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
```

## Agent2Agent (A2A) Protocol Deep Dive

### What is A2A?

The [Agent2Agent Protocol](https://a2a-protocol.org/) is an open standard that enables agents to communicate across:
- **Different frameworks** (ADK, LangChain, CrewAI, etc.)
- **Different languages** (Python, JavaScript, Java, etc.)
- **Different organizations** (Your company ↔ Vendor services)

### A2A Architecture Patterns

**Pattern 1: Cross-Framework Integration**
```
┌──────────────────┐           ┌──────────────────┐
│ ADK Agent        │  ─A2A──▶  │ LangChain Agent  │
│ (Python)         │           │ (Python)         │
└──────────────────┘           └──────────────────┘
```

**Pattern 2: Cross-Language Communication**
```
┌──────────────────┐           ┌──────────────────┐
│ Python Agent     │  ─A2A──▶  │ Java Agent       │
│ (ADK)            │           │ (Custom)         │
└──────────────────┘           └──────────────────┘
```

**Pattern 3: Cross-Organization Boundaries**
```
┌──────────────────┐           ┌──────────────────┐
│ Your Internal    │  ─A2A──▶  │ External Vendor  │
│ Support Agent    │           │ Product Catalog  │
│ (your-domain)    │           │ (vendor.com)     │
└──────────────────┘           └──────────────────┘
```

### A2A vs Local Sub-Agents Decision Table

| Factor | Use A2A | Use Local Sub-Agents |
|--------|---------|---------------------|
| **Location** | Different machines/services | Same process |
| **Ownership** | Different teams/orgs | Your team |
| **Language** | Cross-language needed | Same language |
| **Framework** | Different frameworks | Same framework |
| **Performance** | Network latency OK | Need low latency |
| **Contract** | Formal API contract | Internal interface |
| **Example** | Vendor product catalog | Internal workflow steps |

### Agent Cards Explained

An **agent card** is a JSON document published at `/.well-known/agent-card.json` that describes:

```json
{
  "name": "agent_name",
  "description": "What the agent does",
  "url": "http://agent-host:port",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "id": "skill_id",
      "name": "skill_name",
      "description": "What this skill does"
    }
  ],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"]
}
```

**Think of it as:** The "business card" that tells other agents how to work with this agent.

### Exposing Agents with to_a2a()

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Convert agent to A2A-compatible app
a2a_app = to_a2a(my_agent, port=8001)

# Start the server
# uvicorn will serve the agent at http://localhost:8001
```

**What to_a2a() does:**
1. Wraps agent in FastAPI/Starlette server
2. Auto-generates agent card from agent definition
3. Serves agent card at `/.well-known/agent-card.json`
4. Handles A2A protocol endpoints (`/tasks`)
5. Manages request/response formatting

### Consuming Agents with RemoteA2aAgent

```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Create client-side proxy
remote_agent = RemoteA2aAgent(
    name="remote_service",
    description="Remote agent description",
    agent_card="http://vendor.com/.well-known/agent-card.json"
)

# Use it like a local sub-agent!
my_agent = LlmAgent(
    name="my_agent",
    sub_agents=[remote_agent]  # That's it!
)
```

**What RemoteA2aAgent does:**
1. Fetches and reads the remote agent card
2. Creates a local proxy for the remote agent
3. Translates sub-agent calls into A2A HTTP requests
4. Handles all protocol communication transparently

## Production Deployment Deep Dive

### Deployment Options Comparison

| Feature | Agent Engine | Cloud Run | GKE |
|---------|-------------|-----------|-----|
| **Management** | Fully managed | Serverless | Self-managed |
| **Scaling** | Auto (built-in) | Auto (serverless) | Manual/Auto |
| **Setup** | Easiest | Easy | Complex |
| **Session Management** | Built-in | Manual | Manual |
| **Best For** | AI agents | General apps | Complex systems |
| **Free Tier** | 10 agents | Generous | Compute hours |

### Agent Engine Architecture

```
┌─────────────┐
│  Your Code  │  ← agent.py, tools, instructions
└──────┬──────┘
       │ adk deploy agent_engine
       ↓
┌─────────────┐
│Agent Engine │
│             │
│ • Auto-scale│  ← 0-N instances based on load
│ • Sessions  │  ← Built-in session management
│ • Logging   │  ← Automatic Cloud Logging
│ • Monitoring│  ← Cloud Monitoring integration
│ • Memory    │  ← Memory Bank support
└──────┬──────┘
       │ HTTPS/REST API
       ↓
┌─────────────┐
│   Clients   │  ← Your apps, web UI, mobile
└─────────────┘
```

### Production Agent Structure

```
my_agent/
├── agent.py                      # Agent definition
├── requirements.txt              # Python dependencies
├── .env                          # Environment config
└── .agent_engine_config.json     # Deployment config
```

**agent.py:**
```python
from google.adk.agents import Agent
import vertexai
import os

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

def my_tool(param: str) -> dict:
    # Tool implementation
    pass

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash-lite",
    description="Agent description",
    instruction="Agent instructions",
    tools=[my_tool]
)
```

**requirements.txt:**
```
google-adk
opentelemetry-instrumentation-google-genai
# Add other dependencies
```

**.env:**
```
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI=1
```

**.agent_engine_config.json:**
```json
{
    "min_instances": 0,
    "max_instances": 1,
    "resource_limits": {
        "cpu": "1",
        "memory": "1Gi"
    }
}
```

### Deployment Process

**1. Enable Required APIs:**
```bash
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudtrace.googleapis.com \
  telemetry.googleapis.com
```

**2. Deploy:**
```bash
adk deploy agent_engine \
  --project=YOUR_PROJECT_ID \
  --region=us-east4 \
  my_agent \
  --agent_engine_config_file=my_agent/.agent_engine_config.json
```

**3. Get Resource Name:**
```
projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID
```

**4. Test:**
```python
import vertexai
from vertexai import agent_engines

vertexai.init(project='your-project', location='us-east4')

# Get deployed agent
agents = list(agent_engines.list())
agent = agents[0]

# Test
async for event in agent.async_stream_query(
    message="Test query",
    user_id="user123"
):
    print(event)
```

**5. Cleanup:**
```python
agent_engines.delete(
    resource_name=agent.resource_name,
    force=True
)
```

### Vertex AI Memory Bank

**Problem:**
- Session memory forgets everything when session ends
- Users have to repeat preferences every conversation
- No learning from past interactions

**Solution - Memory Bank:**

```
Session 1:
User: "I prefer Celsius"
Agent: "Noted!"
→ Memory Bank stores: "User prefers Celsius"

Session 2 (days later):
User: "Weather in Tokyo?"
Agent: "Tokyo is 21°C" ← Automatically uses Celsius!
```

**How to Enable:**

1. **Add Memory Tools:**
```python
from google.adk.tools import preload_memory

agent = LlmAgent(
    name="my_agent",
    tools=[preload_memory],  # Loads relevant memories
    ...
)
```

2. **Add Callback:**
```python
async def save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    after_agent_callback=save_to_memory,
    ...
)
```

3. **Redeploy**

**Memory Bank vs Session Memory:**

| Feature | Session Memory | Memory Bank |
|---------|---------------|-------------|
| **Scope** | Single conversation | All conversations |
| **Duration** | Until session ends | Permanent |
| **Use Case** | "What did I just say?" | "What's my favorite city?" |
| **Storage** | In-memory/session | Vertex AI service |
| **Retrieval** | Automatic (context) | Tool-based search |

## Common Issues and Solutions

### A2A Communication Issues

#### Issue: "Connection refused" when testing A2A
**Solution:**
- Check if server is running: `curl http://localhost:8001/.well-known/agent-card.json`
- Wait for server startup (can take 5-10 seconds)
- Check port conflicts: `lsof -i :8001`

#### Issue: Agent card not found (404)
**Solution:**
- Verify server started successfully
- Check URL includes `/.well-known/agent-card.json`
- Ensure `to_a2a()` was called correctly

#### Issue: Remote agent not responding
**Solution:**
- Check server logs for errors
- Verify API key is set in server environment
- Test server directly: `curl http://localhost:8001/.well-known/agent-card.json`

### Deployment Issues

#### Issue: "Project ID not set" error
**Solution:**
```bash
export GOOGLE_CLOUD_PROJECT='your-project-id'
# Or set in .env file
```

#### Issue: API not enabled errors
**Solution:**
- Visit https://console.cloud.google.com/flows/enableapi
- Enable all required APIs listed in deployment guide
- Wait a few minutes for API enablement to propagate

#### Issue: Deployment fails with permissions error
**Solution:**
```bash
# Ensure you're authenticated
gcloud auth login

# Set project
gcloud config set project your-project-id

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/aiplatform.user"
```

#### Issue: Deployment hangs or times out
**Solution:**
- Check internet connection
- Verify region is correct (use: us-east4, europe-west1, etc.)
- Try a different region if one is experiencing issues
- Check GCP status page for outages

## Best Practices

### A2A Communication Best Practices

1. **Always Publish Agent Cards**
   - Serve at `/.well-known/agent-card.json` (standard path)
   - Keep descriptions clear and accurate
   - Version your agent cards

2. **Handle Network Failures Gracefully**
   ```python
   try:
       response = await remote_agent.call(...)
   except Exception as e:
       # Fallback behavior
       return default_response
   ```

3. **Secure A2A Endpoints**
   - Use HTTPS in production
   - Implement API key authentication
   - Rate limit requests

4. **Monitor A2A Traffic**
   - Log all cross-agent calls
   - Track response times
   - Set up alerts for failures

### Production Deployment Best Practices

1. **Start Small**
   ```json
   {
       "min_instances": 0,  // Scale to zero when idle
       "max_instances": 1   // Limit for testing
   }
   ```

2. **Enable Logging**
   - Use Cloud Logging for debugging
   - Enable tracing for performance analysis
   - Set up error monitoring

3. **Test Before Production**
   - Deploy to dev/staging environment first
   - Run load tests
   - Verify all tools work correctly

4. **Cost Management**
   - Start with min_instances=0 to save costs
   - Monitor usage in Cloud Console
   - Set up billing alerts
   - Delete test deployments promptly

5. **Version Control**
   - Tag deployments with version numbers
   - Keep deployment configs in git
   - Document changes between versions

## Learning Resources

### A2A Protocol
- [Official A2A Protocol Website](https://a2a-protocol.org/)
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A Tutorials](https://a2a-protocol.org/latest/tutorials/)

### ADK A2A Documentation
- [Introduction to A2A in ADK](https://google.github.io/adk-docs/a2a/intro/)
- [Exposing Agents Quickstart](https://google.github.io/adk-docs/a2a/quickstart-exposing/)
- [Consuming Agents Quickstart](https://google.github.io/adk-docs/a2a/quickstart-consuming/)

### Deployment Documentation
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/)
- [Deploy to Agent Engine](https://google.github.io/adk-docs/deploy/agent-engine/)
- [Deploy to Cloud Run](https://google.github.io/adk-docs/deploy/cloud-run/)
- [Deploy to GKE](https://google.github.io/adk-docs/deploy/gke/)

### Vertex AI Agent Engine
- [Agent Engine Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [Agent Engine Locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)
- [Memory Bank Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview)

### Video Tutorials
- [Google Cloud Free Trial Setup (3 min)](https://youtu.be/-nUAQq_evxc)
- [ADK Deployment Walkthrough](https://www.youtube.com/watch?v=YOUR_VIDEO)

## Next Steps

After completing Day 5, you've learned:
- ✅ Building multi-agent systems with A2A protocol
- ✅ Exposing agents as services for cross-organization use
- ✅ Consuming remote agents transparently
- ✅ Deploying agents to production with Agent Engine
- ✅ Managing costs and cleaning up resources
- ✅ Adding long-term memory with Memory Bank

**🎓 Course Complete!**

You've finished the entire 5-Day AI Agents Intensive Course! You now have the complete skillset to:
- Build intelligent agents from scratch
- Add tools and capabilities
- Manage sessions and memory
- Debug and evaluate agent performance
- Deploy to production infrastructure

**What's Next:**
1. Build your own AI agent project
2. Deploy it to production
3. Share your work on Kaggle Discord
4. Explore advanced ADK features
5. Contribute to the open-source community!

**Practice Projects:**
1. Build a customer support agent with product catalog integration
2. Create a multi-agent research system with specialized agents
3. Deploy a personal assistant with Memory Bank
4. Build an A2A agent marketplace

Happy building! 🚀🎉

