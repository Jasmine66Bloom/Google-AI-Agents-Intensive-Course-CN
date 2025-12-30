#!/bin/bash

# Setup script for AI Agents Intensive Course
# This script sets up a Python virtual environment and installs dependencies

echo "=================================================="
echo "  AI Agents Intensive Course - Setup Script"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "=================================================="
    echo "  ⚠️  IMPORTANT: Configure your API key"
    echo "=================================================="
    echo ""
    echo "1. Open the .env file in your editor"
    echo "2. Replace 'your-api-key-here' with your actual API key"
    echo "3. Get your key from: https://aistudio.google.com/app/api-keys"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=================================================="
echo "  ✅ Setup Complete!"
echo "=================================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the Day 1 scripts:"
echo "  cd Day-1"
echo "  python day_1a_prompt_to_action.py"
echo "  python day_1b_agent_architectures.py"
echo ""
echo "To deactivate the virtual environment when done:"
echo "  deactivate"
echo ""
