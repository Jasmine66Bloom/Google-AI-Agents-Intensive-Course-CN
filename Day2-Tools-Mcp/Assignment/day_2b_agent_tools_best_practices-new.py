"""
Day 2b: 智能体工具最佳实践
此脚本演示高级智能体工具模式：
- 模型上下文协议（MCP）集成
- 人工参与的长时间运行操作
- 带有状态管理的可恢复工作流

先决条件：
- pip install google-adk python-dotenv
- 已安装 Node.js 和 npx（用于 MCP 服务器演示）
- 创建一个包含你的 DOUBAO_API_KEY 的 .env 文件

注意：MCP 示例需要 Node.js。长时间运行操作可独立运行。
"""

import os
import sys
import uuid
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.adk.tools.function_tool import FunctionTool
from google.adk.apps.app import App, ResumabilityConfig
from google.genai import types

# 添加项目根目录到sys.path，以便导入llm_client
sys.path.append(str(Path(__file__).parent.parent.parent))
from llm_client import AdkLlmWrapper


def setup_api_key():
    """从 .env 文件配置 LLM API key。"""
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 LLM_API_KEY。请执行以下操作：\n"
            "1. 在项目根目录中将 .env.example 复制为 .env\n"
            "2. 将你的 API key 添加到 .env 文件中"
        )
    print("✅ 已从 .env 文件加载 LLM API key。")
    return api_key


# ============================================================================
# 示例 1：模型上下文协议（MCP）集成
# ============================================================================

def demonstrate_mcp_concept():
    """解释 MCP 概念（实际的 MCP 服务器需要 Node.js/npx）。"""
    print("\n--- 模型上下文协议（MCP）---")
    print("""
📡 什么是 MCP？

MCP 是一个开放标准，允许智能体连接到外部服务
而无需编写自定义集成代码。

架构：
    ┌──────────────────┐
    │   你的智能体     │
    │   (MCP 客户端)   │
    └────────┬─────────┘
             │
             │ 标准 MCP 协议
             │
        ┌────┴────┬────────┬────────┐
        │         │        │        │
        ▼         ▼        ▼        ▼
    ┌────────┐ ┌─────┐ ┌──────┐ ┌─────┐
    │ GitHub │ │Slack│ │ Maps │ │ ... │
    │ 服务器 │ │ MCP │ │ MCP  │ │     │
    └────────┘ └─────┘ └──────┘ └─────┘

如何在 ADK 中使用 MCP：

1. 安装 MCP 服务器（例如，通过 npx）
2. 使用连接参数创建 McpToolset
3. 将工具集添加到你的智能体
4. 智能体现在可以使用 MCP 工具了！

示例（需要 Node.js）：
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
        model=AdkLlmWrapper(),
        tools=[mcp_server],  # 将 MCP 工具添加到智能体
    )

可用的 MCP 服务器：
- Kaggle：数据集和笔记本操作
- GitHub：仓库和 PR/issue 管理
- Google Maps：位置和路线
- Slack：团队沟通
- 更多请访问：modelcontextprotocol.io/examples

""")
    print("✅ 已解释 MCP 概念\n")


# ============================================================================
# 示例 2：长时间运行的操作（人工参与）
# ============================================================================

# 配置
LARGE_ORDER_THRESHOLD = 5


def place_shipping_order(
    num_containers: int, destination: str, tool_context: ToolContext
) -> dict:
    """下货运订单。如果订购超过 5 个集装箱，需要审批。

    这演示了一个可以暂停以等待人工审批的长时间运行操作。

    Args:
        num_containers: 要运输的集装箱数量
        destination: 运输目的地
        tool_context: ADK 自动提供此参数

    Returns:
        包含订单状态的字典
    """

    # 场景 1：小订单（≤5 个集装箱）自动批准
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }

    # 场景 2：首次调用 - 大订单需要审批 - 在此处暂停
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination},
        )
        return {
            "status": "pending",
            "message": f"Order for {num_containers} containers requires approval",
        }

    # 场景 3：恢复调用 - 处理审批响应 - 在此处恢复
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} containers to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}",
        }


def create_shipping_system():
    """创建一个带有审批工作流的可恢复货运智能体。"""
    print("\n--- 正在创建长时间运行操作系统 ---")

    # 创建带有可暂停工具的货运智能体
    shipping_agent = LlmAgent(
        name="shipping_agent",
        model=AdkLlmWrapper(),
        instruction="""You are a shipping coordinator assistant.

        When users request to ship containers:
        1. Use the place_shipping_order tool
        2. If status is 'pending', inform user that approval is required
        3. After receiving the final result, provide a clear summary including:
           - Order status (approved/rejected)
           - Order ID (if available)
           - Number of containers and destination
        4. Keep responses concise but informative
        """,
        tools=[FunctionTool(func=place_shipping_order)],
    )

    # 包装在可恢复应用中 - 这是长时间运行操作的关键！
    shipping_app = App(
        name="shipping_coordinator",
        root_agent=shipping_agent,
        resumability_config=ResumabilityConfig(is_resumable=True),
    )

    print("✅ 已创建可恢复货运系统")
    print("🔧 功能：")
    print("  • 自动批准小订单（≤5 个集装箱）")
    print("  • 大订单暂停等待审批（>5 个集装箱）")
    print("  • 在暂停/恢复期间保持状态")

    return shipping_app


# ============================================================================
# 长时间运行操作的辅助函数
# ============================================================================

def check_for_approval(events):
    """检查事件是否包含审批请求。

    Returns:
        包含审批详细信息的字典或 None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None


def print_agent_response(events):
    """从事件中打印智能体的文本响应。"""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent > {part.text}")


def create_approval_response(approval_info, approved):
    """创建审批响应消息。

    Args:
        approval_info: 包含 approval_id 和 invocation_id 的字典
        approved: 指示审批决策的布尔值

    Returns:
        包含审批响应的 Content 对象
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )


# ============================================================================
# 长时间运行操作的工作流函数
# ============================================================================

async def run_shipping_workflow(
    shipping_runner, session_service, query: str, auto_approve: bool = True
):
    """运行带有审批处理的货运工作流。

    这演示了完整的暂停/恢复工作流：
    1. 发送初始请求
    2. 检测智能体是否暂停等待审批
    3. 使用人工决策恢复

    Args:
        shipping_runner: Runner 实例
        session_service: 用于状态管理的会话服务
        query: 用户的货运请求
        auto_approve: 是否自动批准（模拟人工决策）
    """

    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    # 生成唯一的会话 ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # 创建会话
    await session_service.create_session(
        app_name="shipping_coordinator", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # 步骤 1：向智能体发送初始请求
    async for event in shipping_runner.run_async(
        user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # 步骤 2：检查智能体是否暂停等待审批
    approval_info = check_for_approval(events)

    # 步骤 3：处理审批工作流
    if approval_info:
        print(f"⏸️  暂停等待审批...")
        print(f"🤔 人工决策：{'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # 使用审批决策恢复
        async for event in shipping_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(approval_info, auto_approve),
            invocation_id=approval_info["invocation_id"],  # 关键：相同的 ID 以恢复
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent > {part.text}")
    else:
        # 无需审批 - 订单立即完成
        print_agent_response(events)

    print(f"{'='*60}\n")


# ============================================================================
# 主执行
# ============================================================================

async def test_mcp_concept():
    """演示 MCP 概念（不需要实际的 MCP 服务器）。"""
    demonstrate_mcp_concept()


async def test_long_running_operations():
    """演示带有审批工作流的长时间运行操作。"""
    print("\n" + "="*80)
    print("  示例 2：长时间运行的操作（审批工作流）")
    print("="*80)

    # 创建系统
    shipping_app = create_shipping_system()
    session_service = InMemorySessionService()
    shipping_runner = Runner(
        app=shipping_app,
        session_service=session_service,
    )

    print("\n📋 测试三个场景：\n")

    # 场景 1：小订单 - 自动批准
    print("1️⃣ 小订单（3 个集装箱）- 自动批准：")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 3 containers to Singapore"
    )

    # 场景 2：大订单 - 批准
    print("2️⃣ 大订单（10 个集装箱）- 需要审批 - 批准：")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 10 containers to Rotterdam",
        auto_approve=True
    )

    # 场景 3：大订单 - 拒绝
    print("3️⃣ 大订单（8 个集装箱）- 需要审批 - 拒绝：")
    await run_shipping_workflow(
        shipping_runner, session_service,
        "Ship 8 containers to Los Angeles",
        auto_approve=False
    )

    print("✅ 所有的长时间运行操作场景已完成！")


async def main():
    """演示高级智能体工具模式的主函数。"""
    print("\n" + "="*80)
    print("  Day 2b: 智能体工具最佳实践")
    print("="*80)

    # 设置
    setup_api_key()

    print("\n📚 高级模式：")
    print("1. MCP 集成 - 连接到外部服务")
    print("2. 长时间运行的操作 - 人工参与审批")
    print("3. 可恢复工作流 - 使用状态管理暂停和恢复")

    # 示例 1：MCP 概念（仅解释）
    await test_mcp_concept()

    # 示例 2：长时间运行的操作
    await test_long_running_operations()

    print("\n" + "="*80)
    print("  ✅ 所有示例已完成！")
    print("="*80)

    print("\n📖 关键要点：")
    print("- MCP：连接到外部服务而无需自定义集成")
    print("- LRO：暂停工作流以进行人工审批或长时间运行的任务")
    print("- 可恢复性：在对话中断期间保持状态")
    print("- 工具上下文：访问审批状态并请求确认")

    print("\n🔑 何时使用每种模式：")
    print("┌───────────────────────┬──────────────────────────────────────────┐")
    print("│ 模式                  │ 用例                                     │")
    print("├───────────────────────┼──────────────────────────────────────────┤")
    print("│ MCP 集成              │ 连接到外部、标准化的                     │")
    print("│                       │ 服务（GitHub、数据库等）                │")
    print("├───────────────────────┼──────────────────────────────────────────┤")
    print("│ 长时间运行的操作      │ 人工审批、合规检查、                     │")
    print("│                       │ 或跨越时间的操作                         │")
    print("└───────────────────────┴──────────────────────────────────────────┘")

    print("\n🎯 下一步：Day 3 将涵盖状态和内存管理！")


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