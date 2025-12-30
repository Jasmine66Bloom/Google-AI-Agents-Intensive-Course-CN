# Quick Start Guide

Get up and running with the AI Agents course in 3 simple steps!

## Step 1: Run Setup Script

```bash
./setup.sh
```

This will automatically:
- Create a Python virtual environment
- Install all required packages (google-adk, python-dotenv, etc.)
- Create a .env file template

## Step 2: Add Your API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/api-keys)

2. Open the `.env` file in your editor:
   ```bash
   nano .env
   # or use your favorite editor: code .env, vim .env, etc.
   ```

3. Replace `your-api-key-here` with your actual API key:
   ```
   GOOGLE_API_KEY=AIzaSyC_your_actual_key_here
   ```

4. Save and close the file

## Step 3: Run Your First Agent

```bash
# Make sure the virtual environment is activated
# You should see (venv) in your terminal prompt
source venv/bin/activate

# Navigate to Day 1 folder
cd Day-1

# Run the first script
python day_1a_prompt_to_action.py
```

## What's Next?

After completing the first script, try:

```bash
# Run the multi-agent architectures script
python day_1b_agent_architectures.py
```

## Need Help?

- Check the [Day-1/README.md](Day-1/README.md) for detailed instructions
- Make sure you see `(venv)` in your terminal before running scripts
- If you get errors, see the Troubleshooting section in the README

## Deactivating the Virtual Environment

When you're done:

```bash
deactivate
```

This returns you to your system Python environment.

---

**Note:** Your `.env` file containing your API key is protected by `.gitignore` and will never be committed to git!
