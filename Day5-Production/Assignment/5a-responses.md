✅ ADK components imported successfully.
✅ API key loaded from .env file

================================================================================
DAY 5A: AGENT2AGENT (A2A) COMMUNICATION
================================================================================

📚 What You'll Learn:
• Understanding the A2A protocol
• Exposing agents via A2A using to_a2a()
• Consuming remote agents using RemoteA2aAgent
• Building cross-organization agent systems

================================================================================
SECTION 1: Create Product Catalog Agent (To Be Exposed)
================================================================================
✅ Product Catalog Agent created successfully!
   Model: gemini-2.5-flash-lite
   Tool: get_product_info()
   Ready to be exposed via A2A...

================================================================================
SECTION 2 & 3: Expose via A2A and Start Server
================================================================================
📝 Product Catalog server code saved to /tmp/product_catalog_server.py

🚀 Starting Product Catalog Agent server...
   Waiting for server to be ready...
...
✅ Product Catalog Agent server is running!
   Server URL: http://localhost:8001
   Agent card: http://localhost:8001/.well-known/agent-card.json

📋 Product Catalog Agent Card:
{
  "capabilities": {},
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "description": "External vendor's product catalog agent that provides product information and availability.",
  "name": "product_catalog_agent",
  "preferredTransport": "JSONRPC",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "description": "External vendor's product catalog agent that provides product information and availability. \n    I am a product catalog specialist from an external vendor.\n    When asked about products, use the get_product_info tool to fetch data from the catalog.\n    Provide clear, accurate product information including price, availability, and specs.\n    If asked about multiple products, look up each one.\n    Be professional and helpful.\n    ",
      "id": "product_catalog_agent",
      "name": "model",
      "tags": [
        "llm"
      ]
    },
    {
      "description": "Get product information for a given product.",
      "id": "product_catalog_agent-get_product_info",
      "name": "get_product_info",
      "tags": [
        "llm",
        "tools"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": false,
  "url": "http://localhost:8001",
  "version": "0.0.1"
}

✨ Key Information:
   Name: product_catalog_agent
   Description: External vendor's product catalog agent that provides product information and availability.
   URL: http://localhost:8001
   Skills: 2 capabilities exposed

================================================================================
SECTION 4: Create Customer Support Agent (Consumer)
================================================================================
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/Day-5/day_5a_agent2agent_communication.py:273: UserWarning: [EXPERIMENTAL] RemoteA2aAgent: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  remote_product_catalog_agent = RemoteA2aAgent(

✅ Remote Product Catalog Agent proxy created!
   Connected to: http://localhost:8001
   Agent card: http://localhost:8001/.well-known/agent-card.json
   The Customer Support Agent can now use this like a local sub-agent!

✅ Customer Support Agent created!
   Model: gemini-2.5-flash-lite
   Sub-agents: 1 (remote Product Catalog Agent via A2A)
   Ready to help customers!

================================================================================
SECTION 5: Test A2A Communication
================================================================================

🧪 Testing A2A Communication...

👤 Customer: Can you tell me about the iPhone 15 Pro? Is it in stock?

🎧 Support Agent response:
------------------------------------------------------------
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/agents/remote_a2a_agent.py:379: UserWarning: [EXPERIMENTAL] convert_genai_part_to_a2a_part: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  converted_part = self._genai_part_converter(part)
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/a2a/converters/event_converter.py:239: UserWarning: [EXPERIMENTAL] convert_a2a_message_to_event: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  return convert_a2a_message_to_event(
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/venv/lib/python3.14/site-packages/google/adk/a2a/converters/event_converter.py:309: UserWarning: [EXPERIMENTAL] convert_a2a_part_to_genai_part: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  part = part_converter(a2a_part)
The iPhone 15 Pro is available for $999. We have low stock, with only 8 units remaining. It features a 128GB storage capacity and a titanium finish.
------------------------------------------------------------

👤 Customer: I'm looking for a laptop. Can you compare the Dell XPS 15 and MacBook Pro 14 for me?

🎧 Support Agent response:
------------------------------------------------------------
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
The Dell XPS 15 is priced at $1,299 and has 45 units in stock. It features a 15.6" display, 16GB of RAM, and a 512GB SSD.

The MacBook Pro 14" is priced at $1,999 and has 22 units in stock. It is equipped with an M3 Pro chip, 18GB of RAM, and a 512GB SSD.
------------------------------------------------------------

👤 Customer: Do you have the Sony WH-1000XM5 headphones? What's the price?

🎧 Support Agent response:
------------------------------------------------------------
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
The Sony WH-1000XM5 headphones are in stock and available for $399. They feature noise-canceling technology and a 30-hour battery life.
------------------------------------------------------------

================================================================================
CLEANUP
================================================================================

🛑 Stopping Product Catalog server...
✅ Server stopped

================================================================================
SUMMARY
================================================================================

🎯 Key Takeaways:
✅ A2A protocol enables cross-organization agent communication
✅ to_a2a() makes agents accessible with auto-generated agent cards
✅ RemoteA2aAgent consumes remote agents as local sub-agents
✅ Agent cards describe capabilities at /.well-known/agent-card.json

📊 A2A vs Local Sub-Agents:
Use A2A when:
   • Agents are in different codebases/organizations
   • Need cross-language/framework communication
   • Formal API contract required

Use Local Sub-Agents when:
   • Same codebase/internal to your team
   • Need low latency
   • Same language/framework

📚 Learn More:
• A2A Protocol: https://a2a-protocol.org/
• Exposing Agents: https://google.github.io/adk-docs/a2a/quickstart-exposing/
• Consuming Agents: https://google.github.io/adk-docs/a2a/quickstart-consuming/