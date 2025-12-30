# Day 4 - Agent Observability & Evaluation

This folder contains Python scripts based on the Day 4 Jupyter notebooks from the Kaggle 5-day Agents course.

## Scripts Overview

### 1. `day_4a_agent_observability.py`
**Agent Observability - Logs, Traces & Metrics**

This script demonstrates:
- Understanding agent observability pillars (logs, traces, metrics)
- Debugging agents using ADK web UI with DEBUG logging
- Identifying and fixing bugs through log analysis
- Implementing LoggingPlugin for production observability
- Creating custom plugins and callbacks for specialized monitoring

**Key Concepts:**
- **Logs**: Records of individual events showing what happened
- **Traces**: Connected logs showing the entire decision sequence
- **Metrics**: Summary statistics showing overall performance
- **DEBUG Logging**: Detailed inspection of LLM requests/responses
- **Plugins**: Custom code modules that hook into agent lifecycle
- **Callbacks**: Functions that run at specific agent execution points

**Example Use Cases:**
- Debugging mysterious agent failures in development
- Production monitoring with automatic log capture
- Performance tracking with custom metrics
- Compliance and audit trail generation

### 2. `day_4b_agent_evaluation.py`
**Agent Evaluation - Testing & Regression Detection**

This script demonstrates:
- Creating test cases interactively in ADK web UI
- Running systematic evaluations with `adk eval` CLI
- Understanding evaluation metrics (response_match and tool_trajectory)
- Creating evaluation configuration files
- Analyzing evaluation results and fixing issues
- Advanced user simulation concepts

**Key Concepts:**
- **Evaluation**: Systematic testing of agent performance across scenarios
- **Test Cases**: Expected inputs, outputs, and tool usage patterns
- **response_match_score**: Text similarity between actual and expected responses
- **tool_trajectory_avg_score**: Correctness of tool calls and parameters
- **Regression Testing**: Ensuring new changes don't break existing functionality
- **User Simulation**: Dynamic test generation with LLM-powered user behavior

**Example Use Cases:**
- Proactive quality assurance before deployment
- Automated regression testing in CI/CD pipelines
- Measuring agent performance improvements over time
- Discovering edge cases with user simulation

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

## Running the Scripts

### Run Script 4a (Observability)

```bash
# Make sure you're in the Day-4 directory and venv is activated
python day_4a_agent_observability.py
```

**What it does:**
1. **Demo 1 - Broken Agent**: Shows how to identify bugs through debugging
   - Creates an agent with an intentional type error
   - Explains how to use ADK web UI for interactive debugging
   - Demonstrates finding bugs through trace analysis

2. **Demo 2 - LoggingPlugin**: Implements production observability
   - Runs a research paper finder agent
   - Automatically captures all agent activity
   - Demonstrates comprehensive logging output

3. **Demo 3 - Custom Plugin**: Creates specialized monitoring
   - Implements CountInvocationPlugin
   - Tracks agent invocations and LLM requests
   - Shows how to build custom observability

### Run Script 4b (Evaluation)

```bash
python day_4b_agent_evaluation.py
```

**What it does:**
1. **Demo 1 - Interactive Evaluation**: Explains ADK web UI workflow
   - How to create test cases from conversations
   - Running evaluations and viewing results
   - Understanding pass/fail criteria

2. **Demo 2 - Systematic Evaluation**: Sets up CLI evaluation
   - Creates evaluation configuration file
   - Generates test case files
   - Explains `adk eval` command usage

3. **Demo 3 - User Simulation**: Covers advanced testing
   - Dynamic test generation concepts
   - ConversationScenario patterns
   - Benefits over static test cases

4. **Demo 4 - Best Practices**: Shares evaluation strategies
   - Building comprehensive test suites
   - Setting appropriate thresholds
   - Production evaluation workflows

## Understanding the Output

### Day 4a Output (Observability)

**Broken Agent Demo:**
```
🐛 This agent has an intentional bug in the count_papers tool
The tool expects a 'str' but should accept 'List[str]'

👉 In a real scenario, you would:
   1. Run 'adk web --log_level DEBUG' to start the web UI
   2. Test the agent with: 'Find latest quantum computing papers'
   3. Use the Events tab and Traces to find the bug
   4. Look at the function_call to see incorrect parameter types
```

**LoggingPlugin Demo:**
```
🚀 Running agent with LoggingPlugin...
📊 Watch the comprehensive logging output:

INFO: Sending out request, model: gemini-2.5-flash-lite
INFO: Response received from the model
INFO: Tool called: google_search
INFO: Response: [agent response]

✅ Agent execution complete!
• LoggingPlugin automatically captured all agent activity
• Check logger.log file for detailed DEBUG logs
```

**Custom Plugin Demo:**
```
[CountPlugin] Agent invocation #1
[CountPlugin] LLM request #1
[CountPlugin] LLM request #2

📊 Custom Plugin Statistics:
   • Agent invocations: 1
   • LLM requests: 2
💡 Custom plugins allow you to add any observability logic you need!
```

### Day 4b Output (Evaluation)

**Interactive Evaluation:**
```
📝 Interactive Evaluation Workflow:
1️⃣  CREATE TEST CASES:
   • Start ADK web UI: adk web
   • Have a conversation with your agent
   • Navigate to 'Eval' tab
   • Create evaluation set and add current session

2️⃣  RUN EVALUATION:
   • Check your test case
   • Click 'Run Evaluation' button
   • Review metrics and start evaluation

3️⃣  ANALYZE RESULTS:
   • Green 'Pass': Agent behaved as expected
   • Red 'Fail': Agent deviated from expected behavior
```

**CLI Evaluation:**
```
✅ Evaluation configuration created!
📊 Evaluation Criteria:
• tool_trajectory_avg_score: 1.0 - Requires exact tool usage match
• response_match_score: 0.8 - Requires 80% text similarity

✅ Evaluation test cases created
🧪 Test scenarios:
• living_room_light_on: Please turn on the floor lamp...
• kitchen_on_off_sequence: Switch on the main light...

🚀 Run this command to execute evaluation:
   adk eval home_automation_agent integration.evalset.json \
     --config_file_path=test_config.json \
     --print_detailed_results
```

## Key Patterns and When to Use Them

### Observability Approaches

| Approach | When to Use | Best For |
|----------|-------------|----------|
| **adk web --log_level DEBUG** | Development debugging | Interactive problem-solving |
| **LoggingPlugin()** | Production monitoring | Standard observability needs |
| **Custom Plugins** | Specialized requirements | Domain-specific metrics, compliance |

### Evaluation Strategies

| Strategy | When to Use | Best For |
|----------|-------------|----------|
| **Interactive (Web UI)** | Development iteration | Quick feedback, test creation |
| **CLI (adk eval)** | Systematic testing | Regression testing, CI/CD |
| **User Simulation** | Comprehensive coverage | Edge case discovery |

## Observability Deep Dive

### Log Levels

```python
--log_level DEBUG  # Full LLM prompts, responses, internal state
--log_level INFO   # Agent actions, tool calls (default)
--log_level WARNING  # Potential issues
--log_level ERROR  # Failures and exceptions
```

**When to use each:**
- **DEBUG**: Development, debugging mysterious failures
- **INFO**: Production monitoring, general operation tracking
- **WARNING**: Alerting on anomalies
- **ERROR**: Critical failure tracking

### Understanding Traces

Traces show the complete execution flow:

```
User Query
  ↓
Call root_agent
  ↓
  Call google_search_agent
    ↓
    execute_tool: google_search
    ↓
    LLM processes results
  ↓
  Call count_papers tool
  ↓
  LLM generates final response
↓
Return to user
```

**Benefits:**
- Identify bottlenecks (which step takes longest?)
- Understand decision flow (why did agent choose this path?)
- Debug tool usage (which tools were called and when?)

### Custom Plugin Template

```python
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext

class MyCustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="my_custom_plugin")
        # Your initialization

    async def before_agent_callback(self, *, agent, callback_context):
        # Runs before agent starts
        pass

    async def after_agent_callback(self, *, agent, callback_context):
        # Runs after agent completes
        pass

    async def before_tool_callback(self, *, tool, callback_context):
        # Runs before any tool call
        pass

    async def before_model_callback(self, *, callback_context, llm_request):
        # Runs before LLM request
        pass

    async def on_model_error_callback(self, *, callback_context, error):
        # Runs when LLM errors occur
        pass
```

**Use cases:**
- Performance timing
- Cost tracking (token usage)
- Security auditing
- Custom metrics collection

## Evaluation Deep Dive

### Evaluation File Structure

**1. test_config.json** (Optional - defines thresholds)
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

**2. integration.evalset.json** (Required - test cases)
```json
{
  "eval_set_id": "my_test_suite",
  "eval_cases": [
    {
      "eval_id": "test_case_1",
      "conversation": [
        {
          "user_content": {"parts": [{"text": "User query"}]},
          "final_response": {"parts": [{"text": "Expected response"}]},
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "tool_name",
                "args": {"param": "value"}
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Evaluation Metrics Explained

**response_match_score:**
- Measures text similarity using algorithms like cosine similarity
- Range: 0.0 (completely different) to 1.0 (identical)
- Accounts for semantic meaning, not just exact word matching

```
Expected: "The light is now on"
Actual:   "I've turned on the light"
Score:    0.85 (high similarity despite different wording)
```

**tool_trajectory_avg_score:**
- Checks if correct tools were called with correct parameters
- Range: 0.0 (wrong tools) to 1.0 (perfect match)
- Validates both tool selection and parameter values

```
Expected: set_device_status(location="kitchen", device_id="light", status="ON")
Actual:   set_device_status(location="kitchen", device_id="light", status="ON")
Score:    1.0 (perfect match)
```

### Creating Test Cases from Web UI

**Step-by-step:**
1. Start ADK web UI: `adk web`
2. Select your agent from dropdown
3. Have a normal conversation
4. Click "Eval" tab in right panel
5. Click "Create Evaluation set"
6. Name your eval set (e.g., "happy_path_tests")
7. Click ">" arrow next to your eval set
8. Click "Add current session"
9. Give the test case a name
10. Files are automatically created in `.adk/eval_sets/`

**Benefits:**
- No manual JSON writing
- Captures real conversation flow
- Includes tool calls automatically
- Easy iteration

### Running CLI Evaluation

```bash
# Basic evaluation
adk eval <agent_dir> <evalset.json>

# With custom config
adk eval <agent_dir> <evalset.json> --config_file_path=<config.json>

# With detailed output
adk eval <agent_dir> <evalset.json> --print_detailed_results

# Example
adk eval home_automation_agent integration.evalset.json \
  --config_file_path=test_config.json \
  --print_detailed_results
```

**Output includes:**
- Pass/fail summary for each test
- Individual metric scores
- Actual vs expected comparison tables
- Detailed diff for failures

## Common Issues and Solutions

### Observability Issues

#### Issue: Can't see DEBUG logs
**Solution:**
- Check log level: Use `--log_level DEBUG`
- Verify log file location: `cat logger.log`
- Ensure logging is configured before agent runs

#### Issue: Logs are too verbose
**Solution:**
- Use INFO level for production: `--log_level INFO`
- Filter logs with grep: `cat logger.log | grep ERROR`
- Implement custom plugin with selective logging

#### Issue: Can't access ADK web UI
**Solution:**
- Check if port 8000 is available
- Verify: `adk web` command is running
- Local access: http://127.0.0.1:8000
- For Kaggle: Use proxy URL helper

### Evaluation Issues

#### Issue: All tests failing with low response_match_score
**Solution:**
- Agent response format changed
- Update expected responses in evalset
- Or lower threshold in config (e.g., 0.7 instead of 0.8)

```json
{
  "criteria": {
    "response_match_score": 0.7  // Lower threshold
  }
}
```

#### Issue: tool_trajectory_avg_score always 0.0
**Solution:**
- Check parameter order in expected vs actual
- Verify tool names match exactly (case-sensitive)
- Ensure parameter types match (string vs number)

```json
// Incorrect - parameters in wrong order
"args": {"status": "ON", "location": "kitchen"}

// Correct - must match actual call order
"args": {"location": "kitchen", "status": "ON"}
```

#### Issue: Can't find evalset file
**Solution:**
- Use absolute paths or correct relative paths
- Check file extension is `.evalset.json`
- Verify file is in specified location

```bash
# If file is in agent directory
adk eval my_agent my_agent/tests.evalset.json

# If file is in current directory
adk eval my_agent ./tests.evalset.json
```

#### Issue: Agent behavior is non-deterministic, tests flaky
**Solution:**
- Set temperature=0 for deterministic responses
- Increase response_match_score threshold tolerance
- Focus on tool_trajectory (more stable than text)

```python
model=Gemini(
    model="gemini-2.5-flash-lite",
    generation_config={"temperature": 0}  // Deterministic
)
```

## Best Practices

### Observability Best Practices

1. **Development Phase**
   ```bash
   # Use DEBUG logging liberally
   adk web --log_level DEBUG

   # Check logs frequently
   tail -f logger.log
   ```

2. **Production Phase**
   ```python
   # Use LoggingPlugin for automatic capture
   runner = InMemoryRunner(
       agent=agent,
       plugins=[LoggingPlugin()]
   )
   ```

3. **Custom Monitoring**
   ```python
   # Track domain-specific metrics
   class CostTrackingPlugin(BasePlugin):
       async def after_model_callback(self, *, callback_context, llm_response):
           tokens = llm_response.usage_metadata.total_token_count
           self.total_cost += tokens * COST_PER_TOKEN
   ```

### Evaluation Best Practices

1. **Build Comprehensive Test Suites**
   ```
   test_suite/
   ├── happy_path.evalset.json       # Basic functionality
   ├── edge_cases.evalset.json       # Unusual inputs
   ├── error_handling.evalset.json   # Invalid requests
   └── multi_turn.evalset.json       # Complex conversations
   ```

2. **Set Realistic Thresholds**
   ```json
   {
     "criteria": {
       // Critical operations - require perfection
       "tool_trajectory_avg_score": 1.0,

       // Communication - allow some flexibility
       "response_match_score": 0.75
     }
   }
   ```

3. **Iterate on Failures**
   ```bash
   # 1. Run evaluation
   adk eval agent tests.evalset.json --print_detailed_results

   # 2. Analyze failures
   # Look at actual vs expected diff

   # 3. Fix agent or update test expectations

   # 4. Re-run to verify
   adk eval agent tests.evalset.json
   ```

4. **CI/CD Integration**
   ```yaml
   # .github/workflows/test.yml
   - name: Run Agent Evaluation
     run: |
       adk eval my_agent tests/integration.evalset.json \
         --config_file_path=tests/config.json
   ```

5. **Track Metrics Over Time**
   ```python
   # Store evaluation results
   timestamp = datetime.now().isoformat()
   results_file = f"eval_results/{timestamp}.json"

   # Plot trends
   # Has response quality improved?
   # Are tool calls more accurate?
   ```

## Advanced Topics

### User Simulation

**ConversationScenario Structure:**
```json
{
  "user_goal": "Book a flight to Paris",
  "conversation_plan": [
    "Ask about available flights",
    "Inquire about prices",
    "Request specific departure times",
    "Complete the booking"
  ]
}
```

**Benefits:**
- Discovers edge cases you didn't think of
- Tests agent adaptability
- More realistic than static tests
- Automated test generation

**Learn more:** [ADK User Simulation Docs](https://google.github.io/adk-docs/evaluate/user-sim/)

### Advanced Evaluation Criteria

**With Google Cloud credentials:**
```json
{
  "criteria": {
    "safety_v1": 0.9,          // Detect harmful content
    "hallucinations_v1": 0.85,  // Check factual accuracy
    "custom_metric": 0.8        // Your custom evaluator
  }
}
```

**Learn more:** [Vertex AI Evaluation Criteria](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval)

## Debugging Workflow

### Complete Debugging Process

1. **Observe the Symptom**
   ```
   User: "Find papers on AI"
   Agent: "I cannot help with that"
   ```

2. **Check Logs**
   ```bash
   cat logger.log | grep ERROR
   # Or use adk web with DEBUG
   ```

3. **Analyze Traces**
   - Which tools were attempted?
   - What LLM prompts were sent?
   - Where did the error occur?

4. **Identify Root Cause**
   - Missing tool configuration?
   - Incorrect prompt instructions?
   - API error?
   - Tool parameter mismatch?

5. **Fix and Verify**
   - Update agent definition
   - Re-run with same input
   - Confirm fix works
   - Add test case to prevent regression

## Learning Resources

### ADK Documentation
- [Observability Overview](https://google.github.io/adk-docs/observability/logging/)
- [Custom Plugins](https://google.github.io/adk-docs/plugins/)
- [Cloud Trace Integration](https://google.github.io/adk-docs/observability/cloud-trace/)
- [Evaluation Overview](https://google.github.io/adk-docs/evaluate/)
- [Evaluation Criteria](https://google.github.io/adk-docs/evaluate/criteria/)
- [User Simulation](https://google.github.io/adk-docs/evaluate/user-sim/)

### Advanced Topics
- [Pytest-based Evaluation](https://google.github.io/adk-docs/evaluate/#2-pytest-run-tests-programmatically)
- [Vertex AI Evaluation Metrics](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval)

## Next Steps

After completing Day 4, you've learned:
- ✅ How to debug agents with observability tools
- ✅ Production monitoring with LoggingPlugin
- ✅ Creating custom plugins for specialized needs
- ✅ Building comprehensive test suites
- ✅ Running systematic evaluations
- ✅ Analyzing and fixing evaluation failures

**Continue to Day 5** to learn about:
- Deploying agents to production
- Agent2Agent protocol
- Scaling considerations
- Production best practices

**Practice Exercises:**
1. Add LoggingPlugin to your Day 3 memory agents
2. Create evaluation test suites for your existing agents
3. Build a custom plugin to track token usage costs
4. Implement user simulation for your use case
5. Integrate evaluation into a CI/CD workflow

Happy debugging and testing! 🔍✅
