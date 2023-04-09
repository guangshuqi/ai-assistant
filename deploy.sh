#!/bin/bash

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
pkill -f $BOT_SCRIPT
nohup python3 $BOT_SCRIPT &
