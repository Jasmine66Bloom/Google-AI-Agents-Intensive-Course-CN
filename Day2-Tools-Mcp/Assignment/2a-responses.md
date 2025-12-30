================================================================================
  Day 2a: Agent Tools
================================================================================
✅ Gemini API key loaded from .env file.

📚 Key Concepts:
1. Function Tools - Turn Python functions into agent tools
2. Agent Tools - Use specialist agents as tools for delegation
3. Built-in Code Executor - Reliable calculations via code generation

--- Creating Basic Currency Agent ---
✅ Basic currency agent created with custom function tools

================================================================================
  Example 1: Basic Currency Agent (Manual Calculations)
================================================================================

Query: I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?


 ### Created new session: debug_session_id

User > I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?
Warning: there are non-text parts in the response: ['function_call', 'function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
currency_agent > You will receive 455.7 Euros.

Here's how to calculate that:

1. **Exchange Rate**: 1 USD = 0.93 EUR
2. **Fee**: The transaction fee for using a Platinum Credit Card is 2%.
3. **Amount after fee**:
   - First, calculate the fee amount: 500 USD * 0.02 = 10 USD
   - Then, subtract the fee from the initial amount: 500 USD - 10 USD = 490 USD
   - Finally, convert the remaining amount to Euros: 490 USD * 0.93 EUR/USD = 455.7 EUR

✅ Basic currency conversion completed!

--- Creating Enhanced Currency Agent with Agent Tools ---
✅ Enhanced currency agent created
🎯 New capability: Delegates calculations to specialist agent

================================================================================
  Example 2: Enhanced Currency Agent (Code-Based Calculations)
================================================================================

Query: Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation.


 ### Created new session: debug_session_id

User > Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation.
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Warning: there are non-text parts in the response: ['executable_code', 'code_execution_result'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.

✅ Enhanced currency conversion with code execution completed!

================================================================================
  ✅ All examples completed!
================================================================================

📖 Key Takeaways:
- Function Tools: Any Python function can become an agent tool
- Agent Tools: Agents can delegate to specialist agents
- Code Execution: More reliable than LLM arithmetic
- Tool Types: ADK supports custom and built-in tools

🎯 Next: Check out day_2b_agent_tools_best_practices.py
   Learn about MCP integration and long-running operations!