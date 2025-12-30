✅ ADK组件导入成功。
✅ 从.env文件加载了API密钥

================================================================================
第4天A部分：代理可观测性
================================================================================

📚 您将学习：
• 使用ADK Web UI和DEBUG日志调试代理
• 使用LoggingPlugin进行生产环境可观测性
• 创建自定义插件以满足特定需求
• 理解日志、跟踪和指标

================================================================================
演示：有缺陷的代理（用于调试练习）
================================================================================

🐛 此代理在count_papers工具中有一个故意的错误
该工具期望'str'类型，但应该接受'List[str]'

👉 在实际场景中，您将：
   1. 运行'adk web --log_level DEBUG'启动Web UI
   2. 使用以下内容测试代理：'Find latest quantum computing papers'
   3. 使用Events选项卡和Traces查找错误
   4. 查看function_call以查看不正确的参数类型

⚠️  注意：这是一个演示脚本。要实际调试：
   - 创建代理文件夹：adk create research-agent
   - 将代理定义复制到agent.py
   - 运行：adk web --log_level DEBUG
   - 使用Web UI进行交互和调试

================================================================================
演示：带有LoggingPlugin的研究代理
================================================================================
🧹 清理了logger.log
✅ 日志记录已配置

🚀 使用LoggingPlugin运行代理...
📊 观察全面的日志记录输出：


 ### 创建了新会话：debug_session_id

User > Find recent papers on quantum computing
[logging_plugin] 🚀 收到用户消息
[logging_plugin]    调用ID：e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    会话ID：debug_session_id
[logging_plugin]    用户ID：debug_user_id
[logging_plugin]    应用程序名称：InMemoryRunner
[logging_plugin]    根代理：research_paper_finder_agent
[logging_plugin]    用户内容：text: 'Find recent papers on quantum computing'
[logging_plugin] 🏃 调用开始
[logging_plugin]    调用ID：e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    启动代理：research_paper_finder_agent
[logging_plugin] 🤖 代理启动
[logging_plugin]    代理名称：research_paper_finder_agent
[logging_plugin]    调用ID：e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin] 🧠 LLM请求
[logging_plugin]    模型：gemini-2.5-flash-lite
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    系统指令：'Your task is to find research papers and count them.

       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'.
       2) Then, pas...'
[logging_plugin]    可用工具：['google_search_agent', 'count_papers_fixed']
[logging_plugin] 🧠 LLM响应
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    内容：function_call: google_search_agent
[logging_plugin]    Token使用情况 - 输入：250，输出：21
[logging_plugin] 📢 事件生成
[logging_plugin]    事件ID：4c138c18-ae91-4454-8bd3-fa8aa44b644d
[logging_plugin]    作者：research_paper_finder_agent
[logging_plugin]    内容：function_call: google_search_agent
[logging_plugin]    最终响应：False
[logging_plugin]    函数调用：['google_search_agent']
[logging_plugin] 🔧 工具启动
[logging_plugin]    工具名称：google_search_agent
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    函数调用ID：adk-02d3996c-1a40-4762-a773-6a22ae5b8622
[logging_plugin]    参数：{'request': 'recent papers on quantum computing'}
[logging_plugin] 🚀 收到用户消息
[logging_plugin]    调用ID：e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    会话ID：418bb018-2cf7-4b2a-8918-1b8a19e01601
[logging_plugin]    用户ID：debug_user_id
[logging_plugin]    应用程序名称：InMemoryRunner
[logging_plugin]    根代理：google_search_agent
[logging_plugin]    用户内容：text: 'recent papers on quantum computing'
[logging_plugin] 🏃 调用开始
[logging_plugin]    调用ID：e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    启动代理：google_search_agent
[logging_plugin] 🤖 代理启动
[logging_plugin]    代理名称：google_search_agent
[logging_plugin]    调用ID：e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin] 🧠 LLM请求
[logging_plugin]    模型：gemini-2.5-flash-lite
[logging_plugin]    代理：google_search_agent
[logging_plugin]    系统指令：'Use the google_search tool to find information on the given topic. Return the raw search results.

You are an agent. Your internal name is "google_search_agent". The description about you is "Searches...'
[logging_plugin] 🧠 LLM响应
[logging_plugin]    代理：google_search_agent
[logging_plugin]    内容：text: 'Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network t...'
[logging_plugin]    Token使用情况 - 输入：58，输出：445
[logging_plugin] 📢 事件生成
[logging_plugin]    事件ID：490f9e8e-6326-4f2e-8dff-7637fa55d86f
[logging_plugin]    作者：google_search_agent
[logging_plugin]    内容：text: 'Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network t...'
[logging_plugin]    最终响应：True
[logging_plugin] 🤖 代理完成
[logging_plugin]    代理名称：google_search_agent
[logging_plugin]    调用ID：e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin] ✅ 调用完成
[logging_plugin]    调用ID：e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    最终代理：google_search_agent
[logging_plugin] 🔧 工具完成
[logging_plugin]    工具名称：google_search_agent
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    函数调用ID：adk-02d3996c-1a40-4762-a773-6a22ae5b8622
[logging_plugin]    结果：Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network technologies and integrated photonics for trapped ions. There's also a growing focus on post-quantum ...}
[logging_plugin] 📢 事件生成
[logging_plugin]    事件ID：4f2999dc-2006-4fc1-840e-ad5604a76b12
[logging_plugin]    作者：research_paper_finder_agent
[logging_plugin]    内容：function_response: google_search_agent
[logging_plugin]    最终响应：False
[logging_plugin]    函数响应：['google_search_agent']
[logging_plugin] 🧠 LLM请求
[logging_plugin]    模型：gemini-2.5-flash-lite
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    系统指令：'Your task is to find research papers and count them.

       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'.
       2) Then, pas...'
[logging_plugin]    可用工具：['google_search_agent', 'count_papers_fixed']
[logging_plugin] 🧠 LLM响应
[logging_plugin]    代理：research_paper_finder_agent
[logging_plugin]    内容：None
[logging_plugin]    Token使用情况 - 输入：707，输出：None
[logging_plugin] 📢 事件生成
[logging_plugin]    事件ID：ff1b69b1-fc8f-4bf3-b314-5ac2f12a3250
[logging_plugin]    作者：research_paper_finder_agent
[logging_plugin]    内容：None
[logging_plugin]    最终响应：True
[logging_plugin] 🤖 代理完成
[logging_plugin]    代理名称：research_paper_finder_agent
[logging_plugin]    调用ID：e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin] ✅ 调用完成
[logging_plugin]    调用ID：e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    最终代理：research_paper_finder_agent

✅ 代理执行完成！

📋 关键观察：
• LoggingPlugin自动捕获了所有代理活动
• 日志包括：用户消息、代理响应、工具调用、计时数据
• 检查logger.log文件以获取详细的DEBUG日志
• 此方法可扩展用于生产系统

================================================================================
演示：自定义插件（CountInvocationPlugin）
================================================================================
🧹 清理了logger.log
✅ 日志记录已配置

🎯 使用自定义CountInvocationPlugin运行代理...
此插件计算代理调用次数和LLM请求次数


 ### 创建了新会话：debug_session_id

User > Find papers on machine learning
[CountPlugin] 代理调用 #1
[CountPlugin] LLM请求 #1
[CountPlugin] 代理调用 #2
[CountPlugin] LLM请求 #2
[CountPlugin] LLM请求 #3
[CountPlugin] LLM请求 #4
research_paper_finder_agent > 以下是13篇机器学习研究论文：

"A Few Useful Things to Know About Machine Learning" by Pedro Domingos (2012)
"ImageNet Classification with Deep Convolutional Neural Networks" by Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton (2012)
"Generative Adversarial Nets" by Ian Goodfellow et al. (2014)
"Sequence to Sequence Learning with Neural Networks" by Ilya Sutskever, Oriol Vinyals, and Quoc V. Le (2014)
"Deep Residual Learning for Image Recognition" by Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun (2015)
"Attention Is All You Need" by Ashish Vaswani et al. (2017)
"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" by Jacob Devlin et al. (2018)
Journal of Machine Learning Research (JMLR)
Google DeepMind Publications
arXiv
GitHub (ML-Papers-of-the-Week)
"Machine Learning: Models, Challenges, and Research Directions" (MDPI)
"Machine Learning: Algorithms, Real-World Applications and Research Directions" (PMC)

找到的论文总数为13。

📊 自定义插件统计：
   • 代理调用次数：2
   • LLM请求次数：4

💡 自定义插件允许您添加任何需要的可观测性逻辑！

================================================================================
总结
================================================================================

❓ 何时使用哪种类型的日志记录？
1. 开发调试 → 使用'adk web --log_level DEBUG'
2. 常见的生产环境可观测性 → 使用LoggingPlugin()
3. 自定义需求 → 构建自定义回调和插件

🎯 关键要点：
✅ 核心调试模式：症状 → 日志 → 根本原因 → 修复
✅ ADK Web UI提供带有跟踪的交互式调试
✅ LoggingPlugin自动处理标准可观测性
✅ 自定义插件支持专门的监控

📚 了解更多：
• ADK可观测性：https://google.github.io/adk-docs/observability/logging/
• 自定义插件：https://google.github.io/adk-docs/plugins/
• Cloud Trace集成：https://google.github.io/adk-docs/observability/cloud-trace/
