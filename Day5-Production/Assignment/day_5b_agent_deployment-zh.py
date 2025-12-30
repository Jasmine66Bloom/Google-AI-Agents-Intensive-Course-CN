"""
第5天b部分：将 ADK 代理部署到生产环境

本脚本涵盖：
- 构建生产就绪的 ADK 代理
- 了解部署选项（Agent Engine、Cloud Run、GKE）
- 创建部署配置文件
- 使用 ADK CLI 部署到 Vertex AI Agent Engine
- 测试已部署的代理
- 了解用于长期记忆的 Memory Bank
- 成本管理和清理

注意：本脚本演示概念并提供代码示例。
实际部署需要已启用计费的 Google Cloud Platform 账户。

版权所有 2025 Google LLC。
根据 Apache 许可证版本 2.0 许可
"""

import os
import json
from dotenv import load_dotenv

# ============================================================================
# 设置和配置
# ============================================================================

# 从 .env 文件加载环境变量
load_dotenv()

print("✅ 导入成功完成")
print("✅ 环境变量已从 .env 文件加载")

# ============================================================================
# 代理代码模板
# ============================================================================

AGENT_CODE_TEMPLATE = '''"""
生产天气助手代理

此代理使用模拟数据库为城市提供天气信息。
在生产环境中，这将与真实的天气 API 集成。
"""

from google.adk.agents import Agent
import vertexai
import os

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

def get_weather(city: str) -> dict:
    """
    返回给定城市的天气信息。

    这是一个代理在用户询问天气时可以调用的工具。
    在生产环境中，这将调用真实的天气 API（例如，OpenWeatherMap）。
    对于此演示，我们使用模拟数据。

    参数：
        city：城市名称（例如，"Tokyo"、"New York"）

    返回：
        dict：包含状态和天气报告或错误消息的字典
    """
    # 模拟天气数据库，包含结构化响应
    weather_data = {
        "san francisco": {"status": "success", "report": "旧金山的天气晴朗，温度为 72°F (22°C)。"},
        "new york": {"status": "success", "report": "纽约的天气多云，温度为 65°F (18°C)。"},
        "london": {"status": "success", "report": "伦敦的天气下雨，温度为 58°F (14°C)。"},
        "tokyo": {"status": "success", "report": "东京的天气晴朗，温度为 70°F (21°C)。"},
        "paris": {"status": "success", "report": "巴黎的天气部分多云，温度为 68°F (20°C)。"}
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available_cities = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"'{city}' 的天气信息不可用。尝试：{available_cities}"
        }

root_agent = Agent(
    name="weather_assistant",
    model="gemini-2.5-flash-lite",  # 快速、经济实惠的 Gemini 模型
    description="一个有用的天气助手，为城市提供天气信息。",
    instruction="""
    您是一个友好的天气助手。当用户询问天气时：

    1. 从他们的问题中识别城市名称
    2. 使用 get_weather 工具获取当前天气信息
    3. 以友好、对话的语气回应
    4. 如果城市不可用，建议一个可用的城市

    在您的回应中保持乐于助人和简洁。
    """,
    tools=[get_weather]
)
'''

REQUIREMENTS_TXT = """google-adk
opentelemetry-instrumentation-google-genai"""

ENV_FILE = '''# https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#global-endpoint
GOOGLE_CLOUD_LOCATION="global"

# 设置为 1 以使用 Vertex AI，或设置为 0 以使用 Google AI Studio
GOOGLE_GENAI_USE_VERTEXAI=1'''

AGENT_ENGINE_CONFIG = '''{
    "min_instances": 0,
    "max_instances": 1,
    "resource_limits": {"cpu": "1", "memory": "1Gi"}
}'''

# ============================================================================
# 辅助函数
# ============================================================================


def create_agent_directory():
    """创建代理目录结构"""
    agent_dir = "sample_agent"

    print(f"\n📁 创建代理目录：{agent_dir}/")

    # 创建目录
    os.makedirs(agent_dir, exist_ok=True)

    # 创建 agent.py
    with open(f"{agent_dir}/agent.py", "w") as f:
        f.write(AGENT_CODE_TEMPLATE)
    print(f"   ✅ 已创建 {agent_dir}/agent.py")

    # 创建 requirements.txt
    with open(f"{agent_dir}/requirements.txt", "w") as f:
        f.write(REQUIREMENTS_TXT)
    print(f"   ✅ 已创建 {agent_dir}/requirements.txt")

    # 创建 .env
    with open(f"{agent_dir}/.env", "w") as f:
        f.write(ENV_FILE)
    print(f"   ✅ 已创建 {agent_dir}/.env")

    # 创建 .agent_engine_config.json
    with open(f"{agent_dir}/.agent_engine_config.json", "w") as f:
        f.write(AGENT_ENGINE_CONFIG)
    print(f"   ✅ 已创建 {agent_dir}/.agent_engine_config.json")

    print(f"\n✅ 代理目录创建成功！")
    print(f"   目录结构：")
    print(f"   {agent_dir}/")
    print(f"   ├── agent.py                  # 代理逻辑")
    print(f"   ├── requirements.txt          # 库")
    print(f"   ├── .env                      # 配置")
    print(f"   └── .agent_engine_config.json # 硬件规格")

    return agent_dir


def explain_deployment_options():
    """解释不同的部署选项"""
    print("\n" + "=" * 80)
    print("部署选项")
    print("=" * 80)

    print("\n🔷 Vertex AI Agent Engine（本教程）")
    print("   • AI 代理的完全托管服务")
    print("   • 具有内置会话管理的自动扩展")
    print("   • 使用 adk deploy 命令轻松部署")
    print("   • 免费套餐：每个账户 10 个代理")
    print("   📚 指南：https://google.github.io/adk-docs/deploy/agent-engine/")

    print("\n🔷 Cloud Run")
    print("   • 无服务器，最容易上手")
    print("   • 非常适合演示和小到中型工作负载")
    print("   • 不使用时自动扩展到零")
    print("   📚 指南：https://google.github.io/adk-docs/deploy/cloud-run/")

    print("\n🔷 Google Kubernetes Engine (GKE)")
    print("   • 对容器化部署的完全控制")
    print("   • 最适合复杂的多代理系统")
    print("   • 高级编排能力")
    print("   📚 指南：https://google.github.io/adk-docs/deploy/gke/")


def explain_deployment_steps():
    """解释部署过程"""
    print("\n" + "=" * 80)
    print("部署过程")
    print("=" * 80)

    print("\n📋 先决条件：")
    print("   1. Google Cloud Platform 账户")
    print("   2. 已启用计费（免费套餐可用）")
    print("   3. 启用所需的 API：")
    print("      • Vertex AI API")
    print("      • Cloud Storage API")
    print("      • Cloud Logging API")
    print("      • Cloud Monitoring API")
    print("      • Cloud Trace API")
    print("      • Telemetry API")

    print("\n🚀 部署步骤：")
    print("\n   步骤 1：设置您的 PROJECT_ID")
    print("   ```bash")
    print("   export GOOGLE_CLOUD_PROJECT='your-project-id'")
    print("   ```")

    print("\n   步骤 2：使用 Google Cloud 进行身份验证")
    print("   ```bash")
    print("   gcloud auth login")
    print("   gcloud config set project your-project-id")
    print("   ```")

    print("\n   步骤 3：部署代理")
    print("   ```bash")
    print("   adk deploy agent_engine \\")
    print("     --project=$GOOGLE_CLOUD_PROJECT \\")
    print("     --region=us-east4 \\")
    print("     sample_agent \\")
    print("     --agent_engine_config_file=sample_agent/.agent_engine_config.json")
    print("   ```")

    print("\n   步骤 4：等待部署（2-5 分钟）")
    print("   您将收到一个资源名称，如：")
    print("   projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID")

    print("\n   步骤 5：测试已部署的代理")
    print("   使用 Python SDK 或 REST API 发送查询")


def explain_testing():
    """解释如何测试已部署的代理"""
    print("\n" + "=" * 80)
    print("测试已部署的代理")
    print("=" * 80)

    print("\n📝 Python SDK 示例：")
    print("""
import vertexai
from vertexai import agent_engines

# 初始化 Vertex AI
vertexai.init(project='your-project-id', location='us-east4')

# 获取已部署的代理
agents_list = list(agent_engines.list())
remote_agent = agents_list[0]  # 获取最新的

# 测试代理
async for item in remote_agent.async_stream_query(
    message="东京的天气怎么样？",
    user_id="user_42",
):
    print(item)
""")

    print("\n🔍 您将看到：")
    print("   1. 函数调用事件 - 代理调用 get_weather 工具")
    print("   2. 函数响应事件 - 返回天气数据")
    print("   3. 最终响应事件 - 代理的自然语言回答")


def explain_memory_bank():
    """解释 Vertex AI Memory Bank"""
    print("\n" + "=" * 80)
    print("VERTEX AI MEMORY BANK")
    print("=" * 80)

    print("\n🧠 什么是 Memory Bank？")
    print("   Memory Bank 为您的代理提供跨会话的长期记忆。")

    print("\n📊 会话记忆与 Memory Bank 的比较：")
    print("   ┌─────────────────┬────────────────────┐")
    print("   │ 会话记忆        │ Memory Bank        │")
    print("   ├─────────────────┼────────────────────┤")
    print("   │ 单次对话        │ 所有对话           │")
    print("   │ 结束时遗忘      │ 永久记住           │")
    print("   │ '我刚才说了什么'│ '我最喜欢的城市'   │")
    print("   └─────────────────┴────────────────────┘")

    print("\n💡 工作原理：")
    print("   1. 对话期间：代理使用记忆工具搜索过去的事实")
    print("   2. 对话结束后：系统提取关键信息")
    print("   3. 下次会话：代理自动回忆信息")

    print("\n🔧 启用 Memory Bank：")
    print("   1. 向代理添加记忆工具（PreloadMemoryTool）")
    print("   2. 添加回调以保存对话")
    print("   3. 重新部署代理")

    print("\n📚 了解更多：")
    print("   • ADK 记忆：https://google.github.io/adk-docs/sessions/memory/")
    print("   • 记忆工具：https://google.github.io/adk-docs/tools/built-in-tools/")


def explain_cleanup():
    """解释清理过程"""
    print("\n" + "=" * 80)
    print("清理和成本管理")
    print("=" * 80)

    print("\n⚠️  重要：测试完成后务必删除资源！")

    print("\n🧹 删除已部署的代理：")
    print("   ```python")
    print("   from vertexai import agent_engines")
    print("   ")
    print("   agent_engines.delete(")
    print("       resource_name=remote_agent.resource_name,")
    print("       force=True")
    print("   )")
    print("   ```")

    print("\n💰 成本管理：")
    print("   • 免费套餐：每个账户 10 个代理")
    print("   • 本演示：如果清理，通常保持在免费套餐内")
    print("   • 如果保持运行：可能会产生费用")
    print("   • 最佳实践：测试后立即删除")

    print("\n📊 监控成本：")
    print("   • Google Cloud 控制台：https://console.cloud.google.com/billing")
    print("   • 设置计费警报以避免意外")
    print("   • 定期检查 Agent Engine 控制台")


# ============================================================================
# 主函数
# ============================================================================


def main():
    """运行部署指南"""

    print("\n" + "=" * 80)
    print("第5天B部分：将 ADK 代理部署到生产环境")
    print("=" * 80)

    print("\n📚 您将学到：")
    print("• 构建生产就绪的 ADK 代理")
    print("• 了解部署选项")
    print("• 部署到 Vertex AI Agent Engine")
    print("• 测试已部署的代理")
    print("• 了解 Memory Bank")
    print("• 成本管理和清理")

    # 第1部分：部署选项
    explain_deployment_options()

    # 第2部分：创建代理目录
    print("\n" + "=" * 80)
    print("第2部分：创建生产代理")
    print("=" * 80)
    agent_dir = create_agent_directory()

    # 第3部分：部署过程
    explain_deployment_steps()

    # 第4部分：测试
    explain_testing()

    # 第5部分：Memory Bank
    explain_memory_bank()

    # 第6部分：清理
    explain_cleanup()

    # 总结
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)

    print("\n🎯 关键要点：")
    print("✅ Agent Engine 提供完全托管的代理托管")
    print("✅ 使用 'adk deploy agent_engine' 命令部署")
    print("✅ 使用 Python SDK 或 REST API 测试已部署的代理")
    print("✅ Memory Bank 支持跨会话的长期记忆")
    print("✅ 始终清理资源以管理成本")

    print("\n📁 创建的文件：")
    print(f"   • {agent_dir}/agent.py - 代理逻辑")
    print(f"   • {agent_dir}/requirements.txt - 依赖项")
    print(f"   • {agent_dir}/.env - 配置")
    print(f"   • {agent_dir}/.agent_engine_config.json - 硬件规格")

    print("\n🚀 后续步骤：")
    print("   1. 获取 Google Cloud 账户（可用免费积分）")
    print("   2. 在 GCP 控制台中启用所需的 API")
    print("   3. 使用您的项目 ID 运行 'adk deploy agent_engine'")
    print("   4. 测试已部署的代理")
    print("   5. 完成后清理资源")

    print("\n📚 了解更多：")
    print("   • ADK 部署指南：https://google.github.io/adk-docs/deploy/")
    print("   • Agent Engine 文档：https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview")
    print("   • Cloud Run 部署：https://google.github.io/adk-docs/deploy/cloud-run/")
    print("   • GKE 部署：https://google.github.io/adk-docs/deploy/gke/")

    print("\n🎓 课程完成！")
    print("   恭喜您完成 5 天 AI 代理课程！")
    print("   您现在拥有构建、测试和部署生产代理的技能。")

    print("\n⭐ 分享您的项目：")
    print("   • Kaggle Discord：https://discord.com/invite/kaggle")
    print("   • ADK 文档：https://google.github.io/adk-docs/")


if __name__ == "__main__":
    main()