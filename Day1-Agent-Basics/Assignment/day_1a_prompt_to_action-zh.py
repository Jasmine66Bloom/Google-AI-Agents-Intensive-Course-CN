"""
第 1a 天：从提示词到行动
此脚本演示使用 Google ADK 构建你的第一个 AI 智能体。
智能体可以使用 Google Search 等工具来回答问题。

先决条件：
- pip install google-adk python-dotenv
- 创建包含你的 GOOGLE_API_KEY 的 .env 文件
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types


def setup_api_key():
    """
    从 .env 文件配置 Gemini API key。
    在项目根目录中查找 .env 文件。
    """
    # 从项目根目录（Day-1 文件夹的上一级）加载 .env 文件
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 GOOGLE_API_KEY。请：\n"
            "1. 将 .env.example 复制到项目根目录中的 .env\n"
            "2. 将你的 API key 添加到 .env 文件\n"
            "3. 从以下位置获取 API key：https://aistudio.google.com/app/api-keys"
        )
    print("✅ 已从 .env 文件加载 Gemini API key。")
    return api_key


def create_retry_config():
    """
    配置重试选项以处理瞬时错误。
    """
    return types.HttpRetryOptions(
        attempts=5,  # 最大重试次数
        exp_base=7,  # 延迟乘数
        initial_delay=1,  # 第一次重试前的初始延迟（以秒为单位）
        http_status_codes=[429, 500, 503, 504]  # 在这些 HTTP 错误上重试
    )


def create_basic_agent(retry_config):
    """
    创建一个带有 Google Search 工具的基本智能体。

    智能体可以：
    - 回答问题
    - 需要当前信息时使用 Google Search
    - 提供最新响应
    """
    agent = Agent(
        name="helpful_assistant",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        description="一个可以回答一般问题的简单智能体。",
        instruction="你是一个有用的助手。使用 Google Search 获取当前信息或如果不确定。",
        tools=[google_search],
    )
    print("✅ 已创建带有 Google Search 工具的智能体。")
    return agent


async def run_agent_query(agent, query):
    """
    通过智能体运行查询。

    参数：
        agent: Agent 实例
        query: 要问智能体的问题
    """
    print(f"\n{'='*60}")
    print(f"查询：{query}")
    print(f"{'='*60}\n")

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(query)

    print(f"\n{'='*60}")
    print("已收到响应！")
    print(f"{'='*60}\n")


async def main():
    """
    演示智能体功能的主函数。
    """
    print("\n" + "="*60)
    print("第 1a 天：从提示词到行动")
    print("构建你的第一个 AI 智能体")
    print("="*60 + "\n")

    # 设置
    setup_api_key()
    retry_config = create_retry_config()
    agent = create_basic_agent(retry_config)

    # 示例 1：关于 ADK 的查询
    print("\n--- 示例 1：询问关于智能体开发工具包 ---")
    await run_agent_query(
        agent,
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )

    # 示例 2：需要当前信息的查询
    print("\n--- 示例 2：询问当前信息 ---")
    await run_agent_query(
        agent,
        "What's weather in London?"
    )

    # 示例 3：你的自定义查询
    print("\n--- 示例 3：尝试你自己的查询 ---")
    custom_query = input("\n输入你的问题（或按 Enter 跳过）：").strip()
    if custom_query:
        await run_agent_query(agent, custom_query)

    print("\n" + "="*60)
    print("✅ 所有示例已完成！")
    print("="*60 + "\n")

    print("关键要点：")
    print("- 智能体不仅仅是响应——它会推理和行动")
    print("- 它知道何时使用像 Google Search 这样的工具")
    print("- 它可以提供最新信息")
    print("\n下一步：查看 day_1b_agent_architectures.py 了解多智能体系统！")


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
