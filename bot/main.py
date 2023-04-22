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

intents = Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="/", intents=intents)
 # A dictionary to store conversations per user
def is_allowed_channel(ctx):
    return ctx.channel.id == AI_CHANNEL

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()
async def chat(ctx, temperature: float, system_prompt: str):
    if 0 <= temperature <= 2:
        # create conversation 
        thread_name = f"Chat with GPT-4 - {ctx.author.name}"
        thread = await ctx.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        conversation = {
            "thread_id": str(thread.id),
            "system prompt": system_prompt,
            "temperature": str(temperature),
            "messages": [create_message("system", system_prompt)]
        }
        create_conversation(conversation)
        await thread.send(f"Temperature: {temperature}\nSystem Prompt: {system_prompt}\n\nPlease send a message in this thread to start a conversation with GPT-4!")
    else:
        await ctx.send("Temperature must be a number between 0 and 2.")

@chat.error
async def chat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Usage: !chat <temperature> <system_prompt>")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Temperature must be a number.")

@bot.command()
async def resetchat(ctx):
    existing_conversation = get_conversation(ctx.author.id)
    if not existing_conversation:
        await ctx.send('No chat history to reset')
        return
    # user_id = ctx.author.id
    existing_conversation['messages'] = []
    update_conversation(existing_conversation)
    await ctx.send(f'Chat history reset for user: {ctx.author.name}')

@bot.event
async def on_message(message):
    # if not dm or in a thread or in the allowed channel, ignore
    if message.channel.type != discord.ChannelType.private and not is_allowed_channel(message):
        if message.channel.type !=discord.ChannelType.public_thread:
            return
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

        # if message is setn from a thread, use thread_id as key to store
        # else use user_id as key to store
        if message.channel.type == discord.ChannelType.public_thread:
            conversation_id = str(message.channel.id)
        else:
            conversation_id = str(message.author.id)
        user_name = message.author.name
        if not get_conversation(conversation_id):
            system_prompt = build_system_prompt(user_name, bot)
            message_history = [create_message("system", system_prompt)]
            conversation = {
                "thread_id": conversation_id,
                "system prompt": system_prompt,
                "temperature": 0.5,
                "messages": message_history
            }
            create_conversation(conversation)
        

        prompt = message.content
        conversation = get_conversation(conversation_id)
        conversation['messages'].append(create_message("user", prompt))
        async with message.channel.typing():
            response = await generate_response(conversation)
            conversation['messages'].append(create_message("assistant", response))
            update_conversation(conversation)
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
