import os
import discord
import openai
import threading
import queue
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from search_worker import search_worker

search_queue = queue.Queue() 
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

# start search worker thread
worker_thread = threading.Thread(target=search_worker, args=(search_queue, bot))
worker_thread.start()

async def generate_response(user_id, messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
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
            {
                "role": "system", 
                "content": (f"You are a helpful assistant. You are chatting with {user_name}."\
                "First, provide information to the user. If you do not have needed information, "\
                "search for this information by outputting the string `[Search Request]` followed by "\
                "a concise description of needed information. You can also ask follow up questions to the user"\
                "to clarify the information needed."
                )
                
            }
        ]

    # Add user message to conversation
    conversations[user_id].append({"role": "user", "content": message.content})

    response_text = await generate_response(user_id, conversations[user_id])
    conversations[user_id].append({"role": "assistant", "content": response_text})


    if response_text.startswith("[Search Request]"):
        search_description = response_text[16:].strip()
        search_queue.put((user_id, search_description, message.channel))
        await message.channel.send(f"**_Searching for information:_** {search_description}")
    else:
        await message.channel.send(response_text)

    await bot.process_commands(message)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
