"""
第3天a：内存管理 - 第1部分 - 会话

本笔记本涵盖：
- 什么是会话以及如何在您的智能体中使用它们
- 如何使用会话和事件构建有状态的智能体
- 如何在数据库中持久化会话
- 上下文管理实践，如上下文压缩
- 共享会话状态的最佳实践

版权所有 2025 Google LLC。
根据 Apache License 2.0 许可
"""

import os
from typing import Any, Dict

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# ============================================================================
# 设置和配置
# ============================================================================

# 从 .env 文件加载环境变量
from dotenv import load_dotenv

load_dotenv()

# 验证 API 密钥已设置
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ 错误：在环境变量中未找到 GOOGLE_API_KEY")
    print("   请确保您有一个设置了 GOOGLE_API_KEY 的 .env 文件")
    exit(1)

print("✅ ADK 组件导入成功。")
print("✅ API 密钥已从 .env 文件加载")

# ============================================================================
# 配置
# ============================================================================

APP_NAME = "default"
USER_ID = "default"
SESSION = "default"
MODEL_NAME = "gemini-2.5-flash-lite"

# 配置重试选项
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# 辅助函数
# ============================================================================


async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    """
    管理完整对话会话的辅助函数，处理会话
    创建/检索、查询处理和响应流式传输。
    """
    print(f"\n ### 会话：{session_name}")

    # 从 Runner 获取应用名称
    app_name = runner_instance.app_name

    # 尝试创建新会话或检索现有会话
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # 如果提供了查询，则处理
    if user_queries:
        # 将单个查询转换为列表以进行统一处理
        if type(user_queries) == str:
            user_queries = [user_queries]

        # 按顺序处理列表中的每个查询
        for query in user_queries:
            print(f"\n用户 > {query}")

            # 将查询字符串转换为 ADK Content 格式
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # 异步流式传输智能体的响应
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # 检查事件是否包含有效内容
                if event.content and event.content.parts:
                    # 在打印之前过滤掉空或 "None" 的响应
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("没有查询！")


print("✅ 辅助函数已定义。")

# ============================================================================
# 第2节：实现我们的第一个有状态智能体
# ============================================================================


def section_2_stateful_agent():
    """使用 InMemorySessionService 实现有状态智能体"""
    global session_service, runner

    # 步骤 1：创建 LLM 智能体
    root_agent = Agent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="一个文本聊天机器人",
    )

    # 步骤 2：设置会话管理
    session_service = InMemorySessionService()

    # 步骤 3：创建 Runner
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    print("✅ 有状态智能体已初始化！")
    print(f"   - 应用程序：{APP_NAME}")
    print(f"   - 用户：{USER_ID}")
    print(f"   - 使用：{session_service.__class__.__name__}")


# ============================================================================
# 第3节：使用 DatabaseSessionService 的持久化会话
# ============================================================================


def section_3_persistent_sessions():
    """使用 DatabaseSessionService 实现持久化会话"""
    global session_service, runner

    # 步骤 1：创建相同的智能体（这次使用 LlmAgent）
    chatbot_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="一个具有持久化内存的文本聊天机器人",
    )

    # 步骤 2：切换到 DatabaseSessionService
    db_url = "sqlite:///my_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)

    # 步骤 3：使用持久化存储创建新的 runner
    runner = Runner(
        agent=chatbot_agent, app_name=APP_NAME, session_service=session_service
    )

    print("✅ 已升级到持久化会话！")
    print(f"   - 数据库：my_agent_data.db")
    print(f"   - 会话将在重启后保留！")


def inspect_database():
    """检查 SQLite 数据库以查看存储的事件"""
    import sqlite3

    with sqlite3.connect("my_agent_data.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)


# ============================================================================
# 第4节：上下文压缩
# ============================================================================


def section_4_context_compaction():
    """实现上下文压缩以减少上下文大小"""
    global session_service, research_runner_compacting

    chatbot_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="一个具有持久化内存的文本聊天机器人",
    )

    # 重新定义我们的应用程序，启用事件压缩
    research_app_compacting = App(
        name="research_app_compacting",
        root_agent=chatbot_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # 每 3 次调用触发压缩
            overlap_size=1,  # 保留 1 个上一轮次以保持上下文
        ),
    )

    db_url = "sqlite:///my_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)

    # 为我们升级的应用程序创建新的 runner
    research_runner_compacting = Runner(
        app=research_app_compacting, session_service=session_service
    )

    print("✅ 研究应用程序已升级事件压缩！")


async def verify_compaction(session_id: str):
    """通过检查摘要事件来验证是否发生了压缩"""
    final_session = await session_service.get_session(
        app_name="research_app_compacting", user_id=USER_ID, session_id=session_id
    )

    print("--- 搜索压缩摘要事件 ---")
    found_summary = False
    for event in final_session.events:
        if event.actions and event.actions.compaction:
            print("\n✅ 成功！找到压缩事件：")
            print(f"  作者：{event.author}")
            print(f"\n 压缩信息：{event}")
            found_summary = True
            break

    if not found_summary:
        print(
            "\n❌ 未找到压缩事件。尝试增加演示中的轮次数。"
        )


# ============================================================================
# 第5节：使用会话状态
# ============================================================================

# 定义状态键的范围级别
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")


def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    在会话状态中记录和保存用户名和国家的工具。

    参数：
        user_name：要存储在会话状态中的用户名
        country：用户所在国家的名称
    """
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country
    return {"status": "success"}


def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    从会话状态中检索用户名和国家的工具。
    """
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")
    return {"status": "success", "user_name": user_name, "country": country}


def section_5_session_state():
    """创建具有会话状态工具的智能体"""
    global session_service, runner

    # 创建具有会话状态工具的智能体
    root_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="""一个文本聊天机器人。
        用于管理用户上下文的工具：
        * 当提供用户名和国家时，使用 `save_userinfo` 工具记录。
        * 当需要获取用户名和国家时，使用 `retrieve_userinfo` 工具。
        """,
        tools=[save_userinfo, retrieve_userinfo],
    )

    # 设置会话服务和 runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, session_service=session_service, app_name="default"
    )

    print("✅ 具有会话状态工具的智能体已初始化！")


async def inspect_session_state(session_id: str):
    """检查会话状态以查看存储的数据"""
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )

    print("会话状态内容：")
    print(session.state)
    print("\n🔍 注意 'user:name' 和 'user:country' 键正在存储我们的数据！")


# ============================================================================
# 清理
# ============================================================================


def cleanup():
    """清理数据库文件"""
    if os.path.exists("my_agent_data.db"):
        os.remove("my_agent_data.db")
    print("✅ 已清理旧的数据库文件")


# ============================================================================
# 示例用法
# ============================================================================


async def main():
    """不同部分的示例用法"""

    # 第2节：使用 InMemorySessionService 的有状态智能体
    print("\n" + "=" * 80)
    print("第2节：使用 InMemorySessionService 的有状态智能体")
    print("=" * 80)
    section_2_stateful_agent()

    await run_session(
        runner,
        [
            "嗨，我是 Sam！美国的首都是什么？",
            "你好！我的名字是什么？",
        ],
        "stateful-agentic-session",
    )

    # 第3节：持久化会话
    print("\n" + "=" * 80)
    print("第3节：使用 DatabaseSessionService 的持久化会话")
    print("=" * 80)
    section_3_persistent_sessions()

    await run_session(
        runner,
        [
            "嗨，我是 Sam！美国的首都是什么？",
            "你好！我的名字是什么？",
        ],
        "test-db-session-01",
    )

    # 检查数据库
    print("\n--- 数据库内容 ---")
    inspect_database()

    # 第4节：上下文压缩
    print("\n" + "=" * 80)
    print("第4节：上下文压缩")
    print("=" * 80)
    section_4_context_compaction()

    # 运行多个轮次以触发压缩
    await run_session(
        research_runner_compacting,
        "关于医疗保健中的 AI 有什么最新消息？",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "药物发现有什么新的发展吗？",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "告诉我更多关于你发现的第二个发展。",
        "compaction_demo",
    )
    await run_session(
        research_runner_compacting,
        "参与其中的主要公司是谁？",
        "compaction_demo",
    )

    # 验证压缩
    await verify_compaction("compaction_demo")

    # 第5节：会话状态
    print("\n" + "=" * 80)
    print("第5节：使用会话状态")
    print("=" * 80)
    section_5_session_state()

    await run_session(
        runner,
        [
            "嗨，你今天过得怎么样？我的名字是什么？",
            "我的名字是 Sam。我来自波兰。",
            "我的名字是什么？我来自哪个国家？",
        ],
        "state-demo-session",
    )

    # 检查会话状态
    await inspect_session_state("state-demo-session")

    # 测试状态隔离
    await run_session(
        runner,
        ["嗨，你今天过得怎么样？我的名字是什么？"],
        "new-isolated-session",
    )

    # 清理
    cleanup()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
