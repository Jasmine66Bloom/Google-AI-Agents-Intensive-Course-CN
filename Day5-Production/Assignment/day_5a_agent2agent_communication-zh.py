"""
第5天a部分：Agent2Agent (A2A) 通信

本脚本涵盖：
- 理解 A2A 协议及何时使用它
- 常见的 A2A 架构模式（跨框架、跨语言、跨组织）
- 使用 to_a2a() 通过 A2A 暴露 ADK 代理
- 使用 RemoteA2aAgent 消费远程代理
- 构建产品目录集成系统

版权所有 2025 Google LLC。
根据 Apache 许可证版本 2.0 许可
"""

import os
import json
import time
import subprocess
import requests
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ============================================================================
# 设置和配置
# ============================================================================

# 从 .env 文件加载环境变量
load_dotenv()

# 验证 API 密钥已设置
if not os.getenv("DOUBAO_API_KEY"):
    print("❌ 错误：在环境变量中未找到 DOUBAO_API_KEY")
    print("   请确保您有一个设置了 DOUBAO_API_KEY 的 .env 文件")
    exit(1)

print("✅ ADK 组件导入成功。")
print("✅ API 密钥已从 .env 文件加载")

# ============================================================================
# 第1部分：产品目录代理（将通过 A2A 暴露）
# ============================================================================


def get_product_info(product_name: str) -> str:
    """获取给定产品的产品信息。

    参数：
        product_name：产品名称（例如，"iPhone 15 Pro"、"MacBook Pro"）

    返回：
        产品信息作为字符串
    """
    # 模拟产品目录 - 在生产环境中，这将查询真实的数据库
    product_catalog = {
        "iphone 15 pro": "iPhone 15 Pro, $999, 库存低 (8 台), 128GB, 钛金属饰面",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, 有库存 (31 台), 256GB, 幻影黑",
        "dell xps 15": 'Dell XPS 15, $1,299, 有库存 (45 台), 15.6" 显示屏, 16GB 内存, 512GB SSD',
        "macbook pro 14": 'MacBook Pro 14", $1,999, 有库存 (22 台), M3 Pro 芯片, 18GB 内存, 512GB SSD',
        "sony wh-1000xm5": "Sony WH-1000XM5 耳机, $399, 有库存 (67 台), 降噪, 30 小时电池",
        "ipad air": 'iPad Air, $599, 有库存 (28 台), 10.9" 显示屏, 64GB',
        "lg ultrawide 34": 'LG UltraWide 34" 显示器, $499, 无库存, 预计：下周',
    }

    product_lower = product_name.lower().strip()

    if product_lower in product_catalog:
        return f"产品: {product_catalog[product_lower]}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"抱歉，我没有 {product_name} 的信息。可用产品: {available}"


def create_product_catalog_agent():
    """创建产品目录代理"""

    product_catalog_agent = LlmAgent(
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        name="product_catalog_agent",
        description="外部供应商的产品目录代理，提供产品信息和可用性。",
        instruction="""
        您是来自外部供应商的产品目录专家。
        当被问及产品时，使用 get_product_info 工具从目录中获取数据。
        提供清晰、准确的产品信息，包括价格、可用性和规格。
        如果被问及多个产品，请逐个查找。
        保持专业和乐于助人。
        """,
        tools=[get_product_info],
    )

    print("✅ 产品目录代理创建成功！")
    print("   模型：gemini-2.5-flash-lite")
    print("   工具：get_product_info()")
    print("   准备通过 A2A 暴露...")

    return product_catalog_agent


# ============================================================================
# 第2部分：通过 A2A 暴露代理
# ============================================================================


def create_product_catalog_server_file():
    """为 A2A 服务器创建独立的 Python 文件"""

    server_code = f'''
import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

def get_product_info(product_name: str) -> str:
    """获取给定产品的产品信息。"""
    product_catalog = {{
        "iphone 15 pro": "iPhone 15 Pro, $999, 库存低 (8 台), 128GB, 钛金属饰面",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, 有库存 (31 台), 256GB, 幻影黑",
        "dell xps 15": "Dell XPS 15, $1,299, 有库存 (45 台), 15.6\\" 显示屏, 16GB 内存, 512GB SSD",
        "macbook pro 14": "MacBook Pro 14\\", $1,999, 有库存 (22 台), M3 Pro 芯片, 18GB 内存, 512GB SSD",
        "sony wh-1000xm5": "Sony WH-1000XM5 耳机, $399, 有库存 (67 台), 降噪, 30 小时电池",
        "ipad air": "iPad Air, $599, 有库存 (28 台), 10.9\\" 显示屏, 64GB",
        "lg ultrawide 34": "LG UltraWide 34\\" 显示器, $499, 无库存, 预计：下周",
    }}

    product_lower = product_name.lower().strip()

    if product_lower in product_catalog:
        return f"产品: {{product_catalog[product_lower]}}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"抱歉，我没有 {{product_name}} 的信息。可用产品: {{available}}"

product_catalog_agent = LlmAgent(
    model=LiteLlm(
        model="volcengine/doubao-1-5-lite-32k-250115",
        api_key=os.environ.get("DOUBAO_API_KEY")
    ),
    name="product_catalog_agent",
    description="外部供应商的产品目录代理，提供产品信息和可用性。",
    instruction="""
    您是来自外部供应商的产品目录专家。
    当被问及产品时，使用 get_product_info 工具从目录中获取数据。
    提供清晰、准确的产品信息，包括价格、可用性和规格。
    如果被问及多个产品，请逐个查找。
    保持专业和乐于助人。
    """,
    tools=[get_product_info]
)

# 创建 A2A 应用
app = to_a2a(product_catalog_agent, port=8001)
'''

    # 写入临时文件
    server_file = "/tmp/product_catalog_server.py"
    with open(server_file, "w") as f:
        f.write(server_code)

    print(f"📝 产品目录服务器代码已保存到 {server_file}")
    return server_file


def start_product_catalog_server():
    """在后台启动产品目录代理服务器"""

    # 创建服务器文件
    server_file = create_product_catalog_server_file()

    # 在后台启动 uvicorn 服务器
    print("\n🚀 启动产品目录代理服务器...")
    print("   等待服务器准备就绪...")

    server_process = subprocess.Popen(
        [
            "uvicorn",
            "product_catalog_server:app",
            "--host",
            "localhost",
            "--port",
            "8001",
        ],
        cwd="/tmp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ},
    )

    # 等待服务器启动
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                "http://localhost:8001/.well-known/agent-card.json", timeout=1
            )
            if response.status_code == 200:
                print(f"\n✅ 产品目录代理服务器正在运行！")
                print(f"   服务器 URL：http://localhost:8001")
                print(
                    f"   代理卡片：http://localhost:8001/.well-known/agent-card.json"
                )
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\n⚠️  服务器可能尚未准备就绪。如果需要，请手动检查。")

    return server_process


def view_agent_card():
    """获取并显示代理卡片"""

    try:
        response = requests.get(
            "http://localhost:8001/.well-known/agent-card.json", timeout=5
        )

        if response.status_code == 200:
            agent_card = response.json()
            print("\n📋 产品目录代理卡片：")
            print(json.dumps(agent_card, indent=2))

            print("\n✨ 关键信息：")
            print(f"   名称：{agent_card.get('name')}")
            print(f"   描述：{agent_card.get('description')}")
            print(f"   URL：{agent_card.get('url')}")
            print(
                f"   技能：暴露了 {len(agent_card.get('skills', []))} 个能力"
            )
        else:
            print(f"❌ 获取代理卡片失败：{response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 获取代理卡片时出错：{e}")


# ============================================================================
# 第4部分：创建客户支持代理（消费者）
# ============================================================================


def create_customer_support_agent():
    """创建消费产品目录代理的客户支持代理"""

    # 创建连接到产品目录代理的 RemoteA2aAgent
    remote_product_catalog_agent = RemoteA2aAgent(
        name="product_catalog_agent",
        description="来自外部供应商的远程产品目录代理，提供产品信息。",
        agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
    )

    print("\n✅ 远程产品目录代理代理创建成功！")
    print(f"   连接到：http://localhost:8001")
    print(f"   代理卡片：http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}")
    print("   客户支持代理现在可以像本地子代理一样使用它！")

    # 创建客户支持代理
    customer_support_agent = LlmAgent(
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        name="customer_support_agent",
        description="帮助客户处理产品查询和信息的客户支持助手。",
        instruction="""
        您是一个友好且专业的客户支持代理。

        当客户询问产品时：
        1. 使用 product_catalog_agent 子代理查找产品信息
        2. 提供关于价格、可用性和规格的清晰答案
        3. 如果产品缺货，提及预计可用时间
        4. 保持乐于助人和专业！

        在回答客户问题之前，始终从 product_catalog_agent 获取产品信息。
        """,
        sub_agents=[remote_product_catalog_agent],
    )

    print("\n✅ 客户支持代理创建成功！")
    print("   模型：gemini-2.5-flash-lite")
    print("   子代理：1 个（通过 A2A 的远程产品目录代理）")
    print("   准备帮助客户！")

    return customer_support_agent


# ============================================================================
# 第5部分：测试 A2A 通信
# ============================================================================


async def test_a2a_communication(customer_support_agent, user_query: str):
    """测试 A2A 通信"""

    # 设置会话管理
    session_service = InMemorySessionService()

    app_name = "support_app"
    user_id = "demo_user"
    session_id = f"demo_session_{uuid.uuid4().hex[:8]}"

    # 创建会话
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    # 创建运行器
    runner = Runner(
        agent=customer_support_agent,
        app_name=app_name,
        session_service=session_service,
    )

    # 创建用户消息
    test_content = types.Content(parts=[types.Part(text=user_query)])

    # 显示查询
    print(f"\n👤 客户：{user_query}")
    print(f"\n🎧 支持代理响应：")
    print("-" * 60)

    # 运行代理
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=test_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)

    print("-" * 60)


# ============================================================================
# 主函数
# ============================================================================


async def main():
    """运行 A2A 通信演示"""

    print("\n" + "=" * 80)
    print("第5天A部分：AGENT2AGENT (A2A) 通信")
    print("=" * 80)

    print("\n📚 您将学到：")
    print("• 理解 A2A 协议")
    print("• 使用 to_a2a() 通过 A2A 暴露代理")
    print("• 使用 RemoteA2aAgent 消费远程代理")
    print("• 构建跨组织的代理系统")

    # 第1部分：创建产品目录代理
    print("\n" + "=" * 80)
    print("第1部分：创建产品目录代理（待暴露）")
    print("=" * 80)
    product_catalog_agent = create_product_catalog_agent()

    # 第2和3部分：通过 A2A 暴露并启动服务器
    print("\n" + "=" * 80)
    print("第2和3部分：通过 A2A 暴露并启动服务器")
    print("=" * 80)
    server_process = start_product_catalog_server()

    # 查看代理卡片
    view_agent_card()

    # 第4部分：创建客户支持代理
    print("\n" + "=" * 80)
    print("第4部分：创建客户支持代理（消费者）")
    print("=" * 80)
    customer_support_agent = create_customer_support_agent()

    # 第5部分：测试 A2A 通信
    print("\n" + "=" * 80)
    print("第5部分：测试 A2A 通信")
    print("=" * 80)
    print("\n🧪 测试 A2A 通信...")

    # 测试 1
    await test_a2a_communication(
        customer_support_agent, "你能告诉我关于 iPhone 15 Pro 的信息吗？有库存吗？"
    )

    # 测试 2
    await test_a2a_communication(
        customer_support_agent,
        "我在找一台笔记本电脑。你能为我比较一下 Dell XPS 15 和 MacBook Pro 14 吗？",
    )

    # 测试 3
    await test_a2a_communication(
        customer_support_agent,
        "你们有 Sony WH-1000XM5 耳机吗？价格是多少？",
    )

    # 清理
    print("\n" + "=" * 80)
    print("清理")
    print("=" * 80)
    print("\n🛑 停止产品目录服务器...")
    server_process.terminate()
    server_process.wait()
    print("✅ 服务器已停止")

    # 总结
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)

    print("\n🎯 关键要点：")
    print("✅ A2A 协议支持跨组织的代理通信")
    print("✅ to_a2a() 使代理可通过自动生成的代理卡片访问")
    print("✅ RemoteA2aAgent 将远程代理作为本地子代理消费")
    print("✅ 代理卡片在 /.well-known/agent-card.json 描述能力")

    print("\n📊 A2A 与本地子代理比较：")
    print("在以下情况使用 A2A：")
    print("   • 代理位于不同的代码库/组织中")
    print("   • 需要跨语言/框架通信")
    print("   • 需要正式的 API 合约")
    print("\n在以下情况使用本地子代理：")
    print("   • 同一代码库/团队内部")
    print("   • 需要低延迟")
    print("   • 相同的语言/框架")

    print("\n📚 了解更多：")
    print("• A2A 协议：https://a2a-protocol.org/")
    print("• 暴露代理：https://google.github.io/adk-docs/a2a/quickstart-exposing/")
    print("• 消费代理：https://google.github.io/adk-docs/a2a/quickstart-consuming/")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())