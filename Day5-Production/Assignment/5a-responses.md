✅ ADK 组件导入成功。
✅ API 密钥已从 .env 文件加载

================================================================================
第5天A部分：AGENT2AGENT (A2A) 通信
================================================================================

📚 您将学到：
• 理解 A2A 协议
• 使用 to_a2a() 通过 A2A 暴露代理
• 使用 RemoteA2aAgent 消费远程代理
• 构建跨组织的代理系统

================================================================================
第1部分：创建产品目录代理（待暴露）
================================================================================
✅ 产品目录代理创建成功！
   模型：gemini-2.5-flash-lite
   工具：get_product_info()
   准备通过 A2A 暴露...

================================================================================
第2和3部分：通过 A2A 暴露并启动服务器
================================================================================
📝 产品目录服务器代码已保存到 /tmp/product_catalog_server.py

🚀 启动产品目录代理服务器...
   等待服务器准备就绪...
...
✅ 产品目录代理服务器正在运行！
   服务器 URL：http://localhost:8001
   代理卡片：http://localhost:8001/.well-known/agent-card.json

📋 产品目录代理卡片：
{
  "capabilities": {},
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "description": "外部供应商的产品目录代理，提供产品信息和可用性。",
  "name": "product_catalog_agent",
  "preferredTransport": "JSONRPC",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "description": "外部供应商的产品目录代理，提供产品信息和可用性。\n    我是来自外部供应商的产品目录专家。\n    当被问及产品时，使用 get_product_info 工具从目录中获取数据。\n    提供清晰、准确的产品信息，包括价格、可用性和规格。\n    如果被问及多个产品，请逐个查找。\n    保持专业和乐于助人。\n    ",
      "id": "product_catalog_agent",
      "name": "model",
      "tags": [
        "llm"
      ]
    },
    {
      "description": "获取给定产品的产品信息。",
      "id": "product_catalog_agent-get_product_info",
      "name": "get_product_info",
      "tags": [
        "llm",
        "tools"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": false,
  "url": "http://localhost:8001",
  "version": "0.0.1"
}

✨ 关键信息：
   名称：product_catalog_agent
   描述：外部供应商的产品目录代理，提供产品信息和可用性。
   URL：http://localhost:8001
   技能：暴露了 2 个能力

================================================================================
第4部分：创建客户支持代理（消费者）
================================================================================
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/Day-5/day_5a_agent2agent_communication.py:273: UserWarning: [实验性] RemoteA2aAgent：ADK 对 A2A 支持的实现（A2aAgentExecutor、RemoteA2aAgent 及相应的支持组件等）处于实验模式，可能会有重大变更。A2A 协议和 SDK 本身不是实验性的。一旦足够稳定，实验模式将被移除。欢迎您的反馈。
  remote_product_catalog_agent = RemoteA2aAgent(

✅ 远程产品目录代理代理创建成功！
   连接到：http://localhost:8001
   代理卡片：http://localhost:8001/.well-known/agent-card.json
   客户支持代理现在可以像本地子代理一样使用它！

✅ 客户支持代理创建成功！
   模型：gemini-2.5-flash-lite
   子代理：1 个（通过 A2A 的远程产品目录代理）
   准备帮助客户！

================================================================================
第5部分：测试 A2A 通信
================================================================================

🧪 测试 A2A 通信...

👤 客户：你能告诉我关于 iPhone 15 Pro 的信息吗？有库存吗？

🎧 支持代理响应：
------------------------------------------------------------
警告：响应中有非文本部分：['function_call']，返回来自文本部分的连接文本结果。检查完整的 candidates.content.parts 访问器以获取完整的模型响应。
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/agents/remote_a2a_agent.py:379: UserWarning: [实验性] convert_genai_part_to_a2a_part：ADK 对 A2A 支持的实现（A2aAgentExecutor、RemoteA2aAgent 及相应的支持组件等）处于实验模式，可能会有重大变更。A2A 协议和 SDK 本身不是实验性的。一旦足够稳定，实验模式将被移除。欢迎您的反馈。
  converted_part = self._genai_part_converter(part)
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/a2a/converters/event_converter.py:239: UserWarning: [实验性] convert_a2a_message_to_event：ADK 对 A2A 支持的实现（A2aAgentExecutor、RemoteA2aAgent 及相应的支持组件等）处于实验模式，可能会有重大变更。A2A 协议和 SDK 本身不是实验性的。一旦足够稳定，实验模式将被移除。欢迎您的反馈。
  return convert_a2a_message_to_event(
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/a2a/converters/event_converter.py:309: UserWarning: [实验性] convert_a2a_part_to_genai_part：ADK 对 A2A 支持的实现（A2aAgentExecutor、RemoteA2aAgent 及相应的支持组件等）处于实验模式，可能会有重大变更。A2A 协议和 SDK 本身不是实验性的。一旦足够稳定，实验模式将被移除。欢迎您的反馈。
  part = part_converter(a2a_part)
iPhone 15 Pro 可供购买，价格为 999 美元。我们的库存很少，仅剩 8 台。它具有 128GB 存储容量和钛金属饰面。
------------------------------------------------------------

👤 客户：我在找一台笔记本电脑。你能为我比较一下 Dell XPS 15 和 MacBook Pro 14 吗？

🎧 支持代理响应：
------------------------------------------------------------
警告：响应中有非文本部分：['function_call']，返回来自文本部分的连接文本结果。检查完整的 candidates.content.parts 访问器以获取完整的模型响应。
Dell XPS 15 的价格为 1,299 美元，库存有 45 台。它具有 15.6 英寸显示屏、16GB 内存和 512GB SSD。

MacBook Pro 14" 的价格为 1,999 美元，库存有 22 台。它配备了 M3 Pro 芯片、18GB 内存和 512GB SSD。
------------------------------------------------------------

👤 客户：你们有 Sony WH-1000XM5 耳机吗？价格是多少？

🎧 支持代理响应：
------------------------------------------------------------
警告：响应中有非文本部分：['function_call']，返回来自文本部分的连接文本结果。检查完整的 candidates.content.parts 访问器以获取完整的模型响应。
Sony WH-1000XM5 耳机有库存，价格为 399 美元。它们具有降噪技术和 30 小时电池续航。
------------------------------------------------------------

================================================================================
清理
================================================================================

🛑 停止产品目录服务器...
✅ 服务器已停止

================================================================================
总结
================================================================================

🎯 关键要点：
✅ A2A 协议支持跨组织的代理通信
✅ to_a2a() 使代理可通过自动生成的代理卡片访问
✅ RemoteA2aAgent 将远程代理作为本地子代理消费
✅ 代理卡片在 /.well-known/agent-card.json 描述能力

📊 A2A 与本地子代理比较：
在以下情况使用 A2A：
   • 代理位于不同的代码库/组织中
   • 需要跨语言/框架通信
   • 需要正式的 API 合约

在以下情况使用本地子代理：
   • 同一代码库/团队内部
   • 需要低延迟
   • 相同的语言/框架

📚 了解更多：
• A2A 协议：https://a2a-protocol.org/
• 暴露代理：https://google.github.io/adk-docs/a2a/quickstart-exposing/
• 消费代理：https://google.github.io/adk-docs/a2a/quickstart-consuming/