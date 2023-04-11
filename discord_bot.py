import os
import discord
import openai
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

environment = os.environ.get("ENVIRONMENT")

if environment == "production":
    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
else:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY
conversations = {}  # Store conversations per user

async def generate_response(user_id, messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    user_name = message.author.name

    # Create a new conversation for the user if it doesn't exist
    if user_id not in conversations:
        conversations[user_id] = [
            {"role": "system", "content": f"You are a helpful assistant. You are chatting with {user_name}."}
        ]

    # Add user message to conversation
    conversations[user_id].append({"role": "user", "content": message.content})

    response_text = await generate_response(user_id, conversations[user_id])
    conversations[user_id].append({"role": "assistant", "content": response_text})

    await message.channel.send(response_text)

    # This line is important! It allows the bot to process commands.
    await bot.process_commands(message)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
