#!/bin/bash

# Update the package list and install the necessary development tools
sudo yum update -y
sudo yum groupinstall -y "Development Tools"

# Install the required dependencies for Python 3.9
sudo yum install -y openssl-devel bzip2-devel libffi-devel

# Download the Python 3.9 source code
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz

# Extract the downloaded archive and change to the extracted directory
tar xzf Python-3.9.0.tgz
cd Python-3.9.0

# Configure and build Python 3.9
./configure --enable-optimizations
make

# Install Python 3.9
sudo make install

# Remove the existing python3 link and create a new symbolic link for Python 3.9
sudo rm -f /usr/bin/python3
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3

# Verify the installed Python 3.9 version
python3 --version
OPENAI_API_KEY="$1"
DISCORD_BOT_TOKEN="$2"

# Set environment variables on the EC2 instance
echo "export ENVIRONMENT=${ENVIRONMENT}" >> ~/.bashrc
echo "export OPENAI_API_KEY=${OPENAI_API_KEY}" >> ~/.bashrc
echo "export DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}" >> ~/.bashrc

# Reload the .bashrc file
source ~/.bashrc

# Your existing deployment commands, e.g.:
# Stop the existing service
# Start the new service

# Replace these variables with your actual values
BOT_DIRECTORY="/home/ec2-user/ai-assistant"
BOT_SCRIPT="discord_bot.py"

# Go to the bot directory and restart the bot
cd $BOT_DIRECTORY
pip3 install --user -r requirements.txt
pkill -f $BOT_SCRIPT
nohup python3 $BOT_SCRIPT &
