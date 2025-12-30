"""
Day 1b: 多智能体系统与工作流模式
此脚本演示使用不同工作流模式构建多智能体系统：
- 基于 LLM 的编排（动态决策）
- 顺序工作流（固定管道）
- 并行工作流（并发执行）
- 循环工作流（迭代优化）

先决条件：
- pip install google-adk python-dotenv litellm
- 创建一个包含您的 DOUBAO_API_KEY 的 .env 文件
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool


def setup_api_key():
    """
    从 .env 文件配置豆包 API key。
    在项目根目录中查找 .env 文件。
    """
    # 从项目根目录加载 .env 文件（Day-1 文件夹的上一级）
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("DOUBAO_API_KEY")
    if not api_key:
        raise ValueError(
            "未找到 DOUBAO_API_KEY。请执行以下操作：\n"
            "1. 在项目根目录中将 .env.example 复制为 .env\n"
            "2. 将您的 API key 添加到 .env 文件中\n"
        )
    print("✅ 已从 .env 文件加载豆包 API key。")
    return api_key


# ============================================================================
# 模式 1：基于 LLM 的编排（动态工作流）
# ============================================================================

def create_llm_orchestrated_system():
    """
    创建一个基于 LLM 编排的多智能体系统。
    根智能体决定调用哪些子智能体以及调用顺序。
    """
    print("\n--- 正在创建 LLM 编排系统 ---")

    # 研究智能体
    research_agent = Agent(
        name="ResearchAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""你是一个专门的研究智能体。你的唯一工作是
        在给定主题上找到 2-3 条相关信息，并在引用中呈现发现。""",
        output_key="research_findings",
    )

    # 总结智能体：总结研究发现
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""阅读提供的研究发现：{research_findings}
        创建一个简明的摘要，作为包含 3-5 个要点的项目符号列表。""",
        output_key="final_summary",
    )

    # 根协调器：编排工作流
    root_agent = Agent(
        name="ResearchCoordinator",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""你是一个研究协调器。你的目标是回答用户的查询。
        1. 首先，你必须调用 `ResearchAgent` 工具来查找相关信息。
        2. 接下来，在收到研究发现后，你必须调用 `SummarizerAgent` 工具。
        3. 最后，将最终摘要清晰地呈现给用户作为你的回应。""",
        tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    )

    print("✅ 已创建 LLM 编排系统（研究 + 总结）")
    return root_agent


# ============================================================================
# 模式 2：顺序工作流（固定管道）
# ============================================================================

def create_sequential_blog_pipeline():
    """
    创建一个用于博客文章创建的顺序多智能体系统。
    智能体按固定顺序运行：大纲 -> 撰写 -> 编辑
    """
    print("\n--- 正在创建顺序博客管道 ---")

    # 大纲智能体
    outline_agent = Agent(
        name="OutlineAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""为给定主题创建一个博客大纲，包括：
        1. 一个引人注目的标题
        2. 一个介绍性引子
        3. 3-5 个主要部分，每个部分 2-3 个要点
        4. 一个总结性思考""",
        output_key="blog_outline",
    )

    # 撰写智能体
    writer_agent = Agent(
        name="WriterAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""严格遵循此大纲：{blog_outline}
        撰写一篇简短的 200-300 字博客文章，采用引人入胜和信息丰富的语气。""",
        output_key="blog_draft",
    )

    # 编辑智能体
    editor_agent = Agent(
        name="EditorAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""编辑此草稿：{blog_draft}
        修正语法错误，改善流畅度和句子结构，并增强清晰度。""",
        output_key="final_blog",
    )

    # 顺序管道
    root_agent = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )

    print("✅ 已创建顺序管道（大纲 -> 撰写 -> 编辑）")
    return root_agent


# ============================================================================
# 模式 3：并行工作流（并发执行）
# ============================================================================

def create_parallel_research_system():
    """
    创建一个用于多主题研究的并行多智能体系统。
    多个研究智能体并发运行，然后聚合器组合结果。
    """
    print("\n--- 正在创建并行研究系统 ---")

    # 技术研究员
    tech_researcher = Agent(
        name="TechResearcher",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""研究最新的 AI/ML 趋势。包括 3 个关键发展、
        主要参与的公司以及潜在影响。保持简洁（100 字）。""",
        output_key="tech_research",
    )

    # 健康研究员
    health_researcher = Agent(
        name="HealthResearcher",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""研究最近的医学突破。包括 3 个重大进展、
        其实际应用和估计时间表。保持简洁（100 字）。""",
        output_key="health_research",
    )

    # 金融研究员
    finance_researcher = Agent(
        name="FinanceResearcher",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""研究当前的金融科技趋势。包括 3 个关键趋势、
        其市场影响和未来展望。保持简洁（100 字）。""",
        output_key="finance_research",
    )

    # 聚合器智能体
    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""将这三个研究发现组合成一个单一的执行摘要：

        **技术趋势：** {tech_research}
        **健康突破：** {health_research}
        **金融创新：** {finance_research}

        突出共同主题、令人惊讶的联系和关键要点。
        最终摘要应在 200 字左右。""",
        output_key="executive_summary",
    )

    # 并行研究团队
    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    # 顺序包装器，先运行并行团队，然后运行聚合器
    root_agent = SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_research_team, aggregator_agent],
    )

    print("✅ 已创建并行研究系统（技术 + 健康 + 金融 -> 聚合器）")
    return root_agent


# ============================================================================
# 模式 4：循环工作流（迭代优化）
# ============================================================================

def create_loop_story_refinement_system():
    """
    创建一个基于循环的多智能体系统，用于迭代故事优化。
    作家创建草稿，评论家审查它，优化者改进它。
    循环继续，直到评论家批准或达到最大迭代次数。
    """
    print("\n--- 正在创建循环故事优化系统 ---")

    # 初始撰写智能体
    initial_writer_agent = Agent(
        name="InitialWriterAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""根据用户的提示，撰写短篇故事的第一个草稿
        （约 100-150 字）。仅输出故事文本，不要有介绍或解释。""",
        output_key="current_story",
    )

    # 评论家智能体
    critic_agent = Agent(
        name="CriticAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""你是一个建设性的故事评论家。审查下面提供的故事。
        故事：{current_story}

        评估故事的情节、人物和节奏。
        - 如果故事写得很好且完整，你必须用确切的短语回应："APPROVED"
        - 否则，提供 2-3 条具体的、可操作的改进建议。""",
        output_key="critique",
    )

    # 退出循环函数
    def exit_loop():
        """当评论为 'APPROVED' 时调用此函数。"""
        return {"status": "approved", "message": "故事已批准。退出优化循环。"}

    # 优化智能体
    refiner_agent = Agent(
        name="RefinerAgent",
        model=LiteLlm(
            model="volcengine/doubao-1-5-lite-32k-250115",
            api_key=os.environ.get("DOUBAO_API_KEY")
        ),
        instruction="""你是一个故事优化者。你有一个故事草稿和评论。

        故事草稿：{current_story}
        评论：{critique}

        - 如果评论确切为 "APPROVED"，你必须调用 `exit_loop` 函数，不做其他操作。
        - 否则，重写故事草稿，以完全整合评论中的反馈。""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

    # 循环智能体
    story_refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, refiner_agent],
        max_iterations=2,
    )

    # 顺序包装器，先运行初始撰写，然后运行循环
    root_agent = SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_writer_agent, story_refinement_loop],
    )

    print("✅ 已创建循环优化系统（撰写 -> [评论 -> 优化] 循环）")
    return root_agent


# ============================================================================
# 主执行
# ============================================================================

async def run_example(agent, query, title):
    """使用给定的智能体和查询运行单个示例。"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    print(f"\n查询：{query}\n")

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(query)

    print("\n✅ 示例已完成！")


async def main():
    """演示所有工作流模式的主函数。"""
    print("\n" + "="*80)
    print("  Day 1b: 多智能体系统与工作流模式")
    print("="*80)

    # 设置
    setup_api_key()

    # 选择要运行的示例
    print("\n可用的工作流模式：")
    print("1. 基于 LLM 的编排（研究 + 总结）")
    print("2. 顺序管道（博客文章：大纲 -> 撰写 -> 编辑）")
    print("3. 并行执行（多主题研究）")
    print("4. 循环优化（迭代故事改进）")
    print("5. 运行所有示例")

    choice = input("\n选择一个选项（1-5）或按 Enter 运行所有：").strip()

    if choice in ["1", "5", ""]:
        # 示例 1：基于 LLM 的编排
        agent = create_llm_orchestrated_system()
        await run_example(
            agent,
            "量子计算的最新进展是什么，它们对 AI 意味着什么？",
            "示例 1：基于 LLM 的编排"
        )

    if choice in ["2", "5", ""]:
        # 示例 2：顺序工作流
        agent = create_sequential_blog_pipeline()
        await run_example(
            agent,
            "撰写一篇关于多智能体系统对软件开发人员好处的博客文章",
            "示例 2：顺序工作流（博客管道）"
        )

    if choice in ["3", "5", ""]:
        # 示例 3：并行工作流
        agent = create_parallel_research_system()
        await run_example(
            agent,
            "运行关于技术、健康和金融的每日执行简报",
            "示例 3：并行工作流（多主题研究）"
        )

    if choice in ["4", "5", ""]:
        # 示例 4：循环工作流
        agent = create_loop_story_refinement_system()
        await run_example(
            agent,
            "撰写一个关于灯塔看守人发现神秘发光地图的短篇故事",
            "示例 4：循环工作流（迭代故事优化）"
        )

    print("\n" + "="*80)
    print("  ✅ 所有选定的示例已完成！")
    print("="*80)

    print("\n📚 关键要点：")
    print("- LLM 编排：动态、灵活，但可能不可预测")
    print("- 顺序：确定性顺序，非常适合管道")
    print("- 并行：独立任务的并发执行以提高速度")
    print("- 循环：迭代优化以提高质量")
    print("\n🎯 根据您的用例选择正确的模式！")


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
