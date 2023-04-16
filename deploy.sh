# Enable Amazon Linux 2 Extras repository for Python 3.9
sudo amazon-linux-extras enable python3.9

# Update the package lists
sudo yum update -y

# Install Python 3.9
sudo yum install -y python3.9

# Remove the existing python3 link and create a new symbolic link for Python 3.9
sudo rm -f /usr/bin/python3
# Create a new symbolic link for 'python3' pointing to 'python3.9'
sudo ln -s /usr/bin/python3.9 /usr/bin/python3

# Verify the installed Python 3.9 version
python3 --version

# Set environment variables on the EC2 instance
echo "export ENVIRONMENT=${ENVIRONMENT}" >> ~/.bashrc
echo "export OPENAI_API_KEY=${OPENAI_API_KEY}" >> ~/.bashrc
echo "export DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}" >> ~/.bashrc
echo "export GITHUB_TOKEN=${GITHUB_TOKEN}" >> ~/.bashrc
# Reload the .bashrc file
source ~/.bashrc

# Your existing deployment commands, e.g.:
# Stop the existing service
# Start the new service

# Replace these variables with your actual values
BOT_DIRECTORY="/home/ec2-user/ai-assistant"
BOT_SCRIPT="bot/main.py"

# Go to the bot directory and restart the bot
cd $BOT_DIRECTORY
pip3 install --user -r requirements.txt
pkill -f $BOT_SCRIPT
nohup python3 $BOT_SCRIPT &>/dev/null &
disown
