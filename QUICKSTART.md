# 快速入门指南

通过3个简单步骤开始使用AI智能体课程！

## 步骤1：运行设置脚本

```bash
./setup.sh
```

这将自动：
- 创建Python虚拟环境
- 安装所有必需的包（google-adk、python-dotenv等）
- 创建.env文件模板

## 步骤2：添加您的API密钥

1. 从[Google AI Studio](https://aistudio.google.com/app/api-keys)获取您的API密钥

2. 在编辑器中打开`.env`文件：
   ```bash
   nano .env
   # 或使用您喜欢的编辑器：code .env、vim .env等
   ```

3. 将`your-api-key-here`替换为您的实际API密钥：
   ```
   GOOGLE_API_KEY=AIzaSyC_your_actual_key_here
   ```

4. 保存并关闭文件

## 步骤3：运行您的第一个智能体

```bash
# 确保虚拟环境已激活
# 您应该在终端提示符中看到(venv)
source venv/bin/activate

# 导航到Day-1文件夹
cd Day-1

# 运行第一个脚本
python day_1a_prompt_to_action.py
```

## 接下来做什么？

完成第一个脚本后，尝试：

```bash
# 运行多智能体架构脚本
python day_1b_agent_architectures.py
```

## 需要帮助？

- 查看[Day-1/README.md](Day-1/README.md)以获取详细说明
- 确保在运行脚本之前在终端中看到`(venv)`
- 如果遇到错误，请参阅README中的故障排除部分

## 停用虚拟环境

完成后：

```bash
deactivate
```

这将使您返回到系统Python环境。

---

**注意：** 包含您的API密钥的`.env`文件受`.gitignore`保护，永远不会提交到git！
