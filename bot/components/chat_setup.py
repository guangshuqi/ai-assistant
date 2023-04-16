import discord
from store.conversations import create_conversation
from utils.openai_handler import create_message

class TemperatureSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='0', value='0'),
            discord.SelectOption(label='1', value='1'),
            discord.SelectOption(label='2', value='2'),
        ]
        super().__init__(placeholder='Select temperature', min_values=1, max_values=2, options=options)
    async def callback(self, interaction: discord.Interaction):
        self.view.temperature = self.values[0]
        self.view.stop()

class SystemPromptInput(discord.ui.TextInput):
    def __init__(self):
        super().__init__(label = 'System prompt', placeholder='Enter system prompt', min_length=0, max_length=1000)
    async def callback(self, interaction: discord.Interaction):
        self.view.system_prompt = self.value
        self.view.stop()

class SubmitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Submit', style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        self.view.stop()

class ChatSettingView(discord.ui.View):
    def __init__(self, ctx, user_name, user_id):
        super().__init__()
        self.add_item(TemperatureSelect())
        # self.add_item(SystemPromptInput())
        self.add_item(SubmitButton())
        self.user_name = user_name
        self.user_id = user_id
        self.temperature = 0
        self.system_prompt = "you are a helpful discord bot"

    async def on_interaction(self, interaction: discord.Interaction):
        if self.temperature is not None and self.prompt is not None:
            session_title = f"chat session betwen {self.user_name} and gpt-4"
            embed = discord.Embed(title=session_title, color=discord.Color.blue())
            embed.add_field(name="Selected Temperature", value=self.temperature, inline=False)
            embed.add_field(name="Entered Prompt", value=self.prompt, inline=False)
            embed.set_footer(text="Reply in the thread to start conversation")
            thread = await self.message.channel.create_thread(name=session_title)
            thread = await self.message.channel.create_thread(name=f"chat session betwen {self.user_name} and gpt-4")
            conversation = {
                'temperature': self.temperature,
                'user_id': self.user_id,
                'user_name': self.user_name,
                'messages': [create_message('system', self.system_prompt)]
            }
            create_conversation(thread.id, conversation)
            await thread.send(embed=embed)
