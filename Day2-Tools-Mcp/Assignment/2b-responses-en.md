================================================================================
  Day 2b: Agent Tools Best Practices
================================================================================
✅ Gemini API key loaded from .env file.

📚 Advanced Patterns:
1. MCP Integration - Connect to external services
2. Long-Running Operations - Human-in-the-loop approvals
3. Resumable Workflows - Pause and resume with state management

--- Model Context Protocol (MCP) ---

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


✅ MCP concept explained


================================================================================
  Example: Long-Running Operations (Human-in-the-Loop)
================================================================================

--- Creating Long-Running Operation System ---
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/Day-2/day_2b_agent_tools_best_practices.py:213: UserWarning: [EXPERIMENTAL] ResumabilityConfig: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  resumability_config=ResumabilityConfig(is_resumable=True),
✅ Resumable shipping system created
🔧 Features:
  • Auto-approves small orders (≤5 containers)
  • Pauses for approval on large orders (>5 containers)
  • Maintains state across pause/resume

📋 Testing Three Scenarios:

1️⃣ Small Order (3 containers) - Auto-approve:

============================================================
User > Ship 3 containers to Singapore

Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Agent > Shipping order approved. Order ID: ORD-3-AUTO. 3 containers will be shipped to Singapore.
============================================================

2️⃣ Large Order (10 containers) - Approval Required - APPROVE:

============================================================
User > Ship 10 containers to Rotterdam

Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/tools/tool_context.py:92: UserWarning: [EXPERIMENTAL] ToolConfirmation: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  ToolConfirmation(
⏸️  Pausing for approval...
🤔 Human Decision: APPROVE ✅

/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/agents/invocation_context.py:298: UserWarning: [EXPERIMENTAL] BaseAgentState: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  self.agent_states[event.author] = BaseAgentState()
Agent > Shipping order approved: 10 containers to Rotterdam. The order ID is ORD-10-HUMAN.
============================================================

3️⃣ Large Order (8 containers) - Approval Required - REJECT:

============================================================
User > Ship 8 containers to Los Angeles

Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
⏸️  Pausing for approval...
🤔 Human Decision: REJECT ❌

Agent > Your shipping order for 8 containers to Los Angeles has been rejected.
============================================================

✅ All long-running operation scenarios completed!

================================================================================
  ✅ All examples completed!
================================================================================

📖 Key Takeaways:
- MCP: Connect to external services without custom integration
- LRO: Pause workflows for human approval or long-running tasks
- Resumability: Maintain state across conversation breaks
- Tool Context: Access approval status and request confirmation

🔑 When to Use Each Pattern:
┌───────────────────────┬──────────────────────────────────────────┐
│ Pattern               │ Use Case                                 │
├───────────────────────┼──────────────────────────────────────────┤
│ MCP Integration       │ Connect to external, standardized        │
│                       │ services (GitHub, databases, etc.)       │
├───────────────────────┼──────────────────────────────────────────┤
│ Long-Running Ops      │ Human approvals, compliance checks,      │
│                       │ or operations spanning time              │
└───────────────────────┴──────────────────────────────────────────┘

🎯 Next: Day 3 will cover State and Memory Management!