# 5-Day AI Agents Intensive Course - Project Repository (Chinese Translation Available)

![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Translation](https://img.shields.io/badge/Translation-Chinese-green)

## 概述 / Overview
此仓库记录了我从**Google和Kaggle（2025年11月10-14日）5天AI智能体强化课程**中学到的知识和项目。该课程专注于使用**Google的Gemini API**和现代智能体框架构建智能、自主的AI智能体。

**📢 中文翻译说明：** 本项目包含完整的中文翻译版本。所有翻译文件均以`-zh.md`或`-zh.py`后缀命名，与原始英文文件并存。

---

## 原始项目 / Original Project

本项目是基于 [amol-davkhar/Google-AI-Agents-intensive-course](https://github.com/amol-davkhar/Google-AI-Agents-intensive-course) 的中文翻译版本。

This repository is a Chinese translation of [amol-davkhar/Google-AI-Agents-intensive-course](https://github.com/amol-davkhar/Google-AI-Agents-intensive-course).

---

## 关于课程 / About the Course
5天AI智能体强化课程是由Google的AI研究人员和工程师创建的免费结构化在线项目。它涵盖了AI智能体的理论基础和实践应用，从简单的智能体到完整的多智能体系统。

---

## 课程结构 / Course Structure

| 天数 | 主题 | 关键概念 |
| :--- | :--- | :--- |
| **Day 1** | **Foundations of AI Agents** | Agent Architectures, Reasoning Loops, Gemini API |
| **第1天** | **AI智能体基础** | 智能体架构、推理循环、Gemini API |
| **Day 2** | **Tools & Function Calling** | Tool Use, LangChain/LangGraph, Connecting to APIs |
| **第2天** | **工具与函数调用** | 工具使用、LangChain/LangGraph、连接API |
| **Day 3** | **Reasoning & Planning** | ReAct Pattern, Chain of Thought, Multi-step planning |
| **第3天** | **推理与规划** | ReAct模式、思维链、多步规划 |
| **Day 4** | **Memory & Context** | RAG (Retrieval Augmented Generation), Vector Databases, Long-term Memory |
| **第4天** | **记忆与上下文** | RAG（检索增强生成）、向量数据库、长期记忆 |
| **Day 5** | **Multi-Agent Systems** | Orchestration, CrewAI/AutoGen, Production Deployment |
| **第5天** | **多智能体系统** | 编排、CrewAI/AutoGen、生产环境部署 |

## 技术栈 / Tech Stack

- **LLMs**: Google Gemini (Gemini-Pro, Gemini-Flash)
- **大语言模型**：Google Gemini（Gemini-Pro、Gemini-Flash）
- **Frameworks**: LangChain, LangGraph, Google Gen AI SDK
- **框架**：LangChain、LangGraph、Google Gen AI SDK
- **Vector Stores**: ChromaDB / FAISS
- **向量存储**：ChromaDB / FAISS
- **Environment**: Python, Jupyter Notebooks
- **环境**：Python、Jupyter笔记本

## 仓库结构 / Repository Structure

```bash
├── Day1-Agent-Basics/       # Basic agent setup and API calls / 基础智能体设置和API调用
│   ├── Assignment/
│   │   ├── 1a-responses.md / 1a-responses-zh.md
│   │   ├── 1b-responses.md / 1b-responses-zh.md
│   │   ├── day_1a_prompt_to_action.py / day_1a_prompt_to_action-zh.py
│   │   ├── day_1b_agent_architectures.py / day_1b_agent_architectures-zh.py
│   │   ├── README.md / README-zh.md
│   ├── Notebooks/
│   └── Whitepaper/
├── Day2-Tools-Mcp/         # Agents using Calculator, Search, and custom tools / 使用计算器、搜索和自定义工具的智能体
│   ├── Assignment/
│   │   ├── 2a-responses.md / 2a-responses-zh.md
│   │   ├── 2b-responses.md / 2b-responses-zh.md
│   │   ├── day_2a_agent_tools.py / day_2a_agent_tools-zh.py
│   │   ├── day_2b_agent_tools_best_practices.py / day_2b_agent_tools_best_practices-zh.py
│   │   ├── README.md / README-zh.md
│   ├── Notebooks/
│   └── Whitepaper/
├── Day3-Memory-Context/    # Logic and reasoning workflows / 逻辑和推理工作流
│   ├── Assignment/
│   │   ├── 3a-responses.md / 3a-responses-zh.md
│   │   ├── 3b-responses.md / 3b-responses-zh.md
│   │   ├── day_3a_agent_sessions.py / day_3a_agent_sessions-zh.py
│   │   ├── day_3b_agent_memory.py / day_3b_agent_memory-zh.py
│   │   ├── README.md / README-zh.md
│   ├── Notebooks/
│   └── Whitepaper/
├── Day4-Quality-Evaluation/ # RAG implementation and database connections / RAG实现和数据库连接
│   ├── Assignment/
│   │   ├── 4a-responses.md / 4a-responses-zh.md
│   │   ├── 4b-responses.md / 4b-responses-zh.md
│   │   ├── day_4a_agent_observability.py / day_4a_agent_observability-zh.py
│   │   ├── day_4b_agent_evaluation.py / day_4b_agent_evaluation-zh.py
│   │   ├── README.md / README-zh.md
│   ├── Notebooks/
│   └── Whitepaper/
├── Day5-Production/        # Final complex systems / 最终复杂系统
│   ├── Assignment/
│   │   ├── 5a-responses.md / 5a-responses-zh.md
│   │   ├── 5b-responses.md / 5b-responses-zh.md
│   │   ├── day_5a_agent2agent_communication.py / day_5a_agent2agent_communication-zh.py
│   │   ├── day_5b_agent_deployment.py / day_5b_agent_deployment-zh.py
│   │   ├── README.md / README-zh.md
│   ├── Notebooks/
│   └── Whitepaper/
├── README.md / README-zh.md
├── QUICKSTART.md / QUICKSTART-zh.md
└── requirements.txt
```

## 前置条件 / Prerequisites
- Python basics / Python基础知识
- Google account for AI Studio / 用于AI Studio的Google账户
- Verified Kaggle account / 已验证的Kaggle账户
- Kaggle phone verification / Kaggle手机验证

---

## 设置说明 / Setup Instructions

### English Version / 英文版本
1. Create and verify your Kaggle account
2. Set up Google AI Studio and generate an API key
3. Join the Kaggle Discord community
4. Complete Kaggle phone verification to access code labs

### 中文版本 / Chinese Version
1. 创建并验证您的Kaggle账户
2. 设置Google AI Studio并生成API密钥
3. 加入Kaggle Discord社区
4. 完成Kaggle手机验证以访问代码实验室

---

## 快速开始 / Quick Start

### English Version / 英文版本
See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

### 中文版本 / Chinese Version
查看 [QUICKSTART-zh.md](QUICKSTART-zh.md) 获取详细的设置说明。

---

## 许可证 / License
Personal learning materials. Course content belongs to Google and Kaggle.

个人学习材料。课程内容属于Google和Kaggle。

---

## 翻译贡献 / Translation Contribution

如果您发现翻译错误或有改进建议，欢迎提交Issue或Pull Request。

If you find any translation errors or have suggestions for improvement, please feel free to submit an Issue or Pull Request.
