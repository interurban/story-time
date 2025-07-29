#!/bin/bash

echo "Setting up Bedtime Story Generator..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.9+ first."
    echo "Visit: https://python.org/downloads/"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

echo
echo "Setup complete!"
echo
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Edit .env and add your OpenAI API key"
echo "3. Run: python app.py"
echo
echo "Your app will be available at: http://localhost:5000"
echo
