"""
Day 2a: Agent Tools
This script demonstrates creating custom tools for AI agents:
- Function Tools (custom Python functions as tools)
- Agent Tools (using agents as tools for delegation)
- Built-in Code Executor for reliable calculations

Prerequisites:
- pip install google-adk python-dotenv
- Create a .env file with your GOOGLE_API_KEY
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
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
# Example 1: Custom Function Tools - Currency Converter
# ============================================================================

def get_fee_for_payment_method(method: str) -> dict:
    """Looks up the transaction fee percentage for a given payment method.

    This tool simulates looking up a company's internal fee structure based on
    the name of the payment method provided by the user.

    Args:
        method: The name of the payment method. It should be descriptive,
                e.g., "platinum credit card" or "bank transfer".

    Returns:
        Dictionary with status and fee information.
        Success: {"status": "success", "fee_percentage": 0.02}
        Error: {"status": "error", "error_message": "Payment method not found"}
    """
    fee_database = {
        "platinum credit card": 0.02,  # 2%
        "gold debit card": 0.035,  # 3.5%
        "bank transfer": 0.01,  # 1%
    }

    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    else:
        return {
            "status": "error",
            "error_message": f"Payment method '{method}' not found",
        }


def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: The ISO 4217 currency code of the currency you
                       are converting from (e.g., "USD").
        target_currency: The ISO 4217 currency code of the currency you
                         are converting to (e.g., "EUR").

    Returns:
        Dictionary with status and rate information.
        Success: {"status": "success", "rate": 0.93}
        Error: {"status": "error", "error_message": "Unsupported currency pair"}
    """
    # Static data simulating a live exchange rate API
    rate_database = {
        "usd": {
            "eur": 0.93,  # Euro
            "jpy": 157.50,  # Japanese Yen
            "inr": 83.58,  # Indian Rupee
        }
    }

    base = base_currency.lower()
    target = target_currency.lower()

    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}",
        }


def create_basic_currency_agent(retry_config):
    """Create a currency converter agent with custom function tools."""
    print("\n--- Creating Basic Currency Agent ---")

    currency_agent = LlmAgent(
        name="currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant.

        For currency conversion requests:
        1. Use `get_fee_for_payment_method()` to find transaction fees
        2. Use `get_exchange_rate()` to get currency conversion rates
        3. Check the "status" field in each tool's response for errors
        4. Calculate the final amount after fees
        5. First, state the final converted amount. Then, explain how you got that result.""",
        tools=[get_fee_for_payment_method, get_exchange_rate],
    )

    print("✅ Basic currency agent created with custom function tools")
    return currency_agent


# ============================================================================
# Example 2: Agent Tools - Using Agents as Tools
# ============================================================================

def create_calculation_agent(retry_config):
    """Create a calculation specialist agent that generates Python code."""
    calculation_agent = LlmAgent(
        name="CalculationAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized calculator that ONLY responds with Python code.

        **RULES:**
        1. Your output MUST be ONLY a Python code block.
        2. Do NOT write any text before or after the code block.
        3. The Python code MUST calculate the result.
        4. The Python code MUST print the final result to stdout.
        5. You are PROHIBITED from performing the calculation yourself.""",
        code_executor=BuiltInCodeExecutor(),
    )

    return calculation_agent


def create_enhanced_currency_agent(retry_config):
    """Create an enhanced currency agent that delegates calculations to a specialist."""
    print("\n--- Creating Enhanced Currency Agent with Agent Tools ---")

    # Create the calculation specialist
    calculation_agent = create_calculation_agent(retry_config)

    # Create the enhanced currency agent
    enhanced_currency_agent = LlmAgent(
        name="enhanced_currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant.

        For any currency conversion request:
        1. Get Transaction Fee: Use get_fee_for_payment_method()
        2. Get Exchange Rate: Use get_exchange_rate()
        3. Error Check: Check the "status" field in each response
        4. Calculate Final Amount: You MUST use the calculation_agent tool to generate
           Python code that calculates the final converted amount.
        5. Provide Detailed Breakdown: State the final amount and explain the calculation.""",
        tools=[
            get_fee_for_payment_method,
            get_exchange_rate,
            AgentTool(agent=calculation_agent),  # Using another agent as a tool!
        ],
    )

    print("✅ Enhanced currency agent created")
    print("🎯 New capability: Delegates calculations to specialist agent")
    return enhanced_currency_agent


# ============================================================================
# Main Execution
# ============================================================================

async def test_basic_currency_agent(agent):
    """Test the basic currency agent."""
    print("\n" + "="*80)
    print("  Example 1: Basic Currency Agent (Manual Calculations)")
    print("="*80)

    runner = InMemoryRunner(agent=agent)
    query = "I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?"

    print(f"\nQuery: {query}\n")

    response = await runner.run_debug(query)

    print("\n✅ Basic currency conversion completed!")


async def test_enhanced_currency_agent(agent):
    """Test the enhanced currency agent with calculation delegation."""
    print("\n" + "="*80)
    print("  Example 2: Enhanced Currency Agent (Code-Based Calculations)")
    print("="*80)

    runner = InMemoryRunner(agent=agent)
    query = "Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation."

    print(f"\nQuery: {query}\n")

    response = await runner.run_debug(query)

    print("\n✅ Enhanced currency conversion with code execution completed!")


async def main():
    """Main function demonstrating agent tools."""
    print("\n" + "="*80)
    print("  Day 2a: Agent Tools")
    print("="*80)

    # Setup
    setup_api_key()
    retry_config = create_retry_config()

    print("\n📚 Key Concepts:")
    print("1. Function Tools - Turn Python functions into agent tools")
    print("2. Agent Tools - Use specialist agents as tools for delegation")
    print("3. Built-in Code Executor - Reliable calculations via code generation")

    # Example 1: Basic currency agent with custom function tools
    basic_agent = create_basic_currency_agent(retry_config)
    await test_basic_currency_agent(basic_agent)

    # Example 2: Enhanced currency agent with agent tools
    enhanced_agent = create_enhanced_currency_agent(retry_config)
    await test_enhanced_currency_agent(enhanced_agent)

    print("\n" + "="*80)
    print("  ✅ All examples completed!")
    print("="*80)

    print("\n📖 Key Takeaways:")
    print("- Function Tools: Any Python function can become an agent tool")
    print("- Agent Tools: Agents can delegate to specialist agents")
    print("- Code Execution: More reliable than LLM arithmetic")
    print("- Tool Types: ADK supports custom and built-in tools")

    print("\n🎯 Next: Check out day_2b_agent_tools_best_practices.py")
    print("   Learn about MCP integration and long-running operations!")


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
