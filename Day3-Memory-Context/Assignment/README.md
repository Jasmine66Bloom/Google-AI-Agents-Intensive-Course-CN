# Day 3 - Memory Management & Context Engineering

This folder contains Python scripts based on the Day 3 Jupyter notebooks from the Kaggle 5-day Agents course.

## Scripts Overview

### 1. `day_3a_agent_sessions.py`
**Memory Management Part 1 - Sessions**

This script demonstrates:
- What sessions are and how to use them in agents
- Building stateful agents with sessions and events
- Persisting sessions in a database (SQLite)
- Context compaction to manage conversation history
- Session state management for sharing data within conversations

**Key Concepts:**
- **Sessions**: Containers for single, continuous conversations
- **Events**: Building blocks of conversations (user input, agent responses, tool calls)
- **Session State**: Key-value storage for dynamic details during conversation
- **Persistence**: Surviving restarts with DatabaseSessionService
- **Context Compaction**: Automatically summarizing conversation history

**Example Use Cases:**
- Chatbots that remember conversation context
- Multi-turn interactions requiring state
- Reducing token costs with automatic summarization
- Sharing user preferences within a session

### 2. `day_3b_agent_memory.py`
**Memory Management Part 2 - Long-Term Memory**

This script demonstrates:
- Initializing MemoryService for long-term knowledge storage
- Transferring session data to persistent memory
- Searching and retrieving memories across sessions
- Automating memory storage with callbacks
- Understanding memory consolidation concepts

**Key Concepts:**
- **Memory vs Session**: Session = short-term (single conversation), Memory = long-term (across conversations)
- **Memory Retrieval**: load_memory (reactive) vs preload_memory (proactive)
- **Cross-Conversation Recall**: Access information from any past conversation
- **Callbacks**: Automate memory storage after each agent turn
- **Memory Consolidation**: Extract key facts from verbose conversations

**Example Use Cases:**
- Personal assistants remembering user preferences long-term
- Customer support agents recalling past interactions
- Knowledge accumulation across multiple conversations
- Personalized experiences based on historical data

## Prerequisites

Make sure you've completed the setup from the project root:

```bash
# From the project root directory
source venv/bin/activate  # Activate virtual environment
```

If you haven't set up the project yet, run:

```bash
cd ..  # Go to project root
./setup.sh
source venv/bin/activate
```

## Running the Scripts

### Run Script 3a (Sessions)

```bash
# Make sure you're in the Day-3 directory and venv is activated
python day_3a_agent_sessions.py
```

**What it does:**
1. **Section 2**: Creates a stateful agent with InMemorySessionService
   - Demonstrates conversation memory within a session
   - Shows how context is maintained across turns

2. **Section 3**: Upgrades to DatabaseSessionService (SQLite)
   - Persists conversations to disk
   - Demonstrates resuming sessions after restart
   - Shows session isolation (separate sessions don't share data)

3. **Section 4**: Implements Context Compaction
   - Automatically summarizes long conversations
   - Reduces token costs and improves performance
   - Demonstrates finding compaction events in history

4. **Section 5**: Working with Session State
   - Custom tools to save/retrieve user information
   - Demonstrates state persistence within sessions
   - Shows cross-session state sharing

### Run Script 3b (Memory)

```bash
python day_3b_agent_memory.py
```

**What it does:**
1. **Section 3**: Initializes MemoryService
   - Sets up both SessionService and MemoryService
   - Creates an agent with memory support

2. **Section 4**: Ingests Session Data into Memory
   - Has a conversation and saves it to memory
   - Demonstrates manual `add_session_to_memory()` call
   - Verifies session data was transferred

3. **Section 5**: Enables Memory Retrieval
   - Adds `load_memory` tool for reactive retrieval
   - Tests cross-session memory recall
   - Demonstrates manual memory search from code

4. **Section 6**: Automates Memory Storage
   - Uses callbacks for automatic memory saving
   - Implements `preload_memory` for proactive retrieval
   - Shows zero-manual-intervention memory management

## Understanding the Output

### Day 3a Output

**Session Creation and Management:**
```
✅ Stateful agent initialized!
   - Application: default
   - User: default
   - Using: InMemorySessionService

### Session: stateful-agentic-session
User > Hi, I am Sam! What is the capital of United States?
gemini-2.5-flash-lite > Hi Sam! The capital is Washington, D.C.

User > Hello! What is my name?
gemini-2.5-flash-lite > Your name is Sam.
```

**Database Persistence:**
- Creates `my_agent_data.db` SQLite file
- Stores all session events with timestamps
- Enables session resumption after restart

**Context Compaction:**
- Triggers after configured number of turns (e.g., every 3)
- Replaces verbose history with concise summary
- Shows compaction event in session history

**Session State:**
```
Session State Contents:
{'user:name': 'Sam', 'user:country': 'Poland'}

🔍 Notice the 'user:name' and 'user:country' keys storing our data!
```

### Day 3b Output

**Memory Initialization:**
```
✅ Agent and Runner created with memory support!
```

**Session Ingestion:**
```
📝 Session contains:
  user: My favorite color is blue-green...
  model: A tranquil blend, Ocean's calm...

✅ Session added to memory!
```

**Cross-Session Retrieval:**
```
### Session: birthday-session-02
User > When is my birthday?
Model: > Your birthday is on March 15th.
```
(Notice: Different session ID, but agent still remembers!)

**Automatic Memory:**
```
✅ Agent created with automatic memory saving!

# First conversation
User > I gifted a new toy to my nephew...

# Second conversation (NEW session)
User > What did I gift my nephew?
Model: > You gifted your nephew a new toy on his 1st birthday.
```

## Key Patterns and When to Use Them

### Session Types

| Service | Persistence | Use Case |
|---------|-------------|----------|
| **InMemorySessionService** | ❌ Lost on restart | Quick prototypes, testing |
| **DatabaseSessionService** | ✅ Survives restarts | Small to medium apps, local development |
| **Agent Engine Sessions** | ✅ Fully managed (GCP) | Enterprise scale, production |

### Memory Retrieval Strategies

**load_memory (Reactive)**
```python
agent = LlmAgent(
    tools=[load_memory],  # Agent decides when to search
)
```
**When to use:**
- Want to save tokens (only searches when needed)
- Agent can reason about when memory is relevant
- Most queries don't need historical context

**preload_memory (Proactive)**
```python
agent = LlmAgent(
    tools=[preload_memory],  # Always loads before each turn
)
```
**When to use:**
- Memory is always relevant (e.g., personal assistants)
- Want guaranteed context availability
- Willing to trade efficiency for reliability

### Context Compaction

**When to use:**
```python
app = App(
    name="my_app",
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compact every 3 turns
        overlap_size=1,         # Keep 1 previous turn for context
    ),
)
```

**Benefits:**
- Reduces token costs (20-80% reduction possible)
- Improves performance (less context to process)
- Maintains conversation continuity
- Focuses on important information

**Best for:**
- Long conversations (10+ turns)
- Repetitive interactions
- Information-dense dialogs

### Automatic Memory Storage

**Using Callbacks:**
```python
async def auto_save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    after_agent_callback=auto_save_to_memory,  # Saves after each turn
    tools=[preload_memory],
)
```

**When to use:**
- Every conversation should be remembered
- Want zero-manual-intervention memory
- Building production personal assistants
- Customer support systems

## Session State vs Memory

| Feature | Session State | Memory |
|---------|---------------|--------|
| **Scope** | Single session | Across all sessions |
| **Storage** | Key-value pairs | Structured memories |
| **Access** | `tool_context.state` | `load_memory` / `preload_memory` |
| **Persistence** | Depends on SessionService | Always persistent |
| **Best For** | Temporary workflow data | Long-term facts and preferences |

**Example:**
```python
# Session State - temporary, single conversation
tool_context.state["user:current_order_id"] = "12345"

# Memory - long-term, across conversations
await memory_service.add_session_to_memory(session)  # Stores facts
```

## Common Issues and Solutions

### Issue: Sessions don't persist after restart
**Solution:**
- Use `DatabaseSessionService` instead of `InMemorySessionService`
- Check that database file path is accessible
- Verify database file isn't deleted between runs

```python
# Instead of:
session_service = InMemorySessionService()

# Use:
session_service = DatabaseSessionService(db_url="sqlite:///my_data.db")
```

### Issue: Agent doesn't remember across sessions
**Solution:**
- Make sure you're calling `add_session_to_memory()`
- Verify `memory_service` is passed to Runner
- Add `load_memory` or `preload_memory` to agent tools

```python
# Must have BOTH:
runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,  # Required!
)

# AND:
agent = LlmAgent(
    tools=[load_memory],  # Or preload_memory
)
```

### Issue: Context compaction not happening
**Solution:**
- Use `App` with `events_compaction_config`, not just raw Agent
- Pass `app=` to Runner (not `agent=`)
- Check `compaction_interval` matches your turn count

```python
# Must use App, not Agent directly:
app = App(
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,
    ),
)

runner = Runner(app=app, ...)  # Use app=, not agent=
```

### Issue: Session state not shared across sessions
**Solution:**
- This is expected behavior! Session state is session-scoped
- For cross-session sharing, use Memory instead
- Or use user-scoped prefixes: `user:` in state keys

```python
# Session-scoped (isolated):
tool_context.state["temp:order"] = "12345"

# User-scoped (shared across sessions):
tool_context.state["user:preference"] = "dark_mode"
```

### Issue: Memory retrieval returns too many/few results
**Solution:**
- With InMemoryMemoryService: Use exact keywords
- Refine search queries to be more specific
- In production, use VertexAiMemoryBankService for semantic search

```python
# Less effective (vague):
search_memory(query="what color")

# More effective (specific):
search_memory(query="user's favorite color preference")
```

## Memory Consolidation (Advanced)

**What is Consolidation?**

Instead of storing raw conversation events, consolidation extracts key facts:

**Before (Raw Storage):**
```
User: "My favorite color is BlueGreen. I also like purple.
       Actually, I prefer BlueGreen most of the time."
Agent: "Great! I'll remember that."
User: "Thanks!"
Agent: "You're welcome!"

→ Stores ALL 4 messages (redundant, verbose)
```

**After (Consolidation):**
```
Extracted Memory: "User's favorite color: BlueGreen"

→ Stores 1 concise fact
```

**Note:** `InMemoryMemoryService` doesn't consolidate. For production consolidation, use **Vertex AI Memory Bank** (covered in Day 5).

## Learning Resources

### ADK Documentation
- [ADK Sessions](https://google.github.io/adk-docs/sessions/)
- [ADK Memory](https://google.github.io/adk-docs/sessions/memory/)
- [Context Compaction](https://google.github.io/adk-docs/context/compaction/)
- [Context Caching](https://google.github.io/adk-docs/context/caching/)
- [ADK Callbacks](https://google.github.io/adk-docs/agents/callbacks/)

### Google Cloud Documentation
- [Vertex AI Memory Bank Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview)
- [Memory Consolidation Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/generate-memories)

### Medium Articles
- [Manage Context Efficiently with Artifacts](https://medium.com/google-cloud/2-minute-adk-manage-context-efficiently-with-artifacts-6fcc6683d274)

## Best Practices

### Session Management

1. **Choose the Right SessionService**
   - Development: `InMemorySessionService`
   - Production: `DatabaseSessionService` or managed cloud services

2. **Session ID Naming**
   - Use meaningful IDs: `user_123_chat_2025_01_15`
   - Include user identifier for multi-user apps
   - Consider including timestamps for temporal organization

3. **Session Lifecycle**
   - Create sessions explicitly when starting conversations
   - Clean up old sessions periodically (for DatabaseSessionService)
   - Set retention policies based on privacy requirements

### Memory Management

1. **When to Save to Memory**
   - After important milestones in conversation
   - When user explicitly provides preferences/facts
   - Use callbacks for automatic saving in production

2. **Memory Search Best Practices**
   - Be specific in search queries
   - Use `preload_memory` for high-recall scenarios
   - Use `load_memory` to save costs when memory isn't always needed

3. **Memory Hygiene**
   - Periodically review stored memories for accuracy
   - Implement memory deletion for user privacy (GDPR compliance)
   - Consider memory expiration policies

### Context Engineering

1. **Compaction Configuration**
   - Start with `compaction_interval=5` and adjust based on use case
   - Keep `overlap_size=1-2` to maintain conversation flow
   - Monitor token savings vs context quality

2. **State Management**
   - Use consistent prefixes: `user:`, `temp:`, `app:`
   - Document state schema for your application
   - Clean up temporary state when workflows complete

3. **Error Handling**
   ```python
   try:
       session = await session_service.get_session(...)
   except Exception as e:
       # Create new session if not found
       session = await session_service.create_session(...)
   ```

## Architecture Patterns

### Pattern 1: Stateless Agent (Simple)
```python
# No sessions, no memory - each call is independent
agent = LlmAgent(...)
result = agent.run(query="What's the weather?")
```
**Use for:** One-off queries, stateless APIs

### Pattern 2: Session-Only Agent (Medium)
```python
# Sessions for conversation context, no long-term memory
runner = Runner(
    agent=agent,
    session_service=InMemorySessionService(),
)
```
**Use for:** Single-conversation chatbots, temporary support

### Pattern 3: Full Memory Agent (Advanced)
```python
# Sessions + Memory + Compaction
app = App(
    root_agent=LlmAgent(
        tools=[preload_memory],
        after_agent_callback=auto_save_to_memory,
    ),
    events_compaction_config=EventsCompactionConfig(...),
)

runner = Runner(
    app=app,
    session_service=DatabaseSessionService(...),
    memory_service=memory_service,
)
```
**Use for:** Personal assistants, long-term customer relationships

## Database Management

### SQLite Tips (DatabaseSessionService)

**Database File Location:**
```python
# Relative path (in current directory)
db_url = "sqlite:///sessions.db"

# Absolute path
db_url = "sqlite:////absolute/path/to/sessions.db"
```

**Inspecting the Database:**
```python
import sqlite3

with sqlite3.connect("my_agent_data.db") as conn:
    cursor = conn.cursor()

    # View all sessions
    cursor.execute("SELECT DISTINCT session_id FROM events")
    print(cursor.fetchall())

    # View events for a session
    cursor.execute("""
        SELECT author, content
        FROM events
        WHERE session_id = 'my-session-01'
    """)
    for row in cursor.fetchall():
        print(row)
```

**Cleanup Old Sessions:**
```python
# Delete sessions older than 30 days
cursor.execute("""
    DELETE FROM events
    WHERE timestamp < datetime('now', '-30 days')
""")
conn.commit()
```

## Next Steps

After completing Day 3, you've learned:
- ✅ Session management for stateful conversations
- ✅ Persistent storage with databases
- ✅ Context engineering with compaction
- ✅ Long-term memory across sessions
- ✅ Automated memory management with callbacks

**Continue to Day 4** to learn about:
- Observability and monitoring
- Agent evaluation and testing
- Performance metrics
- Production readiness

**Practice Exercises:**
1. Build a personal assistant that remembers user preferences
2. Create a customer support agent with session history
3. Implement a research agent with knowledge accumulation
4. Add memory to your Day 2 agents for enhanced context

Happy learning! 🧠💾
