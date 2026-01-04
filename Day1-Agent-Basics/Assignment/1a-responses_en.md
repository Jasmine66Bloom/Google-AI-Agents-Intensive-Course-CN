
============================================================
Day 1a: From Prompt to Action
Building Your First AI Agent
============================================================

✅ Gemini API key loaded from .env file.
✅ Agent created with Google Search tool.

--- Example 1: Asking about Agent Development Kit ---

============================================================
Query: What is Agent Development Kit from Google? What languages is the SDK available in?
============================================================


 ### Created new session: debug_session_id

User > What is Agent Development Kit from Google? What languages is the SDK available in?
helpful_assistant > The Agent Development Kit (ADK) from Google is a flexible, modular, and open-source framework designed to simplify the development, deployment, and orchestration of AI agents and multi-agent systems. It applies software development principles to AI agent creation, making it feel more like traditional software development. ADK is optimized for the Gemini models and the Google ecosystem but is model-agnostic and deployment-agnostic, allowing compatibility with other frameworks.

The ADK allows developers to define agent logic, tools, and orchestration directly in code, providing flexibility, robust debugging, and reliable versioning. It supports building modular multi-agent systems where specialized agents can be composed into flexible hierarchies. The framework also offers a rich tool ecosystem, allowing agents to utilize pre-built tools, custom functions, OpenAPI specifications, and integrate with third-party libraries or even other agents.

The Agent Development Kit is available in the following SDK languages:
*   **Python**
*   **Java**
*   **Go**

============================================================
Response received!
============================================================


--- Example 2: Asking for current information ---

============================================================
Query: What's the weather in London?
============================================================


 ### Created new session: debug_session_id

User > What's the weather in London?
helpful_assistant > The weather in London is currently light rain, with a temperature of 59°F (15°C). The humidity is around 77%. There is a 55% chance of rain. It feels like 57°F (14°C).

Looking ahead, the forecast for today includes cloudy conditions during the day and light rain at night, with an 85% chance of rain at night. For Wednesday, expect cloudy weather both day and night with a 45% chance of rain during the day.

============================================================
Response received!
============================================================


--- Example 3: Try your own query ---

Enter your question (or press Enter to skip): what was the score of last night's monday night football game? 

============================================================
Query: what was the score of last night's monday night football game?
============================================================


 ### Created new session: debug_session_id

User > what was the score of last night's monday night football game?
helpful_assistant > The score of last night's Monday Night Football game was Eagles 10, Packers 7. It was a defensive battle that ended with a narrow victory for the Eagles. The first half ended in a 0-0 stalemate, which was the first scoreless first half of Monday Night Football since 2009. The Eagles scored their first points with a field goal in the third quarter, and extended their lead to 10-0 in the fourth quarter with a touchdown pass from Jalen Hurts to DeVonta Smith. The Packers responded with a touchdown run from Josh Jacobs, but were unable to overcome the deficit.

============================================================
Response received!
============================================================


============================================================
✅ All examples completed!
============================================================

Key Takeaways:
- The agent doesn't just respond—it REASONS and ACTS
- It knows when to use tools like Google Search
- It can provide up-to-date information

Next: Check out day_1b_agent_architectures.py for multi-agent systems!