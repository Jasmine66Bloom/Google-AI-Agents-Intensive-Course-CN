✅ ADK components imported successfully.
✅ API key loaded from .env file
✅ Helper functions defined.

================================================================================
SECTION 3: Initialize MemoryService
================================================================================
✅ Agent and Runner created with memory support!

================================================================================
SECTION 4: Ingest Session Data into Memory
================================================================================

### Session: conversation-01

User > My favorite color is blue-green. Can you write a Haiku about it?
Model: > A shimmering hue,
Ocean depths and forest green,
Calm and peaceful shade.

📝 Session contains:
  user: My favorite color is blue-green. Can you write a Haiku about...
  model: A shimmering hue,
Ocean depths and forest green,
Calm and pe...

✅ Session added to memory!

================================================================================
SECTION 5: Enable Memory Retrieval in Your Agent
================================================================================
✅ Agent with load_memory tool created.

### Session: color-test

User > What is my favorite color?
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Model: > Your favorite color is blue-green.

--- Complete Manual Workflow Test ---

### Session: birthday-session-01

User > My birthday is on March 15th.
Model: > Okay, I will remember that your birthday is on March 15th.

✅ Birthday session saved to memory!

### Session: birthday-session-02

User > When is my birthday?
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
Model: > Your birthday is on March 15th.

--- Manual Memory Search ---

🔍 Search Results:
  Found 3 relevant memories

  [user]: My favorite color is blue-green. Can you write a Haiku about it?...
  [user]: My birthday is on March 15th....
  [MemoryDemoAgent]: Okay, I will remember that your birthday is on March 15th....

================================================================================
SECTION 6: Automating Memory Storage
================================================================================
✅ Agent created with automatic memory saving!

### Session: auto-save-test

User > I gifted a new toy to my nephew on his 1st birthday!
Model: > That's wonderful! A first birthday is such a special milestone. I hope your nephew loves his new toy!

### Session: auto-save-test-2

User > What did I gift my nephew?
Model: > You gifted your nephew a new toy.