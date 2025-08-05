#!/bin/bash

# BrowserStack + Percy App Test Runner
# This script sets up the environment and runs the mobile app test

echo "🚀 BrowserStack + Percy Mobile App Test Runner"
echo "=============================================="

# Check if creds.sh exists
if [ ! -f "creds.sh" ]; then
    echo "❌ Error: creds.sh file not found!"
    echo "Please create creds.sh with your BrowserStack and Percy credentials."
    exit 1
fi

# Source credentials
echo "🔐 Loading credentials from creds.sh..."
source creds.sh

# Check if required credentials are set
if [ -z "$BROWSERSTACK_USERNAME" ] || [ -z "$BROWSERSTACK_ACCESS_KEY" ] || [ -z "$PERCY_TOKEN" ]; then
    echo "❌ Error: Missing required credentials in creds.sh"
    echo "Please ensure BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, and PERCY_TOKEN are set."
    exit 1
fi

echo "✅ Credentials loaded successfully"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Make Python script executable
chmod +x browserstack_percy_app_test.py

# Run the test
echo "🎯 Starting BrowserStack + Percy app test..."
echo "=============================================="
python browserstack_percy_app_test.py

# Capture exit code
exit_code=$?

echo "=============================================="
if [ $exit_code -eq 0 ]; then
    echo "✅ Test completed successfully!"
    echo "📊 Check your Percy dashboard for visual comparisons"
    echo "📱 Check your BrowserStack dashboard for test details"
else
    echo "❌ Test failed with exit code: $exit_code"
fi

echo "=============================================="