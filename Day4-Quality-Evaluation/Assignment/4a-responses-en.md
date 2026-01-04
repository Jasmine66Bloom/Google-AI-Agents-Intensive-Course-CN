✅ ADK components imported successfully.
✅ API key loaded from .env file

================================================================================
DAY 4A: AGENT OBSERVABILITY
================================================================================

📚 What You'll Learn:
• Debugging agents with ADK web UI and DEBUG logs
• Using LoggingPlugin for production observability
• Creating custom plugins for specialized needs
• Understanding logs, traces, and metrics

================================================================================
DEMO: Broken Agent (for debugging practice)
================================================================================

🐛 This agent has an intentional bug in the count_papers tool
The tool expects a 'str' but should accept 'List[str]'

👉 In a real scenario, you would:
   1. Run 'adk web --log_level DEBUG' to start the web UI
   2. Test the agent with: 'Find latest quantum computing papers'
   3. Use the Events tab and Traces to find the bug
   4. Look at the function_call to see incorrect parameter types

⚠️  Note: This is a demo script. To actually debug:
   - Create an agent folder: adk create research-agent
   - Copy the agent definition to agent.py
   - Run: adk web --log_level DEBUG
   - Use the web UI to interact and debug

================================================================================
DEMO: Research Agent with LoggingPlugin
================================================================================
🧹 Cleaned up logger.log
✅ Logging configured

🚀 Running agent with LoggingPlugin...
📊 Watch the comprehensive logging output:


 ### Created new session: debug_session_id

User > Find recent papers on quantum computing
[logging_plugin] 🚀 USER MESSAGE RECEIVED
[logging_plugin]    Invocation ID: e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    Session ID: debug_session_id
[logging_plugin]    User ID: debug_user_id
[logging_plugin]    App Name: InMemoryRunner
[logging_plugin]    Root Agent: research_paper_finder_agent
[logging_plugin]    User Content: text: 'Find recent papers on quantum computing'
[logging_plugin] 🏃 INVOCATION STARTING
[logging_plugin]    Invocation ID: e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    Starting Agent: research_paper_finder_agent
[logging_plugin] 🤖 AGENT STARTING
[logging_plugin]    Agent Name: research_paper_finder_agent
[logging_plugin]    Invocation ID: e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin] 🧠 LLM REQUEST
[logging_plugin]    Model: gemini-2.5-flash-lite
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    System Instruction: 'Your task is to find research papers and count them.

       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'.
       2) Then, pas...'
[logging_plugin]    Available Tools: ['google_search_agent', 'count_papers_fixed']
[logging_plugin] 🧠 LLM RESPONSE
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    Content: function_call: google_search_agent
[logging_plugin]    Token Usage - Input: 250, Output: 21
[logging_plugin] 📢 EVENT YIELDED
[logging_plugin]    Event ID: 4c138c18-ae91-4454-8bd3-fa8aa44b644d
[logging_plugin]    Author: research_paper_finder_agent
[logging_plugin]    Content: function_call: google_search_agent
[logging_plugin]    Final Response: False
[logging_plugin]    Function Calls: ['google_search_agent']
[logging_plugin] 🔧 TOOL STARTING
[logging_plugin]    Tool Name: google_search_agent
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    Function Call ID: adk-02d3996c-1a40-4762-a773-6a22ae5b8622
[logging_plugin]    Arguments: {'request': 'recent papers on quantum computing'}
[logging_plugin] 🚀 USER MESSAGE RECEIVED
[logging_plugin]    Invocation ID: e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    Session ID: 418bb018-2cf7-4b2a-8918-1b8a19e01601
[logging_plugin]    User ID: debug_user_id
[logging_plugin]    App Name: InMemoryRunner
[logging_plugin]    Root Agent: google_search_agent
[logging_plugin]    User Content: text: 'recent papers on quantum computing'
[logging_plugin] 🏃 INVOCATION STARTING
[logging_plugin]    Invocation ID: e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    Starting Agent: google_search_agent
[logging_plugin] 🤖 AGENT STARTING
[logging_plugin]    Agent Name: google_search_agent
[logging_plugin]    Invocation ID: e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin] 🧠 LLM REQUEST
[logging_plugin]    Model: gemini-2.5-flash-lite
[logging_plugin]    Agent: google_search_agent
[logging_plugin]    System Instruction: 'Use the google_search tool to find information on the given topic. Return the raw search results.

You are an agent. Your internal name is "google_search_agent". The description about you is "Searches...'
[logging_plugin] 🧠 LLM RESPONSE
[logging_plugin]    Agent: google_search_agent
[logging_plugin]    Content: text: 'Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network t...'
[logging_plugin]    Token Usage - Input: 58, Output: 445
[logging_plugin] 📢 EVENT YIELDED
[logging_plugin]    Event ID: 490f9e8e-6326-4f2e-8dff-7637fa55d86f
[logging_plugin]    Author: google_search_agent
[logging_plugin]    Content: text: 'Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network t...'
[logging_plugin]    Final Response: True
[logging_plugin] 🤖 AGENT COMPLETED
[logging_plugin]    Agent Name: google_search_agent
[logging_plugin]    Invocation ID: e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin] ✅ INVOCATION COMPLETED
[logging_plugin]    Invocation ID: e-666dab78-f4e6-4ae7-8eb3-4b827ea525de
[logging_plugin]    Final Agent: google_search_agent
[logging_plugin] 🔧 TOOL COMPLETED
[logging_plugin]    Tool Name: google_search_agent
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    Function Call ID: adk-02d3996c-1a40-4762-a773-6a22ae5b8622
[logging_plugin]    Result: Recent papers on quantum computing highlight significant advancements in hardware, algorithms, and applications. Key developments include breakthroughs in quantum hardware with new hypercube network technologies and integrated photonics for trapped ions. There's also a growing focus on post-quantum ...}
[logging_plugin] 📢 EVENT YIELDED
[logging_plugin]    Event ID: 4f2999dc-2006-4fc1-840e-ad5604a76b12
[logging_plugin]    Author: research_paper_finder_agent
[logging_plugin]    Content: function_response: google_search_agent
[logging_plugin]    Final Response: False
[logging_plugin]    Function Responses: ['google_search_agent']
[logging_plugin] 🧠 LLM REQUEST
[logging_plugin]    Model: gemini-2.5-flash-lite
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    System Instruction: 'Your task is to find research papers and count them.

       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'.
       2) Then, pas...'
[logging_plugin]    Available Tools: ['google_search_agent', 'count_papers_fixed']
[logging_plugin] 🧠 LLM RESPONSE
[logging_plugin]    Agent: research_paper_finder_agent
[logging_plugin]    Content: None
[logging_plugin]    Token Usage - Input: 707, Output: None
[logging_plugin] 📢 EVENT YIELDED
[logging_plugin]    Event ID: ff1b69b1-fc8f-4bf3-b314-5ac2f12a3250
[logging_plugin]    Author: research_paper_finder_agent
[logging_plugin]    Content: None
[logging_plugin]    Final Response: True
[logging_plugin] 🤖 AGENT COMPLETED
[logging_plugin]    Agent Name: research_paper_finder_agent
[logging_plugin]    Invocation ID: e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin] ✅ INVOCATION COMPLETED
[logging_plugin]    Invocation ID: e-48f81f74-225f-46e5-8161-178223400d82
[logging_plugin]    Final Agent: research_paper_finder_agent

✅ Agent execution complete!

📋 Key Observations:
• LoggingPlugin automatically captured all agent activity
• Logs include: user messages, agent responses, tool calls, timing data
• Check logger.log file for detailed DEBUG logs
• This approach scales for production systems

================================================================================
DEMO: Custom Plugin (CountInvocationPlugin)
================================================================================
🧹 Cleaned up logger.log
✅ Logging configured

🎯 Running agent with custom CountInvocationPlugin...
This plugin counts agent invocations and LLM requests


 ### Created new session: debug_session_id

User > Find papers on machine learning
[CountPlugin] Agent invocation #1
[CountPlugin] LLM request #1
[CountPlugin] Agent invocation #2
[CountPlugin] LLM request #2
[CountPlugin] LLM request #3
[CountPlugin] LLM request #4
research_paper_finder_agent > Here are 13 research papers on machine learning:

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

The total number of papers found is 13.

📊 Custom Plugin Statistics:
   • Agent invocations: 2
   • LLM requests: 4

💡 Custom plugins allow you to add any observability logic you need!

================================================================================
SUMMARY
================================================================================

❓ When to use which type of logging?
1. Development debugging → Use 'adk web --log_level DEBUG'
2. Common production observability → Use LoggingPlugin()
3. Custom requirements → Build Custom Callbacks and Plugins

🎯 Key Takeaways:
✅ Core debugging pattern: symptom → logs → root cause → fix
✅ ADK web UI provides interactive debugging with traces
✅ LoggingPlugin handles standard observability automatically
✅ Custom plugins enable specialized monitoring

📚 Learn More:
• ADK Observability: https://google.github.io/adk-docs/observability/logging/
• Custom Plugins: https://google.github.io/adk-docs/plugins/
• Cloud Trace Integration: https://google.github.io/adk-docs/observability/cloud-trace/