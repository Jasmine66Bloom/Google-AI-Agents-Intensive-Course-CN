# Day 2 - Agent Tools & Best Practices

This folder contains Python scripts based on the Day 2 Jupyter notebooks from the Kaggle 5-day Agents course.

## Scripts Overview

### 1. `day_2a_agent_tools.py`
**Agent Tools - Custom Functions and Delegation**

This script demonstrates:
- Creating custom function tools (currency converter example)
- Using Python functions as agent tools
- Agent Tools pattern (using agents as tools for delegation)
- Built-in Code Executor for reliable calculations
- Complete guide to ADK tool types

**Key Concepts:**
- Function Tools: Turn any Python function into an agent tool
- Agent Tools: Delegate tasks to specialist agents
- Code Execution: More reliable than LLM arithmetic
- Tool orchestration and error handling

**Example Use Cases:**
- Currency conversion with fee calculations
- Delegating complex calculations to specialist agents
- Business logic encapsulation in tools

### 2. `day_2b_agent_tools_best_practices.py`
**Advanced Tool Patterns - MCP and Long-Running Operations**

This script demonstrates:
- Model Context Protocol (MCP) integration concepts
- Long-Running Operations (LRO) with human-in-the-loop
- Pausable and resumable workflows
- State management across conversation breaks
- Approval workflows for critical operations

**Key Concepts:**
- MCP: Connect to external services without custom integration
- LRO: Pause workflows for human approval
- Resumability: Maintain state when paused
- Tool Context: Access and manage approval status

**Example Use Cases:**
- Shipping orders requiring approval for large quantities
- Financial transactions needing human oversight
- Any operation that needs external input before completing

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

### Run Script 2a (Agent Tools)

```bash
# Make sure you're in the Day-2 directory and venv is activated
python day_2a_agent_tools.py
```

**What it does:**
- Creates a currency converter agent with custom tools
- Demonstrates function tools for fees and exchange rates
- Shows agent delegation to a calculation specialist
- Compares manual calculations vs code-generated calculations

### Run Script 2b (Best Practices)

```bash
python day_2b_agent_tools_best_practices.py
```

**What it does:**
- Explains MCP integration concepts
- Demonstrates long-running operations with approval workflows
- Tests three scenarios:
  1. Small order (auto-approved)
  2. Large order (paused for approval - approved)
  3. Large order (paused for approval - rejected)

**Note:** The MCP section explains the concept without requiring Node.js installation. To actually run MCP servers, you would need Node.js and npx installed.

## Understanding the Output

### Day 2a Output
You'll see:
- Custom function tools being called (fee lookup, exchange rates)
- Basic currency conversion with manual calculations
- Enhanced conversion using code generation for precise math
- Agent delegation to calculation specialist

### Day 2b Output
You'll see:
- MCP architecture and usage explanation
- Long-running operation workflows:
  - Status: "approved" for small orders
  - Status: "pending" → pause → resume for large orders
  - Human decision simulation (approve/reject)
  - Final status after resuming

## Key Patterns and When to Use Them

### Function Tools
**When to use:**
- You have business logic to encapsulate
- You need custom calculations or data lookups
- You want to connect to internal systems

**Pattern:**
```python
def my_custom_tool(param: str) -> dict:
    """Clear docstring helps LLM understand the tool."""
    # Your business logic
    return {"status": "success", "data": result}

agent = LlmAgent(
    tools=[my_custom_tool],  # Just add function to tools list
)
```

### Agent Tools (Delegation)
**When to use:**
- Task needs specialist expertise
- Want to reuse agents across systems
- Need modular, composable agent architectures

**Pattern:**
```python
specialist_agent = LlmAgent(...)  # Create specialist

main_agent = LlmAgent(
    tools=[AgentTool(agent=specialist_agent)],  # Use as tool
)
```

### Long-Running Operations
**When to use:**
- Financial transactions requiring approval
- Bulk operations needing confirmation
- Compliance checkpoints
- Any operation that must pause for external input

**Pattern:**
```python
def my_pausable_tool(param: str, tool_context: ToolContext) -> dict:
    if needs_approval:
        tool_context.request_confirmation(hint="Approve?")
        return {"status": "pending"}

    if tool_context.tool_confirmation.confirmed:
        # Approved - proceed
        return {"status": "approved"}

# Wrap agent in App with resumability
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
```

## Tool Types Quick Reference

| Tool Type | What It Does | Use Case |
|-----------|-------------|----------|
| **Function Tools** | Python functions as tools | Custom business logic |
| **Agent Tools** | Agents as tools | Delegation, specialization |
| **Code Executor** | Runs Python code | Reliable calculations |
| **MCP Tools** | External service integration | GitHub, Slack, databases |
| **Long-Running** | Pausable operations | Human approvals, time-spanning tasks |

## Common Issues and Solutions

### Issue: "Tool not found" or agent doesn't use tool
**Solution:**
- Check tool's docstring is clear and descriptive
- Ensure tool name in agent instructions matches function name
- Verify tool is in the agent's `tools=[]` list

### Issue: Long-running operation doesn't pause
**Solution:**
- Verify `tool_context: ToolContext` parameter in function signature
- Check that App has `resumability_config` enabled
- Ensure you're using `Runner` with `app=` not `agent=`

### Issue: Agent gives wrong calculations
**Solution:**
- Use Agent Tools pattern to delegate to code-generating specialist
- Add `code_executor=BuiltInCodeExecutor()` to calculation agent
- Instruct agent to generate code, not calculate directly

## Learning Resources

- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
- [ADK Function Tools Guide](https://google.github.io/adk-docs/tools/function-tools/)
- [ADK MCP Tools](https://google.github.io/adk-docs/tools/mcp-tools/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ADK Runtime (Sessions, Runners)](https://google.github.io/adk-docs/runtime/)

## Best Practices

### Writing Good Tool Functions

1. **Clear Docstrings:** LLMs use these to understand when/how to use tools
```python
def my_tool(param: str) -> dict:
    """Brief description of what this tool does.

    Args:
        param: Clear parameter description

    Returns:
        Dictionary with status and data
    """
```

2. **Type Hints:** Enable proper schema generation
```python
def my_tool(count: int, name: str) -> dict:
    # ADK uses type hints to validate input
```

3. **Structured Returns:** Always return dict with status
```python
# Success
return {"status": "success", "data": result}

# Error
return {"status": "error", "error_message": "What went wrong"}
```

4. **Error Handling:** Handle exceptions gracefully
```python
try:
    result = risky_operation()
    return {"status": "success", "data": result}
except Exception as e:
    return {"status": "error", "error_message": str(e)}
```

### Tool Naming Conventions

- Use descriptive, verb-based names: `get_exchange_rate`, `place_order`
- Be specific: `calculate_shipping_cost` vs `calculate`
- Match business domain language

### Agent Instructions for Tools

- Reference tools by exact function name
- Explain when to use each tool
- Specify the sequence of tool calls if order matters
- Describe how to handle tool errors

## Advanced: MCP Integration

To use MCP servers in production (requires Node.js):

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

# Example: Everything MCP Server
mcp_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
        ),
        timeout=30,
    )
)

agent = LlmAgent(
    tools=[mcp_server],
)
```

Available MCP servers:
- **Kaggle**: Dataset and notebook operations
- **GitHub**: Repository and PR management
- **Google Maps**: Location services
- **Slack**: Team communication
- Many more at [modelcontextprotocol.io/examples](https://modelcontextprotocol.io/examples)

## Next Steps

After completing Day 2:
- You understand how to create custom agent tools
- You can delegate tasks to specialist agents
- You know how to implement approval workflows
- You're ready for Day 3: State and Memory Management

**Continue Learning:**
- Review the Day 2 notebooks for detailed explanations
- Try modifying the examples with your own business logic
- Explore the ADK documentation for more tool types

Happy coding! 🚀
