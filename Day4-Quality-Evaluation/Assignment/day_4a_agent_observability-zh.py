"""
第4天A：代理可观测性 - 日志、追踪和指标

本笔记本涵盖：
- 理解什么是代理可观测性以及为什么它很重要
- 使用 ADK Web UI 进行交互式调试
- 实现 LoggingPlugin 用于生产可观测性
- 创建自定义插件和回调
- 理解日志、追踪和指标

版权所有 2025 Google LLC。
根据 Apache 许可证 2.0 版本获得许可
"""

import os
import logging
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.genai import types
from typing import List

# ============================================================================
# 设置和配置
# ============================================================================

# 从 .env 文件加载环境变量
from dotenv import load_dotenv

load_dotenv()

# 验证 API 密钥已设置
if not os.getenv("DOUBAO_API_KEY"):
    print("❌ 错误：在环境变量中未找到 DOUBAO_API_KEY")
    print("   请确保您有一个设置了 DOUBAO_API_KEY 的 .env 文件")
    exit(1)

print("✅ ADK 组件导入成功。")
print("✅ API 密钥从 .env 文件加载")

# ============================================================================
# 配置日志记录
# ============================================================================


def setup_logging():
    """设置具有 DEBUG 级别的日志记录配置"""
    # 清理任何先前的日志
    for log_file in ["logger.log", "web.log", "tunnel.log"]:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"🧹 已清理 {log_file}")

    # 配置具有 DEBUG 日志级别的日志记录
    logging.basicConfig(
        filename="logger.log",
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
    )

    print("✅ 日志记录已配置")


MODEL_NAME = "volcengine/doubao-1-5-lite-32k-250115"

# ============================================================================
# 第2节：研究论文查找代理（故意破坏）
# ============================================================================


def count_papers_broken(papers: str):
    """
    此函数计算字符串列表中的论文数量。

    故意错误：接受 str 而不是 List[str]

    参数：
      papers：字符串列表，其中每个字符串是一篇研究论文。
    返回：
      列表中的论文数量。
    """
    return len(papers)


def count_papers_fixed(papers: List[str]):
    """
    此函数计算字符串列表中的论文数量。

    已修复：现在正确接受 List[str]

    参数：
      papers：字符串列表，其中每个字符串是一篇研究论文。
    返回：
      列表中的论文数量。
    """
    return len(papers)


def create_research_agent_broken():
    """创建一个带有故意错误的研究代理用于调试练习"""

    # 搜索代理
    search_agent = LlmAgent(
        name="search_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        description="查找信息",
        instruction="""查找有关给定主题的信息。
        返回搜索结果。
        如果用户要求论文列表，则给他们您找到的研究论文列表
        而不是摘要。""",
    )

    # 带有破坏的 count_papers 工具的根代理
    root_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""您的任务是查找研究论文并计算它们。

        您必须始终遵循以下步骤：
        1) 使用 'search_agent' 查找用户提供的主题的研究论文。
        2) 然后，将论文传递给 'count_papers' 工具以计算返回的论文数量。
        3) 返回研究论文列表和论文总数。
        """,
        tools=[AgentTool(agent=search_agent), count_papers_broken],
    )

    return root_agent


def create_research_agent_fixed():
    """创建一个修复了错误的研究代理"""

    # 搜索代理
    search_agent = LlmAgent(
        name="search_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        description="查找信息",
        instruction="""查找有关给定主题的信息。
        返回搜索结果。
        如果用户要求论文列表，则给他们您找到的研究论文列表
        而不是摘要。""",
    )

    # 带有修复的 count_papers 工具的根代理
    root_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""您的任务是查找研究论文并计算它们。

        您必须始终遵循以下步骤：
        1) 使用 'search_agent' 查找用户提供的主题的研究论文。
        2) 然后，将论文传递给 'count_papers' 工具以计算返回的论文数量。
        3) 返回研究论文列表和论文总数。
        """,
        tools=[AgentTool(agent=search_agent), count_papers_fixed],
    )

    return root_agent


# ============================================================================
# 第3节：自定义插件示例
# ============================================================================


class CountInvocationPlugin(BasePlugin):
    """一个计算代理和工具调用的自定义插件。"""

    def __init__(self) -> None:
        """使用计数器初始化插件。"""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """计算代理运行。"""
        self.agent_count += 1
        logging.info(f"[Plugin] 代理运行计数：{self.agent_count}")
        print(f"[CountPlugin] 代理调用 #{self.agent_count}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """计算 LLM 请求。"""
        self.llm_request_count += 1
        logging.info(f"[Plugin] LLM 请求计数：{self.llm_request_count}")
        print(f"[CountPlugin] LLM 请求 #{self.llm_request_count}")


# ============================================================================
# 第3节：在生产环境中使用 LoggingPlugin
# ============================================================================


def create_agent_with_logging_plugin():
    """创建带有 LoggingPlugin 的研究代理以实现全面的可观测性"""

    # 搜索代理
    search_agent = LlmAgent(
        name="search_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        description="查找信息",
        instruction="查找有关给定主题的信息。返回搜索结果。",
    )

    # 带有修复工具的根代理
    research_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""您的任务是查找研究论文并计算它们。

       您必须遵循以下步骤：
       1) 使用 'search_agent' 查找用户提供的主题的研究论文。
       2) 然后，将论文传递给 'count_papers' 工具以计算返回的论文数量。
       3) 返回研究论文列表和论文总数。
       """,
        tools=[AgentTool(agent=search_agent), count_papers_fixed],
    )

    # 创建带有 LoggingPlugin 的运行器
    runner = InMemoryRunner(
        agent=research_agent,
        plugins=[LoggingPlugin()],  # 处理标准可观测性日志记录
    )

    return runner


# ============================================================================
# 演示函数
# ============================================================================


async def demo_broken_agent():
    """演示破坏的代理用于调试练习"""
    print("\n" + "=" * 80)
    print("演示：破坏的代理（用于调试练习）")
    print("=" * 80)
    print("\n🐛 此代理在 count_papers 工具中有故意错误")
    print("该工具期望 'str' 但应该接受 'List[str]'")
    print("\n👉 在实际场景中，您将：")
    print("   1. 运行 'adk web --log_level DEBUG' 启动 Web UI")
    print("   2. 使用以下内容测试代理：'查找最新的量子计算论文'")
    print("   3. 使用事件选项卡和追踪查找错误")
    print("   4. 查看 function_call 以查看不正确的参数类型")

    agent = create_research_agent_broken()
    runner = InMemoryRunner(agent=agent)

    print("\n⚠️  注意：这是一个演示脚本。要实际调试：")
    print("   - 创建代理文件夹：adk create research-agent")
    print("   - 将代理定义复制到 agent.py")
    print("   - 运行：adk web --log_level DEBUG")
    print("   - 使用 Web UI 进行交互和调试")


async def demo_logging_plugin():
    """演示用于生产可观测性的 LoggingPlugin"""
    print("\n" + "=" * 80)
    print("演示：带有 LoggingPlugin 的研究代理")
    print("=" * 80)

    setup_logging()

    runner = create_agent_with_logging_plugin()

    print("\n🚀 使用 LoggingPlugin 运行代理...")
    print("📊 观看全面的日志记录输出：\n")

    response = await runner.run_debug("查找最近的量子计算论文")

    print("\n✅ 代理执行完成！")
    print("\n📋 关键观察：")
    print("• LoggingPlugin 自动捕获了所有代理活动")
    print("• 日志包括：用户消息、代理响应、工具调用、计时数据")
    print("• 检查 logger.log 文件以获取详细的 DEBUG 日志")
    print("• 此方法可扩展用于生产系统")


async def demo_custom_plugin():
    """演示创建和使用自定义插件"""
    print("\n" + "=" * 80)
    print("演示：自定义插件（CountInvocationPlugin）")
    print("=" * 80)

    setup_logging()

    # 创建带有自定义插件的代理
    agent = create_research_agent_fixed()
    custom_plugin = CountInvocationPlugin()

    runner = InMemoryRunner(
        agent=agent,
        plugins=[custom_plugin],
    )

    print("\n🎯 使用自定义 CountInvocationPlugin 运行代理...")
    print("此插件计算代理调用和 LLM 请求\n")

    response = await runner.run_debug("查找机器学习论文")

    print("\n📊 自定义插件统计：")
    print(f"   • 代理调用：{custom_plugin.agent_count}")
    print(f"   • LLM 请求：{custom_plugin.llm_request_count}")
    print("\n💡 自定义插件允许您添加任何您需要的可观测性逻辑！")


# ============================================================================
# 主函数
# ============================================================================


async def main():
    """运行所有可观测性演示"""

    print("\n" + "=" * 80)
    print("第4天A：代理可观测性")
    print("=" * 80)

    print("\n📚 您将学到：")
    print("• 使用 ADK Web UI 和 DEBUG 日志调试代理")
    print("• 使用 LoggingPlugin 进行生产可观测性")
    print("• 创建自定义插件以满足特殊需求")
    print("• 理解日志、追踪和指标")

    # 演示1：破坏的代理
    await demo_broken_agent()

    # 演示2：LoggingPlugin
    await demo_logging_plugin()

    # 演示3：自定义插件
    await demo_custom_plugin()

    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    print("\n❓ 何时使用哪种类型的日志记录？")
    print("1. 开发调试 → 使用 'adk web --log_level DEBUG'")
    print("2. 常见生产可观测性 → 使用 LoggingPlugin()")
    print("3. 自定义需求 → 构建自定义回调和插件")

    print("\n🎯 关键要点：")
    print("✅ 核心调试模式：症状 → 日志 → 根本原因 → 修复")
    print("✅ ADK Web UI 提供带有追踪的交互式调试")
    print("✅ LoggingPlugin 自动处理标准可观测性")
    print("✅ 自定义插件启用专门监控")

    print("\n📚 了解更多：")
    print("• ADK 可观测性：https://google.github.io/adk-docs/observability/logging/")
    print("• 自定义插件：https://google.github.io/adk-docs/plugins/")
    print("• Cloud Trace 集成：https://google.github.io/adk-docs/observability/cloud-trace/")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
