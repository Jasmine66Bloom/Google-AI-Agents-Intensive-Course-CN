"""
Day 4b: Agent Evaluation

This notebook covers:
- Understanding what agent evaluation is and why it's important
- Creating test cases interactively in ADK web UI
- Running systematic evaluations with adk eval CLI
- Creating evaluation configuration files
- Understanding evaluation metrics (response_match_score and tool_trajectory_avg_score)
- Analyzing evaluation results

Copyright 2025 Google LLC.
Licensed under the Apache License, Version 2.0
"""

import os
import json
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

# ============================================================================
# Setup and Configuration
# ============================================================================

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found in environment variables")
    print("   Please make sure you have a .env file with GOOGLE_API_KEY set")
    exit(1)

print("✅ ADK components imported successfully.")
print("✅ API key loaded from .env file")

# ============================================================================
# Configure Retry Options
# ============================================================================

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# Section 2: Home Automation Agent
# ============================================================================


def set_device_status(location: str, device_id: str, status: str) -> dict:
    """Sets the status of a smart home device.

    Args:
        location: The room where the device is located.
        device_id: The unique identifier for the device.
        status: The desired status, either 'ON' or 'OFF'.

    Returns:
        A dictionary confirming the action.
    """
    print(f"Tool Call: Setting {device_id} in {location} to {status}")
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}.",
    }


def create_home_automation_agent():
    """
    Create a home automation agent with deliberate flaws for evaluation practice.

    This agent has intentional issues:
    - Overconfident instructions claiming to control ALL devices
    - Assumes it can control any device the user mentions
    - Doesn't validate if devices exist or are supported
    """

    root_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="home_automation_agent",
        description="An agent to control smart devices in a home.",
        instruction="""You are a home automation assistant. You control ALL smart devices in the house.

        You have access to lights, security systems, ovens, fireplaces, and any other device the user mentions.
        Always try to be helpful and control whatever device the user asks for.

        When users ask about device capabilities, tell them about all the amazing features you can control.""",
        tools=[set_device_status],
    )

    return root_agent


# ============================================================================
# Section 4: Creating Evaluation Configuration
# ============================================================================


def create_evaluation_config(output_dir: str = "."):
    """
    Create evaluation configuration file with pass/fail thresholds.

    Args:
        output_dir: Directory to write the config file
    """

    eval_config = {
        "criteria": {
            "tool_trajectory_avg_score": 1.0,  # Perfect tool usage required
            "response_match_score": 0.8,  # 80% text similarity threshold
        }
    }

    config_path = os.path.join(output_dir, "test_config.json")
    with open(config_path, "w") as f:
        json.dump(eval_config, f, indent=2)

    print("✅ Evaluation configuration created!")
    print(f"   Saved to: {config_path}")
    print("\n📊 Evaluation Criteria:")
    print("• tool_trajectory_avg_score: 1.0 - Requires exact tool usage match")
    print("• response_match_score: 0.8 - Requires 80% text similarity")
    print("\n🎯 What this evaluation will catch:")
    print("✅ Incorrect tool usage (wrong device, location, or status)")
    print("✅ Poor response quality and communication")
    print("✅ Deviations from expected behavior patterns")

    return config_path


# ============================================================================
# Section 4: Creating Test Cases
# ============================================================================


def create_evaluation_test_cases(output_dir: str = "."):
    """
    Create evaluation test cases file.

    This file contains multiple test scenarios with:
    - User prompts (what the user says)
    - Expected responses (what the agent should say)
    - Expected tool calls (which tools should be used and how)

    Args:
        output_dir: Directory to write the evalset file
    """

    test_cases = {
        "eval_set_id": "home_automation_integration_suite",
        "eval_cases": [
            {
                "eval_id": "living_room_light_on",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [
                                {
                                    "text": "Please turn on the floor lamp in the living room"
                                }
                            ]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "Successfully set the floor lamp in the living room to on."
                                }
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "living room",
                                        "device_id": "floor lamp",
                                        "status": "ON",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "eval_id": "kitchen_on_off_sequence",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [
                                {"text": "Switch on the main light in the kitchen."}
                            ]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "Successfully set the main light in the kitchen to on."
                                }
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "kitchen",
                                        "device_id": "main light",
                                        "status": "ON",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }

    evalset_path = os.path.join(output_dir, "integration.evalset.json")
    with open(evalset_path, "w") as f:
        json.dump(test_cases, f, indent=2)

    print("✅ Evaluation test cases created")
    print(f"   Saved to: {evalset_path}")
    print("\n🧪 Test scenarios:")
    for case in test_cases["eval_cases"]:
        user_msg = case["conversation"][0]["user_content"]["parts"][0]["text"]
        print(f"• {case['eval_id']}: {user_msg}")

    print("\n📊 Expected results:")
    print("• living_room_light_on: Should pass both criteria")
    print("• kitchen_on_off_sequence: Should pass both criteria")
    print(
        "\n💡 These test cases verify the agent uses correct tools with correct parameters"
    )

    return evalset_path


# ============================================================================
# Demonstration Functions
# ============================================================================


def demo_interactive_evaluation():
    """Demonstrate interactive evaluation workflow with ADK web UI"""
    print("\n" + "=" * 80)
    print("DEMO: Interactive Evaluation with ADK Web UI")
    print("=" * 80)

    print("\n📝 Interactive Evaluation Workflow:")
    print("\n1️⃣  CREATE TEST CASES:")
    print("   • Start ADK web UI: adk web")
    print("   • Have a conversation with your agent")
    print("   • Navigate to 'Eval' tab")
    print("   • Click 'Create Evaluation set' and name it")
    print("   • Add current session to the evaluation set")

    print("\n2️⃣  RUN EVALUATION:")
    print("   • In the Eval tab, check your test case")
    print("   • Click 'Run Evaluation' button")
    print("   • Review the metrics dialog (response_match and tool_trajectory)")
    print("   • Click 'Start' to run")

    print("\n3️⃣  ANALYZE RESULTS:")
    print("   • Green 'Pass': Agent behaved as expected")
    print("   • Red 'Fail': Agent deviated from expected behavior")
    print("   • Hover over results for detailed comparison")
    print("   • View actual vs expected responses and tool calls")

    print("\n📊 Understanding Evaluation Metrics:")
    print(
        "   • response_match_score: Measures text similarity (1.0 = perfect match)"
    )
    print(
        "   • tool_trajectory_avg_score: Measures correct tool usage (1.0 = perfect)"
    )

    print("\n💡 Benefits of Interactive Evaluation:")
    print("   ✅ Visual feedback on agent behavior")
    print("   ✅ Quick iteration during development")
    print("   ✅ Easy test case creation from real conversations")
    print("   ✅ Immediate comparison of actual vs expected")


def demo_systematic_evaluation():
    """Demonstrate systematic evaluation with CLI"""
    print("\n" + "=" * 80)
    print("DEMO: Systematic Evaluation with CLI")
    print("=" * 80)

    print("\n🎯 Why Systematic Evaluation?")
    print("   • Scale beyond manual testing")
    print("   • Automated regression detection")
    print("   • Batch testing multiple scenarios")
    print("   • CI/CD integration for production")

    # Create evaluation files
    print("\n📁 Creating evaluation files...")
    output_dir = "home_automation_agent"
    os.makedirs(output_dir, exist_ok=True)

    config_path = create_evaluation_config(output_dir)
    print()
    evalset_path = create_evaluation_test_cases(output_dir)

    print("\n🚀 Running Evaluation:")
    print(f"\n   Command: adk eval {output_dir} {evalset_path} \\")
    print(f"              --config_file_path={config_path} \\")
    print(f"              --print_detailed_results")

    print("\n📊 What the CLI Does:")
    print("   1. Loads your agent from the specified directory")
    print("   2. Runs each test case from the evalset")
    print("   3. Compares actual vs expected:")
    print("      • Final responses (text similarity)")
    print("      • Tool usage (function calls and parameters)")
    print("   4. Applies pass/fail thresholds from config")
    print("   5. Prints detailed results for each test")

    print("\n📈 Sample Output Analysis:")
    print("   Test Case: living_room_light_on")
    print("   ✅ tool_trajectory_avg_score: 1.0/1.0 (PASS)")
    print("   ❌ response_match_score: 0.45/0.80 (FAIL)")
    print("\n   Diagnosis:")
    print("   • Tool usage is perfect (correct tool, correct params)")
    print("   • Response quality needs improvement")
    print("   • Fix: Update agent instructions for consistent messaging")

    print("\n⚙️  To actually run the evaluation:")
    print(f"   1. Create agent: adk create home_automation_agent")
    print(f"   2. Copy agent definition to agent.py")
    print(f"   3. Run: adk eval home_automation_agent {evalset_path} \\")
    print(f"            --config_file_path={config_path} \\")
    print(f"            --print_detailed_results")


def demo_user_simulation():
    """Demonstrate advanced user simulation concepts"""
    print("\n" + "=" * 80)
    print("DEMO: User Simulation (Advanced)")
    print("=" * 80)

    print("\n🎯 The Limitation of Static Tests:")
    print("   • Fixed test cases only cover known scenarios")
    print("   • Real users are unpredictable and varied")
    print("   • Conversations take unexpected turns")
    print("   • Edge cases emerge in production")

    print("\n💡 User Simulation Solution:")
    print("   • Uses LLM to generate dynamic user prompts")
    print("   • Follows a ConversationScenario with goals")
    print("   • Adapts based on agent responses")
    print("   • Discovers edge cases automatically")

    print("\n📝 How It Works:")
    print("   1. Define a ConversationScenario:")
    print("      • User's overall goal")
    print("      • Conversation plan outline")
    print("   2. LLM acts as simulated user:")
    print("      • Generates realistic prompts")
    print("      • Maintains conversational context")
    print("      • Adapts to agent behavior")
    print("   3. Evaluation runs automatically:")
    print("      • Tests agent's adaptability")
    print("      • Uncovers unexpected failures")
    print("      • More comprehensive coverage")

    print("\n📚 Learn More:")
    print(
        "   • User Simulation Docs: https://google.github.io/adk-docs/evaluate/user-sim/"
    )
    print("   • Implement ConversationScenario for your agent")
    print("   • Test against dynamic, realistic conversations")


def demo_best_practices():
    """Share evaluation best practices"""
    print("\n" + "=" * 80)
    print("EVALUATION BEST PRACTICES")
    print("=" * 80)

    print("\n1️⃣  BUILD A COMPREHENSIVE TEST SUITE:")
    print("   • Happy path scenarios (basic functionality)")
    print("   • Edge cases (unusual requests)")
    print("   • Error handling (invalid inputs)")
    print("   • Multi-turn conversations")
    print("   • Ambiguous user intents")

    print("\n2️⃣  SET APPROPRIATE THRESHOLDS:")
    print("   • tool_trajectory_avg_score:")
    print("     - 1.0 for critical operations (safety, financial)")
    print("     - 0.8-0.9 for general functionality")
    print("   • response_match_score:")
    print("     - 0.9-1.0 for exact wording requirements")
    print("     - 0.7-0.8 for semantic equivalence")

    print("\n3️⃣  ITERATIVE IMPROVEMENT:")
    print("   • Run evaluations frequently during development")
    print("   • Add test cases when bugs are discovered")
    print("   • Update thresholds based on production needs")
    print("   • Monitor evaluation trends over time")

    print("\n4️⃣  PRODUCTION EVALUATION:")
    print("   • Integrate into CI/CD pipeline")
    print("   • Run before deployments")
    print("   • Track metrics over versions")
    print("   • Alert on regression detection")

    print("\n5️⃣  ADVANCED CRITERIA (with Google Cloud):")
    print("   • safety_v1: Detect harmful content")
    print("   • hallucinations_v1: Check factual accuracy")
    print("   • custom_criteria: Define domain-specific metrics")


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all evaluation demonstrations"""

    print("\n" + "=" * 80)
    print("DAY 4B: AGENT EVALUATION")
    print("=" * 80)

    print("\n📚 What You'll Learn:")
    print("• Creating test cases interactively in ADK web UI")
    print("• Running systematic evaluations with CLI")
    print("• Understanding evaluation metrics")
    print("• Analyzing and fixing evaluation failures")
    print("• Advanced user simulation concepts")

    # Demo 1: Interactive Evaluation
    demo_interactive_evaluation()

    # Demo 2: Systematic Evaluation
    demo_systematic_evaluation()

    # Demo 3: User Simulation
    demo_user_simulation()

    # Demo 4: Best Practices
    demo_best_practices()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\n🎯 Key Takeaways:")
    print("✅ Evaluation is proactive (vs observability is reactive)")
    print("✅ Test both tool usage AND response quality")
    print("✅ Use ADK web UI for development iteration")
    print("✅ Use CLI evaluation for systematic regression testing")
    print("✅ User simulation extends coverage beyond static tests")

    print("\n📊 Evaluation Workflow:")
    print("1. Create test cases (web UI or synthetic)")
    print("2. Define evaluation criteria (config file)")
    print("3. Run evaluations (adk eval CLI)")
    print("4. Analyze results (detailed output)")
    print("5. Fix issues and iterate")

    print("\n📚 Learn More:")
    print(
        "• ADK Evaluation: https://google.github.io/adk-docs/evaluate/"
    )
    print(
        "• Evaluation Criteria: https://google.github.io/adk-docs/evaluate/criteria/"
    )
    print(
        "• Pytest Integration: https://google.github.io/adk-docs/evaluate/#2-pytest-run-tests-programmatically"
    )
    print(
        "• User Simulation: https://google.github.io/adk-docs/evaluate/user-sim/"
    )

    print("\n🚀 Next Steps:")
    print("• Apply evaluation to your own agents")
    print("• Build comprehensive test suites")
    print("• Integrate into your development workflow")
    print("• Stay tuned for Day 5: Production Deployment!")


if __name__ == "__main__":
    main()
