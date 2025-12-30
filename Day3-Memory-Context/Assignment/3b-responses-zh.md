✅ ADK 组件导入成功。
✅ API 密钥已从 .env 文件加载
✅ 辅助函数已定义。

================================================================================
第 3 部分：初始化 MemoryService
================================================================================
✅ 已创建支持记忆功能的 Agent 和 Runner！

================================================================================
第 4 部分：将会话数据导入记忆
================================================================================

### 会话：conversation-01

用户 > 我最喜欢的颜色是蓝绿色。你能写一首关于它的俳句吗？
模型 > 闪烁的色调，
海洋深处和森林绿，
平静而安宁的色调。

📝 会话包含：
  user: My favorite color is blue-green. Can you write a Haiku about...
  model: A shimmering hue,
Ocean depths and forest green,
Calm and pe...

✅ 会话已添加到记忆中！

================================================================================
第 5 部分：在您的 Agent 中启用记忆检索
================================================================================
✅ 已创建带有 load_memory 工具的 Agent。

### 会话：color-test

用户 > 我最喜欢的颜色是什么？
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
模型 > 你最喜欢的颜色是蓝绿色。

--- 完整的手动工作流测试 ---

### 会话：birthday-session-01

用户 > 我的生日是 3 月 15 日。
模型 > 好的，我会记住你的生日是 3 月 15 日。

✅ 生日会话已保存到记忆中！

### 会话：birthday-session-02

用户 > 我的生日是什么时候？
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
模型 > 你的生日是 3 月 15 日。

--- 手动记忆搜索 ---

🔍 搜索结果：
  找到 3 条相关记忆

  [user]: My favorite color is blue-green. Can you write a Haiku about it?...
  [user]: My birthday is on March 15th....
  [MemoryDemoAgent]: Okay, I will remember that your birthday is on March 15th....

================================================================================
第 6 部分：自动化记忆存储
================================================================================
✅ 已创建具有自动记忆保存功能的 Agent！

### 会话：auto-save-test

用户 > 我在我侄子 1 岁生日时送了他一个新玩具！
模型 > 太棒了！第一个生日是一个特别的里程碑。希望你的侄子喜欢他的新玩具！

### 会话：auto-save-test-2

用户 > 我送了我侄子什么？
模型 > 你送了你侄子一个新玩具。
