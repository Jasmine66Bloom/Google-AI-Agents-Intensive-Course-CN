# Day 1 - AI Agents Python Scripts

This folder contains Python scripts based on the Day 1 Jupyter notebooks from the Kaggle 5-day Agents course.

## Scripts Overview

### 1. `day_1a_prompt_to_action.py`
**From Prompt to Action - Your First AI Agent**

This script demonstrates:
- Setting up a basic AI agent with Google ADK
- Using the Google Search tool
- Running queries that require current information
- Understanding how agents reason and take action

**Key Concepts:**
- Agents don't just respond—they REASON and ACT
- Tools extend agent capabilities
- Agents can decide when to use tools

### 2. `day_1b_agent_architectures.py`
**Multi-Agent Systems & Workflow Patterns**

This script demonstrates four powerful workflow patterns:

1. **LLM-Based Orchestration**: Dynamic workflow where an LLM decides which agents to call
   - Example: Research agent + Summarizer agent

2. **Sequential Workflow**: Fixed pipeline where agents run in order
   - Example: Outline agent → Writer agent → Editor agent

3. **Parallel Workflow**: Concurrent execution of independent tasks
   - Example: Multiple research agents working simultaneously

4. **Loop Workflow**: Iterative refinement with feedback
   - Example: Writer → Critic → Refiner (loops until approved)

## Setup Instructions

### Quick Setup (macOS/Linux)

The easiest way to get started is using the automated setup script:

```bash
# From the project root directory
./setup.sh
```

This script will:
- Create a Python virtual environment
- Install all required packages
- Create a .env file template for your API key

### Manual Setup

If you prefer to set up manually or are on Windows:

1. **Create a Virtual Environment** (Python 3.14+ on macOS requires this)

   ```bash
   # From the project root directory
   python3 -m venv venv

   # Activate the virtual environment
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```

2. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   **Note for macOS users:** Use `pip` (not `pip3`) once your virtual environment is activated.

3. **Get a Gemini API Key**
   - Visit: https://aistudio.google.com/app/api-keys
   - Create a new API key

4. **Configure Your API Key**
   ```bash
   # From the project root directory
   cp .env.example .env
   ```

   Then edit the `.env` file and replace `your-api-key-here` with your actual API key:
   ```
   GOOGLE_API_KEY=your-actual-api-key-here
   ```

   **Important:** The `.env` file is already in `.gitignore`, so your API key will NOT be committed to git.

## Running the Scripts

**Important:** Make sure your virtual environment is activated before running the scripts!

```bash
# Activate the virtual environment (if not already activated)
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### Run Script 1a (Basic Agent)
```bash
cd Day-1
python day_1a_prompt_to_action.py
```

This will:
- Create a basic agent with Google Search
- Run example queries
- Let you try your own custom query

### Run Script 1b (Multi-Agent Architectures)
```bash
cd Day-1
python day_1b_agent_architectures.py
```

When you run this script, you'll be prompted to choose which pattern to run:
- Option 1: LLM-Based Orchestration
- Option 2: Sequential Pipeline
- Option 3: Parallel Execution
- Option 4: Loop Refinement
- Option 5: Run all examples

**Note:** Running all examples may take several minutes and use multiple API calls.

## Understanding the Output

Both scripts will show:
- The agent's thinking process
- Which tools are being called
- The final responses
- Session management (debug_session_id)

You may see warnings like:
```
WARNING:google_genai.types:Warning: there are non-text parts in the response...
```
These are normal and indicate the agent is using function calls (tools).

## Workflow Pattern Decision Guide

**Use Sequential when:**
- Order matters (each step builds on the previous)
- You need a linear pipeline
- Predictable execution is important

**Use Parallel when:**
- Tasks are independent
- Speed matters
- You can execute concurrently

**Use Loop when:**
- Iterative improvement is needed
- Quality refinement matters
- You need repeated cycles until a condition is met

**Use LLM Orchestration when:**
- Dynamic decisions are needed
- The workflow should adapt to the query
- Flexibility is more important than predictability

## Troubleshooting

### Error: "command not found: pip" or "No module named..."
Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On macOS/Linux
# You should see (venv) in your terminal prompt
```

If you don't have a virtual environment set up yet, run the setup script:
```bash
./setup.sh
```

### Error: "GOOGLE_API_KEY not found"
Make sure you've created a `.env` file in the project root:
```bash
# From the project root directory
cp .env.example .env
# Then edit .env and add your API key
```

### Error: 429 (Rate Limit)
The scripts include retry logic, but if you hit rate limits:
- Wait a few minutes before retrying
- Consider running examples individually instead of all at once

### Error: "No module named 'google.adk'" or "No module named 'dotenv'"
Install the required libraries:
```bash
# From the project root directory
pip install -r requirements.txt
```

## Learning Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Quickstart for Python](https://google.github.io/adk-docs/get-started/python/)
- [ADK Agents Overview](https://google.github.io/adk-docs/agents/)
- [Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [Parallel Agents](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)

## Next Steps

After completing Day 1, move on to Day 2 notebooks to learn about:
- Custom Functions
- MCP Tools
- Long-Running Operations

Happy learning!
