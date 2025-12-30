✅ ADK components imported successfully.
✅ API key loaded from .env file

================================================================================
DAY 4B: AGENT EVALUATION
================================================================================

📚 What You'll Learn:
• Creating test cases interactively in ADK web UI
• Running systematic evaluations with CLI
• Understanding evaluation metrics
• Analyzing and fixing evaluation failures
• Advanced user simulation concepts

================================================================================
DEMO: Interactive Evaluation with ADK Web UI
================================================================================

📝 Interactive Evaluation Workflow:

1️⃣  CREATE TEST CASES:
   • Start ADK web UI: adk web
   • Have a conversation with your agent
   • Navigate to 'Eval' tab
   • Click 'Create Evaluation set' and name it
   • Add current session to the evaluation set

2️⃣  RUN EVALUATION:
   • In the Eval tab, check your test case
   • Click 'Run Evaluation' button
   • Review the metrics dialog (response_match and tool_trajectory)
   • Click 'Start' to run

3️⃣  ANALYZE RESULTS:
   • Green 'Pass': Agent behaved as expected
   • Red 'Fail': Agent deviated from expected behavior
   • Hover over results for detailed comparison
   • View actual vs expected responses and tool calls

📊 Understanding Evaluation Metrics:
   • response_match_score: Measures text similarity (1.0 = perfect match)
   • tool_trajectory_avg_score: Measures correct tool usage (1.0 = perfect)

💡 Benefits of Interactive Evaluation:
   ✅ Visual feedback on agent behavior
   ✅ Quick iteration during development
   ✅ Easy test case creation from real conversations
   ✅ Immediate comparison of actual vs expected

================================================================================
DEMO: Systematic Evaluation with CLI
================================================================================

🎯 Why Systematic Evaluation?
   • Scale beyond manual testing
   • Automated regression detection
   • Batch testing multiple scenarios
   • CI/CD integration for production

📁 Creating evaluation files...
✅ Evaluation configuration created!
   Saved to: home_automation_agent/test_config.json

📊 Evaluation Criteria:
• tool_trajectory_avg_score: 1.0 - Requires exact tool usage match
• response_match_score: 0.8 - Requires 80% text similarity

🎯 What this evaluation will catch:
✅ Incorrect tool usage (wrong device, location, or status)
✅ Poor response quality and communication
✅ Deviations from expected behavior patterns

✅ Evaluation test cases created
   Saved to: home_automation_agent/integration.evalset.json

🧪 Test scenarios:
• living_room_light_on: Please turn on the floor lamp in the living room
• kitchen_on_off_sequence: Switch on the main light in the kitchen.

📊 Expected results:
• living_room_light_on: Should pass both criteria
• kitchen_on_off_sequence: Should pass both criteria

💡 These test cases verify the agent uses correct tools with correct parameters

🚀 Running Evaluation:

   Command: adk eval home_automation_agent home_automation_agent/integration.evalset.json \
              --config_file_path=home_automation_agent/test_config.json \
              --print_detailed_results

📊 What the CLI Does:
   1. Loads your agent from the specified directory
   2. Runs each test case from the evalset
   3. Compares actual vs expected:
      • Final responses (text similarity)
      • Tool usage (function calls and parameters)
   4. Applies pass/fail thresholds from config
   5. Prints detailed results for each test

📈 Sample Output Analysis:
   Test Case: living_room_light_on
   ✅ tool_trajectory_avg_score: 1.0/1.0 (PASS)
   ❌ response_match_score: 0.45/0.80 (FAIL)

   Diagnosis:
   • Tool usage is perfect (correct tool, correct params)
   • Response quality needs improvement
   • Fix: Update agent instructions for consistent messaging

⚙️  To actually run the evaluation:
   1. Create agent: adk create home_automation_agent
   2. Copy agent definition to agent.py
   3. Run: adk eval home_automation_agent home_automation_agent/integration.evalset.json \
            --config_file_path=home_automation_agent/test_config.json \
            --print_detailed_results

================================================================================
DEMO: User Simulation (Advanced)
================================================================================

🎯 The Limitation of Static Tests:
   • Fixed test cases only cover known scenarios
   • Real users are unpredictable and varied
   • Conversations take unexpected turns
   • Edge cases emerge in production

💡 User Simulation Solution:
   • Uses LLM to generate dynamic user prompts
   • Follows a ConversationScenario with goals
   • Adapts based on agent responses
   • Discovers edge cases automatically

📝 How It Works:
   1. Define a ConversationScenario:
      • User's overall goal
      • Conversation plan outline
   2. LLM acts as simulated user:
      • Generates realistic prompts
      • Maintains conversational context
      • Adapts to agent behavior
   3. Evaluation runs automatically:
      • Tests agent's adaptability
      • Uncovers unexpected failures
      • More comprehensive coverage

📚 Learn More:
   • User Simulation Docs: https://google.github.io/adk-docs/evaluate/user-sim/
   • Implement ConversationScenario for your agent
   • Test against dynamic, realistic conversations

================================================================================
EVALUATION BEST PRACTICES
================================================================================

1️⃣  BUILD A COMPREHENSIVE TEST SUITE:
   • Happy path scenarios (basic functionality)
   • Edge cases (unusual requests)
   • Error handling (invalid inputs)
   • Multi-turn conversations
   • Ambiguous user intents

2️⃣  SET APPROPRIATE THRESHOLDS:
   • tool_trajectory_avg_score:
     - 1.0 for critical operations (safety, financial)
     - 0.8-0.9 for general functionality
   • response_match_score:
     - 0.9-1.0 for exact wording requirements
     - 0.7-0.8 for semantic equivalence

3️⃣  ITERATIVE IMPROVEMENT:
   • Run evaluations frequently during development
   • Add test cases when bugs are discovered
   • Update thresholds based on production needs
   • Monitor evaluation trends over time

4️⃣  PRODUCTION EVALUATION:
   • Integrate into CI/CD pipeline
   • Run before deployments
   • Track metrics over versions
   • Alert on regression detection

5️⃣  ADVANCED CRITERIA (with Google Cloud):
   • safety_v1: Detect harmful content
   • hallucinations_v1: Check factual accuracy
   • custom_criteria: Define domain-specific metrics

================================================================================
SUMMARY
================================================================================

🎯 Key Takeaways:
✅ Evaluation is proactive (vs observability is reactive)
✅ Test both tool usage AND response quality
✅ Use ADK web UI for development iteration
✅ Use CLI evaluation for systematic regression testing
✅ User simulation extends coverage beyond static tests

📊 Evaluation Workflow:
1. Create test cases (web UI or synthetic)
2. Define evaluation criteria (config file)
3. Run evaluations (adk eval CLI)
4. Analyze results (detailed output)
5. Fix issues and iterate

📚 Learn More:
• ADK Evaluation: https://google.github.io/adk-docs/evaluate/
• Evaluation Criteria: https://google.github.io/adk-docs/evaluate/criteria/
• Pytest Integration: https://google.github.io/adk-docs/evaluate/#2-pytest-run-tests-programmatically
• User Simulation: https://google.github.io/adk-docs/evaluate/user-sim/

🚀 Next Steps:
• Apply evaluation to your own agents
• Build comprehensive test suites
• Integrate into your development workflow
• Stay tuned for Day 5: Production Deployment!