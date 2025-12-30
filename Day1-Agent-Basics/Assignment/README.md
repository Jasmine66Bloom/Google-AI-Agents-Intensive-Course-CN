# 第 1 天 - AI 智能体 Python 脚本

此文件夹包含基于 Kaggle 5 天智能体课程第 1 天 Jupyter 笔记本的 Python 脚本。

## 脚本概述

### 1. `day_1a_prompt_to_action.py`
**从提示词到行动 - 你的第一个 AI 智能体**

此脚本演示：
- 使用 Google ADK 设置基本 AI 智能体
- 使用 Google Search 工具
- 运行需要当前信息的查询
- 了解智能体如何推理和采取行动

**关键概念：**
- 智能体不仅仅是响应——它们会推理和行动
- 工具扩展智能体能力
- 智能体可以决定何时使用工具

### 2. `day_1b_agent_architectures.py`
**多智能体系统与工作流模式**

此脚本演示四种强大的工作流模式：

1. **基于 LLM 的编排**：LLM 决定调用哪些智能体的动态工作流
   - 示例：研究智能体 + 总结智能体

2. **顺序工作流**：智能体按顺序运行的固定管道
   - 示例：大纲智能体 → 写作智能体 → 编辑智能体

3. **并行工作流**：独立任务的并发执行
   - 示例：多个研究智能体同时工作

4. **循环工作流**：通过反馈进行迭代优化
   - 示例：Writer → Critic → Refiner（循环直到批准）

## 设置说明

### 快速设置（macOS/Linux）

开始的最简单方法是使用自动化设置脚本：

```bash
# 从项目根目录
./setup.sh
```

此脚本将：
- 创建 Python 虚拟环境
- 安装所有必需的包
- 为你的 API key 创建 .env 文件模板

### 手动设置

如果你更喜欢手动设置或使用 Windows：

1. **创建虚拟环境**（macOS 上的 Python 3.14+ 需要此操作）

   ```bash
   # 从项目根目录
   python3 -m venv venv

   # 激活虚拟环境
   source venv/bin/activate  # 在 macOS/Linux 上
   # 或
   venv\Scripts\activate     # 在 Windows 上
   ```

2. **安装必需的包**

   ```bash
   pip install -r requirements.txt
   ```

   **macOS 用户注意：** 激活虚拟环境后，使用 `pip`（而不是 `pip3`）。

3. **获取 Gemini API Key**
   - 访问：https://aistudio.google.com/app/api-keys
   - 创建新的 API key

4. **配置你的 API Key**
   ```bash
   # 从项目根目录
   cp .env.example .env
   ```

   然后编辑 `.env` 文件，将 `your-api-key-here` 替换为你的实际 API key：
   ```
   GOOGLE_API_KEY=your-actual-api-key-here
   ```

   **重要：** `.env` 文件已在 `.gitignore` 中，因此你的 API key 不会被提交到 git。

## 运行脚本

**重要：** 运行脚本之前，请确保你的虚拟环境已激活！

```bash
# 激活虚拟环境（如果尚未激活）
source venv/bin/activate  # 在 macOS/Linux 上
# 或
venv\Scripts\activate     # 在 Windows 上
```

### 运行脚本 1a（基本智能体）
```bash
cd Day-1
python day_1a_prompt_to_action.py
```

这将：
- 创建一个带有 Google Search 的基本智能体
- 运行示例查询
- 让你尝试自己的自定义查询

### 运行脚本 1b（多智能体架构）
```bash
cd Day-1
python day_1b_agent_architectures.py
```

运行此脚本时，你将提示选择要运行的模式：
- 选项 1：基于 LLM 的编排
- 选项 2：顺序管道
- 选项 3：并行执行
- 选项 4：循环优化
- 选项 5：运行所有示例

**注意：** 运行所有示例可能需要几分钟并使用多个 API 调用。

## 理解输出

两个脚本都将显示：
- 智能体的思考过程
- 正在调用哪些工具
- 最终响应
- 会话管理（debug_session_id）

你可能会看到如下警告：
```
WARNING:google_genai.types:Warning: there are non-text parts in the response...
```
这些是正常的，表明智能体正在使用函数调用（工具）。

## 工作流模式决策指南

**使用顺序工作流，当：**
- 顺序很重要（每个步骤建立在前一个步骤之上）
- 你需要线性管道
- 可预测的执行很重要

**使用并行工作流，当：**
- 任务是独立的
- 速度很重要
- 你可以并发执行

**使用循环工作流，当：**
- 需要迭代改进
- 质量优化很重要
- 你需要重复循环直到满足条件

**使用 LLM 编排，当：**
- 需要动态决策
- 工作流应该适应查询
- 灵活性比可预测性更重要

## 故障排除

### 错误："command not found: pip" 或 "No module named..."
确保你的虚拟环境已激活：
```bash
source venv/bin/activate  # 在 macOS/Linux 上
# 你应该在你的终端提示符中看到 (venv)
```

如果你还没有设置虚拟环境，请运行设置脚本：
```bash
./setup.sh
```

### 错误："GOOGLE_API_KEY not found"
确保你在项目根目录中创建了 `.env` 文件：
```bash
# 从项目根目录
cp .env.example .env
# 然后编辑 .env 并添加你的 API key
```

### 错误：429（速率限制）
脚本包含重试逻辑，但如果你遇到速率限制：
- 等待几分钟再重试
- 考虑单独运行示例而不是一次性运行所有示例

### 错误："No module named 'google.adk'" 或 "No module named 'dotenv'"
安装所需的库：
```bash
# 从项目根目录
pip install -r requirements.txt
```

## 学习资源

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Quickstart for Python](https://google.github.io/adk-docs/get-started/python/)
- [ADK Agents Overview](https://google.github.io/adk-docs/agents/)
- [Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [Parallel Agents](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)

## 下一步

完成第 1 天后，继续学习第 2 天笔记本，了解：
- 自定义函数
- MCP 工具
- 长时间运行操作

祝学习愉快！
