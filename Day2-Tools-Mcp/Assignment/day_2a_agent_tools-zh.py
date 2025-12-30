"""
Day 2a: 智能体工具
此脚本演示为 AI 智能体创建自定义工具：
- 函数工具（自定义 Python 函数作为工具）
- 智能体工具（使用智能体作为工具进行委托）
- 内置代码执行器，用于可靠计算

先决条件：
- pip install google-adk python-dotenv
- 创建一个包含你的 GOOGLE_API_KEY 的 .env 文件
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool


def setup_api_key():
    """从 .env 文件配置 Gemini API key。"""
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 GOOGLE_API_KEY。请执行以下操作：\n"
            "1. 在项目根目录中将 .env.example 复制为 .env\n"
            "2. 将你的 API key 添加到 .env 文件中\n"
            "3. 从以下位置获取 API key：https://aistudio.google.com/app/api-keys"
        )
    print("✅ 已从 .env 文件加载 Gemini API key。")
    return api_key


# ============================================================================
# 示例 1：自定义函数工具 - 货币转换器
# ============================================================================

def get_fee_for_payment_method(method: str) -> dict:
    """查找给定支付方式的交易费百分比。

    此工具模拟根据用户提供的支付方式名称
    查找公司的内部费用结构。

    Args:
        method: 支付方式的名称。它应该是描述性的，
                例如，"platinum credit card" 或 "bank transfer"。

    Returns:
        包含状态和费用信息的字典。
        成功：{"status": "success", "fee_percentage": 0.02}
        错误：{"status": "error", "error_message": "Payment method not found"}
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
    """查找并返回两种货币之间的汇率。

    Args:
        base_currency: 你要转换的货币的 ISO 4217 货币代码
                       （例如，"USD"）。
        target_currency: 你要转换到的货币的 ISO 4217 货币代码
                         （例如，"EUR"）。

    Returns:
        包含状态和汇率信息的字典。
        成功：{"status": "success", "rate": 0.93}
        错误：{"status": "error", "error_message": "Unsupported currency pair"}
    """
    # 模拟实时汇率 API 的静态数据
    rate_database = {
        "usd": {
            "eur": 0.93,  # 欧元
            "jpy": 157.50,  # 日元
            "inr": 83.58,  # 印度卢比
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


def create_basic_currency_agent():
    """创建一个带有自定义函数工具的货币转换智能体。"""
    print("\n--- 正在创建基础货币智能体 ---")

    currency_agent = LlmAgent(
        name="currency_agent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""You are a smart currency conversion assistant.

        For currency conversion requests:
        1. Use `get_fee_for_payment_method()` to find transaction fees
        2. Use `get_exchange_rate()` to get currency conversion rates
        3. Check the "status" field in each tool's response for errors
        4. Calculate the final amount after fees
        5. First, state the final converted amount. Then, explain how you got that result.""",
        tools=[get_fee_for_payment_method, get_exchange_rate],
    )

    print("✅ 已创建带有自定义函数工具的基础货币智能体")
    return currency_agent


# ============================================================================
# 示例 2：智能体工具 - 使用智能体作为工具
# ============================================================================

def create_calculation_agent():
    """创建一个计算专业智能体。"""
    calculation_agent = LlmAgent(
        name="CalculationAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""You are a specialized calculator.

        **RULES:**
        1. Calculate the result directly.
        2. Provide the final result clearly.
        3. Show your calculation steps when requested.""",
    )

    return calculation_agent


def create_enhanced_currency_agent():
    """创建一个将计算委托给专业人员的增强货币智能体。"""
    print("\n--- 正在创建带有智能体工具的增强货币智能体 ---")

    # 创建计算专业人员
    calculation_agent = create_calculation_agent()

    # 创建增强货币智能体
    enhanced_currency_agent = LlmAgent(
        name="enhanced_currency_agent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""You are a smart currency conversion assistant.

        For any currency conversion request:
        1. Get Transaction Fee: Use get_fee_for_payment_method()
        2. Get Exchange Rate: Use get_exchange_rate()
        3. Error Check: Check the "status" field in each response
        4. Calculate Final Amount: Use the calculation_agent tool to calculate the final converted amount.
        5. Provide Detailed Breakdown: State the final amount and explain the calculation.""",
        tools=[
            get_fee_for_payment_method,
            get_exchange_rate,
            AgentTool(agent=calculation_agent),  # 使用另一个智能体作为工具！
        ],
    )

    print("✅ 已创建增强货币智能体")
    print("🎯 新功能：将计算委托给专业智能体")
    return enhanced_currency_agent


# ============================================================================
# 主执行
# ============================================================================

async def test_basic_currency_agent(agent):
    """测试基础货币智能体。"""
    print("\n" + "="*80)
    print("  示例 1：基础货币智能体（手动计算）")
    print("="*80)

    runner = InMemoryRunner(agent=agent)
    query = "I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?"

    print(f"\nQuery: {query}\n")

    response = await runner.run_debug(query)

    print("\n✅ 基础货币兑换已完成！")


async def test_enhanced_currency_agent(agent):
    """测试带有计算委托的增强货币智能体。"""
    print("\n" + "="*80)
    print("  示例 2：增强货币智能体（基于智能体的计算）")
    print("="*80)

    runner = InMemoryRunner(agent=agent)
    query = "Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation."

    print(f"\nQuery: {query}\n")

    response = await runner.run_debug(query)

    print("\n✅ 带有智能体委托的增强货币兑换已完成！")


async def main():
    """演示智能体工具的主函数。"""
    print("\n" + "="*80)
    print("  Day 2a: 智能体工具")
    print("="*80)

    # 设置
    setup_api_key()

    print("\n📚 关键概念：")
    print("1. 函数工具 - 将 Python 函数转换为智能体工具")
    print("2. 智能体工具 - 使用专业智能体作为工具进行委托")
    print("3. 内置代码执行器 - 通过代码生成进行可靠计算")

    # 示例 1：带有自定义函数工具的基础货币智能体
    basic_agent = create_basic_currency_agent()
    await test_basic_currency_agent(basic_agent)

    # 示例 2：带有智能体工具的增强货币智能体
    enhanced_agent = create_enhanced_currency_agent()
    await test_enhanced_currency_agent(enhanced_agent)

    print("\n" + "="*80)
    print("  ✅ 所有示例已完成！")
    print("="*80)

    print("\n📖 关键要点：")
    print("- 函数工具：任何 Python 函数都可以成为智能体工具")
    print("- 智能体工具：智能体可以委托给专业智能体")
    print("- 代码执行：比 LLM 算术更可靠")
    print("- 工具类型：ADK 支持自定义和内置工具")

    print("\n🎯 下一步：查看 day_2b_agent_tools_best_practices.py")
    print("   了解 MCP 集成和长时间运行的操作！")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as e:
        print(f"\n❌ 错误：{e}")
    except KeyboardInterrupt:
        print("\n\n⏸️  脚本被用户中断。")
    except Exception as e:
        print(f"\n❌ 意外错误：{e}")
        raise
