#!/bin/bash

echo "Setting up B2 Monitoring Tool..."
sleep 2

echo "Checking if Python 3 is installed..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3
    sleep 2
else
    echo "Python 3 is already installed."
    sleep 2
fi

echo "Installing python3-venv package..."
sudo apt install -y python3-venv
sleep 2

echo "Creating virtual environment in current user's home directory..."
python3 -m venv ~/b2_env
sleep 2

echo "Activating virtual environment..."
source ~/b2_env/bin/activate
sleep 2

echo "Updating package list..."
sudo apt update
sleep 2

echo "Installing B2 CLI in virtual environment..."
pip install b2
sleep 2

echo "Installing git..."
sudo apt install -y git
sleep 2

echo "Now you need to authorize your B2 account."
echo "Please enter your B2 account ID and application key when prompted."
sleep 2
b2 account authorize
sleep 2

echo "Creating default configuration..."
python3 b2monitoring.py --first-run
sleep 2

echo ""
echo "Setup complete!"
echo "A default configuration file 'config.json' has been created."
echo ""
echo "Next steps:"
echo "1. Edit the config.json file to customize your settings:"
echo "   nano config.json"
echo ""
echo "2. Run the monitoring script:"
echo "   python3 b2monitoring.py"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "   source ~/b2_env/bin/activate"
echo ""
echo "Enjoy your B2 monitoring tool!"
