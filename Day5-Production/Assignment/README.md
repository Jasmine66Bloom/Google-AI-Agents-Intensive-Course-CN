# 第5天 - Agent2Agent通信与生产环境部署

此文件夹包含基于Kaggle 5天智能体课程第5天Jupyter笔记本的Python脚本 - 这是最后一天！

## 脚本概述

### 1. `day_5a_agent2agent_communication.py`
**Agent2Agent (A2A) 通信**

此脚本演示：
- 理解A2A协议以及何时使用它与本地子智能体
- 常见的A2A架构模式（跨框架、跨语言、跨组织）
- 使用`to_a2a()`通过A2A暴露ADK智能体
- 使用`RemoteA2aAgent`消费远程智能体
- 构建产品目录集成系统

**关键概念：**
- **A2A协议**：跨网络智能体间通信的标准
- **智能体卡片**：描述智能体能力的JSON文档
- **to_a2a()**：通过自动生成的智能体卡片暴露智能体
- **RemoteA2aAgent**：用于消费远程智能体的客户端代理
- **跨组织集成**：来自不同团队/公司的智能体

**示例用例：**
- 与外部供应商服务集成
- 具有智能体专业化的微服务架构
- 跨语言智能体通信（Python ↔ Java）
- 第三方智能体市场集成

### 2. `day_5b_agent_deployment.py`
**将ADK智能体部署到生产环境**

此脚本演示：
- 构建生产就绪的ADK智能体
- 理解部署选项（Agent Engine、Cloud Run、GKE）
- 创建部署配置文件
- 使用ADK CLI部署到Vertex AI Agent Engine
- 使用Python SDK测试已部署的智能体
- 理解Vertex AI Memory Bank用于长期记忆
- 成本管理和清理最佳实践

**关键概念：**
- **Vertex AI Agent Engine**：用于托管智能体的完全托管服务
- **部署配置**：硬件规格和扩展设置
- **生产架构**：分离代码、配置和密钥
- **Memory Bank**：跨会话的长期记忆
- **成本管理**：免费层级、扩展和清理

**示例用例：**
- 将客户支持智能体部署到生产环境
- 使用自动扩展基础设施扩展智能体
- 构建具有持久记忆的多会话智能体
- 在企业环境中管理智能体群

## 前置条件

确保您已完成项目根目录的设置：

```bash
# 从项目根目录
source venv/bin/activate  # 激活虚拟环境
```

如果尚未设置项目，请运行：

```bash
cd ..  # 转到项目根目录
./setup.sh
source venv/bin/activate
```

### 第5b天（部署）的额外前置条件

**对于生产环境部署，您需要：**
- Google Cloud Platform账户（[在此注册](https://cloud.google.com/free)）
- 已启用计费（免费层级包含90天300美元的额度）
- 已启用所需的API（Vertex AI、Cloud Storage、Logging等）

**注意：** 部署脚本提供指导但不执行实际部署。要部署，请按照脚本输出中的说明进行操作。

## 运行脚本

### 运行脚本5a（A2A通信）

```bash
# 确保您在Day-5目录中且已激活venv
python day_5a_agent2agent_communication.py
```

**它做什么：**
1. **第1部分**：创建具有产品查找工具的产品目录智能体
2. **第2和第3部分**：通过A2A暴露智能体并在localhost:8001上启动服务器
3. **查看智能体卡片**：获取并显示自动生成的智能体卡片
4. **第4部分**：创建消费产品目录智能体的客户支持智能体
5. **第5部分**：使用多个查询测试A2A通信
6. **清理**：停止服务器

**注意：** 此脚本启动后台服务器。脚本会自动处理清理，但如果需要，您可以使用Ctrl+C手动停止它。

### 运行脚本5b（部署指南）

```bash
python day_5b_agent_deployment.py
```

**它做什么：**
1. **解释部署选项**：Agent Engine、Cloud Run、GKE
2. **创建智能体目录**：生成生产就绪的智能体文件
3. **解释部署过程**：分步部署说明
4. **解释测试**：如何测试已部署的智能体
5. **解释Memory Bank**：长期记忆概念
6. **解释清理**：成本管理和资源删除

**注意：** 此脚本是教育性的，并创建模板文件。实际部署需要Google Cloud凭据和`adk deploy`命令。

## 理解输出

### 第5a天输出（A2A通信）

**智能体创建：**
```
✅ Product Catalog Agent created successfully!
   Model: gemini-2.5-flash-lite
   Tool: get_product_info()
   Ready to be exposed via A2A...
```

**服务器启动：**
```
🚀 Starting Product Catalog Agent server...
   Waiting for server to be ready...
.....
✅ Product Catalog Agent server is running!
   Server URL: http://localhost:8001
   Agent card: http://localhost:8001/.well-known/agent-card.json
```

**智能体卡片：**
```json
{
  "name": "product_catalog_agent",
  "description": "External vendor's product catalog agent...",
  "url": "http://localhost:8001",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "id": "product_catalog_agent-get_product_info",
      "name": "get_product_info",
      "description": "Get product information for a given product."
    }
  ]
}
```

**A2A通信测试：**
```
👤 Customer: Can you tell me about the iPhone 15 Pro? Is it in stock?

🎧 Support Agent response:
------------------------------------------------------------
The iPhone 15 Pro is available for $999. We currently have low stock,
with only 8 units remaining. It features a 128GB storage capacity and
a titanium finish.
------------------------------------------------------------
```

### 第5b天输出（部署指南）

**目录创建：**
```
📁 Creating agent directory: sample_agent/
   ✅ Created sample_agent/agent.py
   ✅ Created sample_agent/requirements.txt
   ✅ Created sample_agent/.env
   ✅ Created sample_agent/.agent_engine_config.json

✅ Agent directory created successfully!
   Directory structure:
   sample_agent/
   ├── agent.py                  # The agent logic
   ├── requirements.txt          # The libraries
   ├── .env                      # The configuration
   └── .agent_engine_config.json # The hardware specs
```

**部署说明：**
```
🚀 Deployment Steps:

   Step 1: Set your PROJECT_ID
   ```bash
   export GOOGLE_CLOUD_PROJECT='your-project-id'
   ```

   Step 2: Authenticate with Google Cloud
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

   Step 3: Deploy the agent
   ```bash
   adk deploy agent_engine \
     --project=$GOOGLE_CLOUD_PROJECT \
     --region=us-east4 \
     sample_agent \
     --agent_engine_config_file=sample_agent/.agent_engine_config.json
   ```
```

## Agent2Agent (A2A) 协议深入探讨

### 什么是A2A？

[Agent2Agent协议](https://a2a-protocol.org/)是一个开放标准，使智能体能够跨以下环境进行通信：
- **不同框架**（ADK、LangChain、CrewAI等）
- **不同语言**（Python、JavaScript、Java等）
- **不同组织**（您的公司 ↔ 供应商服务）

### A2A架构模式

**模式1：跨框架集成**
```
┌──────────────────┐           ┌──────────────────┐
│ ADK Agent        │  ─A2A──▶  │ LangChain Agent  │
│ (Python)         │           │ (Python)         │
└──────────────────┘           └──────────────────┘
```

**模式2：跨语言通信**
```
┌──────────────────┐           ┌──────────────────┐
│ Python Agent     │  ─A2A──▶  │ Java Agent       │
│ (ADK)            │           │ (Custom)         │
└──────────────────┘           └──────────────────┘
```

**模式3：跨组织边界**
```
┌──────────────────┐           ┌──────────────────┐
│ Your Internal    │  ─A2A──▶  │ External Vendor  │
│ Support Agent    │           │ Product Catalog  │
│ (your-domain)    │           │ (vendor.com)     │
└──────────────────┘           └──────────────────┘
```

### A2A与本地子智能体决策表

| 因素 | 使用A2A | 使用本地子智能体 |
|--------|---------|---------------------|
| **位置** | 不同的机器/服务 | 同一进程 |
| **所有权** | 不同的团队/组织 | 您的团队 |
| **语言** | 需要跨语言 | 相同语言 |
| **框架** | 不同的框架 | 相同框架 |
| **性能** | 网络延迟可接受 | 需要低延迟 |
| **契约** | 正式API契约 | 内部接口 |
| **示例** | 供应商产品目录 | 内部工作流步骤 |

### 智能体卡片说明

**智能体卡片**是发布在`/.well-known/agent-card.json`的JSON文档，描述：

```json
{
  "name": "agent_name",
  "description": "What the agent does",
  "url": "http://agent-host:port",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "id": "skill_id",
      "name": "skill_name",
      "description": "What this skill does"
    }
  ],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"]
}
```

**可以将其视为：** 告诉其他智能体如何与此智能体协作的"名片"。

### 使用to_a2a()暴露智能体

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Convert agent to A2A-compatible app
a2a_app = to_a2a(my_agent, port=8001)

# Start the server
# uvicorn will serve the agent at http://localhost:8001
```

**to_a2a()做什么：**
1. 将智能体包装在FastAPI/Starlette服务器中
2. 从智能体定义自动生成智能体卡片
3. 在`/.well-known/agent-card.json`提供智能体卡片
4. 处理A2A协议端点（`/tasks`）
5. 管理请求/响应格式化

### 使用RemoteA2aAgent消费智能体

```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Create client-side proxy
remote_agent = RemoteA2aAgent(
    name="remote_service",
    description="Remote agent description",
    agent_card="http://vendor.com/.well-known/agent-card.json"
)

# Use it like a local sub-agent!
my_agent = LlmAgent(
    name="my_agent",
    sub_agents=[remote_agent]  # That's it!
)
```

**RemoteA2aAgent做什么：**
1. 获取并读取远程智能体卡片
2. 为远程智能体创建本地代理
3. 将子智能体调用转换为A2A HTTP请求
4. 透明地处理所有协议通信

## 生产环境部署深入探讨

### 部署选项比较

| 功能 | Agent Engine | Cloud Run | GKE |
|---------|-------------|-----------|-----|
| **管理** | 完全托管 | 无服务器 | 自管理 |
| **扩展** | 自动（内置） | 自动（无服务器） | 手动/自动 |
| **设置** | 最简单 | 简单 | 复杂 |
| **会话管理** | 内置 | 手动 | 手动 |
| **最适合** | AI智能体 | 通用应用 | 复杂系统 |
| **免费层级** | 10个智能体 | 慷慨 | 计算小时 |

### Agent Engine架构

```
┌─────────────┐
│  Your Code  │  ← agent.py, tools, instructions
└──────┬──────┘
       │ adk deploy agent_engine
       ↓
┌─────────────┐
│Agent Engine │
│             │
│ • Auto-scale│  ← 0-N instances based on load
│ • Sessions  │  ← Built-in session management
│ • Logging   │  ← Automatic Cloud Logging
│ • Monitoring│  ← Cloud Monitoring integration
│ • Memory    │  ← Memory Bank support
└──────┬──────┘
       │ HTTPS/REST API
       ↓
┌─────────────┐
│   Clients   │  ← Your apps, web UI, mobile
└─────────────┘
```

### 生产智能体结构

```
my_agent/
├── agent.py                      # Agent definition
├── requirements.txt              # Python dependencies
├── .env                          # Environment config
└── .agent_engine_config.json     # Deployment config
```

**agent.py:**
```python
from google.adk.agents import Agent
import vertexai
import os

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

def my_tool(param: str) -> dict:
    # Tool implementation
    pass

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash-lite",
    description="Agent description",
    instruction="Agent instructions",
    tools=[my_tool]
)
```

**requirements.txt:**
```
google-adk
opentelemetry-instrumentation-google-genai
# Add other dependencies
```

**.env:**
```
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI=1
```

**.agent_engine_config.json:**
```json
{
    "min_instances": 0,
    "max_instances": 1,
    "resource_limits": {
        "cpu": "1",
        "memory": "1Gi"
    }
}
```

### 部署过程

**1. 启用所需的API：**
```bash
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudtrace.googleapis.com \
  telemetry.googleapis.com
```

**2. 部署：**
```bash
adk deploy agent_engine \
  --project=YOUR_PROJECT_ID \
  --region=us-east4 \
  my_agent \
  --agent_engine_config_file=my_agent/.agent_engine_config.json
```

**3. 获取资源名称：**
```
projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID
```

**4. 测试：**
```python
import vertexai
from vertexai import agent_engines

vertexai.init(project='your-project', location='us-east4')

# Get deployed agent
agents = list(agent_engines.list())
agent = agents[0]

# Test
async for event in agent.async_stream_query(
    message="Test query",
    user_id="user123"
):
    print(event)
```

**5. 清理：**
```python
agent_engines.delete(
    resource_name=agent.resource_name,
    force=True
)
```

### Vertex AI Memory Bank

**问题：**
- 会话记忆在会话结束时忘记所有内容
- 用户必须在每次对话中重复偏好
- 无法从过去的交互中学习

**解决方案 - Memory Bank：**

```
Session 1:
User: "I prefer Celsius"
Agent: "Noted!"
→ Memory Bank stores: "User prefers Celsius"

Session 2 (days later):
User: "Weather in Tokyo?"
Agent: "Tokyo is 21°C" ← Automatically uses Celsius!
```

**如何启用：**

1. **添加记忆工具：**
```python
from google.adk.tools import preload_memory

agent = LlmAgent(
    name="my_agent",
    tools=[preload_memory],  # Loads relevant memories
    ...
)
```

2. **添加回调：**
```python
async def save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    after_agent_callback=save_to_memory,
    ...
)
```

3. **重新部署**

**Memory Bank与会话记忆对比：**

| 功能 | 会话记忆 | Memory Bank |
|---------|---------------|-------------|
| **范围** | 单次对话 | 所有对话 |
| **持续时间** | 直到会话结束 | 永久 |
| **用例** | "我刚才说了什么？" | "我最喜欢的城市是什么？" |
| **存储** | 内存/会话 | Vertex AI服务 |
| **检索** | 自动（上下文） | 基于工具的搜索 |

## 常见问题和解决方案

### A2A通信问题

#### 问题：测试A2A时出现"Connection refused"
**解决方案：**
- 检查服务器是否正在运行：`curl http://localhost:8001/.well-known/agent-card.json`
- 等待服务器启动（可能需要5-10秒）
- 检查端口冲突：`lsof -i :8001`

#### 问题：未找到智能体卡片（404）
**解决方案：**
- 验证服务器已成功启动
- 检查URL包含`/.well-known/agent-card.json`
- 确保`to_a2a()`被正确调用

#### 问题：远程智能体无响应
**解决方案：**
- 检查服务器日志中的错误
- 验证API密钥在服务器环境中已设置
- 直接测试服务器：`curl http://localhost:8001/.well-known/agent-card.json`

### 部署问题

#### 问题："Project ID not set"错误
**解决方案：**
```bash
export GOOGLE_CLOUD_PROJECT='your-project-id'
# Or set in .env file
```

#### 问题：API未启用错误
**解决方案：**
- 访问https://console.cloud.google.com/flows/enableapi
- 启用部署指南中列出的所有必需API
- 等待几分钟以使API启用传播

#### 问题：部署失败并出现权限错误
**解决方案：**
```bash
# Ensure you're authenticated
gcloud auth login

# Set project
gcloud config set project your-project-id

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/aiplatform.user"
```

#### 问题：部署挂起或超时
**解决方案：**
- 检查互联网连接
- 验证区域正确（使用：us-east4、europe-west1等）
- 如果某个区域遇到问题，尝试不同的区域
- 检查GCP状态页面是否有中断

## 最佳实践

### A2A通信最佳实践

1. **始终发布智能体卡片**
   - 在`/.well-known/agent-card.json`（标准路径）提供
   - 保持描述清晰准确
   - 对智能体卡片进行版本控制

2. **优雅地处理网络故障**
   ```python
   try:
       response = await remote_agent.call(...)
   except Exception as e:
       # Fallback behavior
       return default_response
   ```

3. **保护A2A端点**
   - 在生产环境中使用HTTPS
   - 实现API密钥身份验证
   - 对请求进行速率限制

4. **监控A2A流量**
   - 记录所有跨智能体调用
   - 跟踪响应时间
   - 为故障设置警报

### 生产环境部署最佳实践

1. **从小开始**
   ```json
   {
       "min_instances": 0,  // Scale to zero when idle
       "max_instances": 1   // Limit for testing
   }
   ```

2. **启用日志记录**
   - 使用Cloud Logging进行调试
   - 启用跟踪以进行性能分析
   - 设置错误监控

3. **在生产环境之前测试**
   - 首先部署到开发/测试环境
   - 运行负载测试
   - 验证所有工具正常工作

4. **成本管理**
   - 从min_instances=0开始以节省成本
   - 在Cloud Console中监控使用情况
   - 设置计费警报
   - 及时删除测试部署

5. **版本控制**
   - 使用版本号标记部署
   - 将部署配置保存在git中
   - 记录版本之间的更改

## 学习资源

### A2A协议
- [官方A2A协议网站](https://a2a-protocol.org/)
- [A2A协议规范](https://a2a-protocol.org/latest/specification/)
- [A2A教程](https://a2a-protocol.org/latest/tutorials/)

### ADK A2A文档
- [ADK中的A2A介绍](https://google.github.io/adk-docs/a2a/intro/)
- [暴露智能体快速入门](https://google.github.io/adk-docs/a2a/quickstart-exposing/)
- [消费智能体快速入门](https://google.github.io/adk-docs/a2a/quickstart-consuming/)

### 部署文档
- [ADK部署指南](https://google.github.io/adk-docs/deploy/)
- [部署到Agent Engine](https://google.github.io/adk-docs/deploy/agent-engine/)
- [部署到Cloud Run](https://google.github.io/adk-docs/deploy/cloud-run/)
- [部署到GKE](https://google.github.io/adk-docs/deploy/gke/)

### Vertex AI Agent Engine
- [Agent Engine概述](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [Agent Engine位置](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)
- [Memory Bank文档](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview)

### 视频教程
- [Google Cloud免费试用设置（3分钟）](https://youtu.be/-nUAQq_evxc)
- [ADK部署演练](https://www.youtube.com/watch?v=YOUR_VIDEO)

## 下一步

完成第5天后，您已学习：
- ✅ 使用A2A协议构建多智能体系统
- ✅ 将智能体作为服务暴露以供跨组织使用
- ✅ 透明地消费远程智能体
- ✅ 使用Agent Engine将智能体部署到生产环境
- ✅ 管理成本和清理资源
- ✅ 使用Memory Bank添加长期记忆

**🎓 课程完成！**

您已完成整个5天AI智能体强化课程！您现在拥有完整的技能集：
- 从头开始构建智能智能体
- 添加工具和功能
- 管理会话和记忆
- 调试和评估智能体性能
- 部署到生产基础设施

**接下来：**
1. 构建您自己的AI智能体项目
2. 将其部署到生产环境
3. 在Kaggle Discord上分享您的工作
4. 探索高级ADK功能
5. 为开源社区做出贡献！

**练习项目：**
1. 构建具有产品目录集成的客户支持智能体
2. 创建具有专业化智能体的多智能体研究系统
3. 部署具有Memory Bank的个人助手
4. 构建A2A智能体市场

祝您构建愉快！🚀🎉
