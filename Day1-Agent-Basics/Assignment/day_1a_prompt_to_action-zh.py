"""
第 1a 天：从提示词到行动
此脚本演示使用 Google ADK 构建你的第一个 AI 智能体。
智能体可以使用工具来回答问题。

先决条件：
- pip install google-adk python-dotenv litellm
- 创建包含你的 DOUBAO_API_KEY 的 .env 文件
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner


def setup_api_key():
    """
    从 .env 文件配置豆包 API key。
    在项目根目录中查找 .env 文件。
    """
    # 从项目根目录（Day-1 文件夹的上一级）加载 .env 文件
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("DOUBAO_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 DOUBAO_API_KEY。请执行以下操作：\n"
            "1. 在项目根目录中将 .env.example 复制为 .env\n"
            "2. 将您的 API key 添加到 .env 文件中\n"
        )
    print("✅ 已从 .env 文件加载豆包 API key。")
    return api_key


def create_basic_agent():
    """
    创建一个基本智能体。

    智能体可以：
    - 回答问题
    - 提供智能响应
    """
    agent = Agent(
        name="helpful_assistant",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        description="一个可以回答一般问题的简单智能体。",
        instruction="你是一个有用的助手。",
    )
    print("✅ 已创建基本智能体。")
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
    print("响应已接收！")
    print(f"{'='*60}\n")


async def main():
    """
    演示智能体功能的主函数。
    """
    print("\n" + "="*60)
    print("第 1a 天：从提示词到行动")
    print("构建你的第一个 AI 智能体（使用豆包 API）")
    print("="*60 + "\n")

    # 设置
    setup_api_key()
    agent = create_basic_agent()

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
    print("- 它知道何时使用 Google Search 等工具")
    print("- 它可以提供最新信息")
    print("\n下一步：查看 day_1b_agent_architectures-zh.py 了解多智能体系统！")


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
