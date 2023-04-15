from discord import Intents
import os
import asyncio
import inspect
from discord.ext import commands
from config import TOKEN, ERROR_CHANNEL_ID
from utils.openai_handler import generate_response, create_message
from utils.error_handler import send_error_to_channel
from utils.prompt_builder import build_prompt
from utils.message_splitter import split
from store.conversations import conversations
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

 # A dictionary to store conversations per user

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.content.startswith("!"):
        print('executing command')
        if message.author == bot.user:
            ctx = await bot.get_context(message)
        # the type of the invocation context's bot attribute will be correct
            # await bot.invoke(ctx)  
            cog = bot.get_cog('GithubCog')
            if message.content == '!listfile':
                await cog.listfile(ctx)
            else:
                command_name, args = message.content.split(' ', 1)
                command_function = getattr(cog, command_name[1:])
                # argspec = inspect.getfullargspec(command_function)
                number_of_arguments = len(command_function.signature.split(' '))
                args_list = args.split(' ', number_of_arguments - 1)
                await command_function(ctx, *args_list)
        else:
            await bot.process_commands(message)
        return
    if message.channel.id == ERROR_CHANNEL_ID or message.author == bot.user:
        return
    try:
        user_id = message.author.id
        user_name = message.author.name
        system_prompt = build_prompt(user_name, bot)
        print(system_prompt)
        if user_id not in conversations:
            conversations[user_id] = [create_message("system", system_prompt)]

        prompt = message.content
        conversations[user_id].append(create_message("user", prompt))
        async with message.channel.typing():
            response = await generate_response(conversations[user_id])
            conversations[user_id].append(create_message("assistant", response))
            # Split the response into multiple messages using the textwrap module
            wrapped_response = split(response)
            for chunk in wrapped_response:
                await message.reply(chunk)
    except Exception as e:
        await send_error_to_channel(bot, str(e))

    # await bot.process_commands(message)

# Load the GitHub extension
async def load_extensions():
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
