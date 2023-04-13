from discord import Intents
import textwrap
from discord.ext import commands
from config import TOKEN, ERROR_CHANNEL_ID
from utils.openai_handler import generate_response, create_message
from utils.error_handler import send_error_to_channel
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

conversations = {}  # A dictionary to store conversations per user
MAX_MESSAGE_LENGTH = 2000

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.channel.id == ERROR_CHANNEL_ID or message.author == bot.user:
        return
    try:
        user_id = message.author.id
        user_name = message.author.name
        if user_id not in conversations:
            conversations[user_id] = [create_message("system", (f"You are a helpful assistant. You are chatting with {user_name}."
                            "First, provide information to the user. If you do not have needed information, "
                            "search for this information by outputting the string `[Search Request]` followed by "
                            "a concise description of needed information. You can also ask follow up questions to the user"
                            "to clarify the information needed."
                            ))]

        prompt = message.content
        conversations[user_id].append(create_message("user", prompt))
        async with message.channel.typing():
            response = await generate_response(conversations[user_id])
            conversations[user_id].append(create_message("assistant", response))
            # Split the response into multiple messages using the textwrap module
            wrapped_response = textwrap.wrap(response, width=MAX_MESSAGE_LENGTH, break_long_words=True, replace_whitespace=False)
            for chunk in wrapped_response:
                await message.channel.send(chunk)
    except Exception as e:
        await send_error_to_channel(bot, str(e))

    await bot.process_commands(message)
    
bot.run(TOKEN)
