"""
生产天气助手代理

此代理使用模拟数据库为城市提供天气信息。
在生产环境中，这将与真实的天气 API 集成。
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os

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
    model=LiteLlm(
        model="volcengine/doubao-1-5-lite-32k-250115",
        api_key=os.environ.get("DOUBAO_API_KEY")
    ),
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
