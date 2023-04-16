from discord import Intents
import discord
import os
import asyncio
import inspect
from discord.ext import commands
from config import TOKEN, ERROR_CHANNEL_ID, AI_CHANNEL
from utils.openai_handler import generate_response, create_message
from utils.error_handler import send_error_to_channel
from utils.prompt_builder import build_system_prompt
from utils.message_splitter import split
from store.conversations import create_conversation, get_conversation, update_conversation
from components.chat_setup import ChatSettingView

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

 # A dictionary to store conversations per user
def is_allowed_channel(ctx):
    return ctx.channel.id == AI_CHANNEL

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
@commands.check(is_allowed_channel)
async def chat(ctx):
    user_name = ctx.author.name
    user_id = ctx.author.id
    view = ChatSettingView(ctx, user_name, user_id)
    await ctx.send('Select temperature and enter your prompt:', view=view)

@bot.command()
async def resetchat(ctx):
    existing_conversation = get_conversation(ctx.author.id)
    if not existing_conversation:
        await ctx.send('No chat history to reset')
        return
    user_id = ctx.author.id
    existing_conversation['conversation'] = []
    update_conversation(user_id, existing_conversation)
    await ctx.send(f'Chat history reset for user: {ctx.author.name}')

@bot.event
async def on_message(message):
    try:
        if message.content.startswith("/"):
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
    
        user_id = message.author.id
        user_name = message.author.name
        system_prompt = build_system_prompt(user_name, bot)
        print(system_prompt)
        if not get_conversation(user_id):
            conversaton = [create_message("system", system_prompt)]
            create_conversation(user_id, conversaton)
        

        prompt = message.content
        conversaton = get_conversation(user_id)
        conversaton_history = conversaton['conversation']
        conversaton_history.append(create_message("user", prompt))
        async with message.channel.typing():
            response = await generate_response(conversaton_history)
            conversaton_history.append(create_message("assistant", response))
            update_conversation(user_id, conversaton)
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
