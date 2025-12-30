"""
第3天b：内存管理 - 第2部分 - 内存

本笔记本涵盖：
- 初始化 MemoryService 并与您的智能体集成
- 将会话数据传输到内存存储
- 搜索和检索记忆
- 自动化内存存储和检索
- 理解记忆整合（概念概述）

什么是内存？
- 会话 = 短期记忆（单个对话）
- 内存 = 长期知识（跨越多个对话）

版权所有 2025 Google LLC。
根据 Apache License 2.0 许可
"""

import os
from typing import Any, Dict

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
from google.genai import types

# ============================================================================
# 设置和配置
# ============================================================================

# 从 .env 文件加载环境变量
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("DOUBAO_API_KEY"):
    print("❌ 错误：在环境变量中未找到 DOUBAO_API_KEY")
    print("   请确保您有一个设置了 DOUBAO_API_KEY 的 .env 文件")
    exit(1)

print("✅ ADK 组件导入成功。")
print("✅ API 密钥已从 .env 文件加载")

# ============================================================================
# 配置
# ============================================================================

APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"
MODEL_NAME = "volcengine/doubao-1-5-lite-32k-250115"

# ============================================================================
# 辅助函数
# ============================================================================


async def run_session(
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default"
):
    """辅助函数，用于在会话中运行查询并显示响应。"""
    print(f"\n### 会话：{session_id}")

    # 创建或检索会话
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # 将单个查询转换为列表
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # 处理每个查询
    for query in user_queries:
        print(f"\n用户 > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # 流式传输智能体响应
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"模型：> {text}")


print("✅ 辅助函数已定义。")

# ============================================================================
# 第3节：初始化 MemoryService
# ============================================================================


def section_3_initialize_memory():
    """初始化内存服务并创建具有内存支持的智能体"""
    global memory_service, session_service, user_agent, runner

    # 步骤 1：初始化内存服务
    memory_service = InMemoryMemoryService()

    # 步骤 2：创建智能体
    user_agent = LlmAgent(
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        name="MemoryDemoAgent",
        instruction="用简单的语言回答用户问题。",
    )

    # 步骤 3：创建会话服务
    session_service = InMemorySessionService()

    # 步骤 4：使用两个服务创建 runner
    runner = Runner(
        agent=user_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ 已创建具有内存支持的智能体和 Runner！")


# ============================================================================
# 第4节：将会话数据摄入到内存中
# ============================================================================


async def section_4_ingest_session():
    """演示如何将会话数据摄入到内存中"""

    # 进行对话
    await run_session(
        runner,
        "我最喜欢的颜色是蓝绿色。你能写一首关于它的俳句吗？",
        "conversation-01",
    )

    # 验证对话已被捕获
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )

    print("\n📝 会话包含：")
    for event in session.events:
        text = (
            event.content.parts[0].text[:60]
            if event.content and event.content.parts
            else "(空)"
        )
        print(f"  {event.content.role}: {text}...")

    # 将会话传输到内存
    await memory_service.add_session_to_memory(session)
    print("\n✅ 会话已添加到内存！")


# ============================================================================
# 第5节：在您的智能体中启用内存检索
# ============================================================================


def section_5_enable_retrieval():
    """创建具有 load_memory 工具的智能体以进行响应式检索"""
    global user_agent, runner

    # 创建具有 load_memory 工具的智能体
    user_agent = LlmAgent(
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        name="MemoryDemoAgent",
        instruction="用简单的语言回答用户问题。如果您需要回忆过去的对话，请使用 load_memory 工具。",
        tools=[load_memory],
    )

    # 使用更新的智能体创建新的 runner
    runner = Runner(
        agent=user_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ 已创建具有 load_memory 工具的智能体。")


async def test_manual_memory_workflow():
    """完整的手动工作流测试：摄入 → 存储 → 检索"""

    # 测试 1：保存生日信息
    await run_session(runner, "我的生日是3月15日。", "birthday-session-01")

    # 手动将会话保存到内存
    birthday_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01"
    )
    await memory_service.add_session_to_memory(birthday_session)
    print("\n✅ 生日会话已保存到内存！")

    # 测试 2：在新会话中检索
    await run_session(runner, "我的生日是什么时候？", "birthday-session-02")


async def manual_memory_search():
    """演示从代码直接进行内存搜索"""

    # 搜索颜色偏好
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="用户最喜欢的颜色是什么？"
    )

    print("\n🔍 搜索结果：")
    print(f"  找到 {len(search_response.memories)} 个相关记忆")
    print()

    for memory in search_response.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{memory.author}]: {text}...")


# ============================================================================
# 第6节：自动化内存存储
# ============================================================================


async def auto_save_to_memory(callback_context):
    """在每个智能体轮次后自动将会话保存到内存。"""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


def section_6_automatic_memory():
    """使用回调创建具有自动内存保存的智能体"""
    global auto_memory_agent, auto_runner

    # 具有自动内存保存的智能体
    auto_memory_agent = LlmAgent(
        model=LiteLlm(
            model=MODEL_NAME,
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        name="AutoMemoryAgent",
        instruction="回答用户问题。",
        tools=[preload_memory],
        after_agent_callback=auto_save_to_memory,
    )

    # 为自动保存智能体创建 runner
    auto_runner = Runner(
        agent=auto_memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ 已创建具有自动内存保存的智能体！")


async def test_automatic_memory():
    """测试自动内存存储和检索"""

    # 测试 1：告诉智能体关于礼物的事情
    await run_session(
        auto_runner,
        "我在侄子1岁生日时送了他一个新玩具！",
        "auto-save-test",
    )

    # 测试 2：在新会话中询问礼物
    await run_session(
        auto_runner,
        "我送了侄子什么礼物？",
        "auto-save-test-2",
    )


# ============================================================================
# 示例用法
# ============================================================================


async def main():
    """不同部分的示例用法"""

    # 第3节：初始化内存
    print("\n" + "=" * 80)
    print("第3节：初始化 MemoryService")
    print("=" * 80)
    section_3_initialize_memory()

    # 第4节：摄入会话数据
    print("\n" + "=" * 80)
    print("第4节：将会话数据摄入到内存中")
    print("=" * 80)
    await section_4_ingest_session()

    # 第5节：启用内存检索
    print("\n" + "=" * 80)
    print("第5节：在您的智能体中启用内存检索")
    print("=" * 80)
    section_5_enable_retrieval()

    # 使用颜色查询进行测试
    await run_session(runner, "我最喜欢的颜色是什么？", "color-test")

    # 完整的手动工作流
    print("\n--- 完整的手动工作流测试 ---")
    await test_manual_memory_workflow()

    # 手动内存搜索
    print("\n--- 手动内存搜索 ---")
    await manual_memory_search()

    # 第6节：自动化内存存储
    print("\n" + "=" * 80)
    print("第6节：自动化内存存储")
    print("=" * 80)
    section_6_automatic_memory()

    # 测试自动内存
    await test_automatic_memory()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
