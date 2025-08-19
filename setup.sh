#!/bin/bash

# Impostor Word Game - Setup Script
echo "🎮 Setting up Impostor Word Game Server..."
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🚀 Setup complete! You can now run the game server with:"
    echo "   python3 server.py"
    echo ""
    echo "📱 Players can then connect by going to the IP address shown by the server"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
