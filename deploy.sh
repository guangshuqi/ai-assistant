#!/bin/bash

# Replace these variables with your actual values
BOT_DIRECTORY="/home/ec2-user/ai-assistant"
BOT_SCRIPT="discord_bot.py"

# Go to the bot directory and restart the bot
cd $BOT_DIRECTORY
pkill -f $BOT_SCRIPT
nohup python3 $BOT_SCRIPT &
