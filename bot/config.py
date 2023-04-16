import os
from dotenv import load_dotenv

environment = os.environ.get("ENVIRONMENT")

if environment == "production":
    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
else:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ERROR_CHANNEL_ID = 1095546338340515980 
if environment == "production":
    AI_CHANNEL = 1096979770702577666
else:
    AI_CHANNEL = 1096979578943176725