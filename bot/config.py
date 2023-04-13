import os
from dotenv import load_dotenv

environment = os.environ.get("ENVIRONMENT")

if environment == "production":
    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
else:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ERROR_CHANNEL_ID = 1095546338340515980 