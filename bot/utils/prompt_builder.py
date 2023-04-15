def build_system_prompt(username, bot):
    # Print the docstrings for all commands in the ExampleCog
    commands = ""
    cog = bot.get_cog("GithubCog")
    for command in cog.get_commands():
        commands += f"Command: !{command.name} {command.help}\n\n"
    
    return (f"You are a helpful assistant. You are chatting with {username}."
            "First, provide information to the user. If you do not have needed information, "
            "search for this information by outputting the string `[Search Request]` followed by "
            "a concise description of needed information. You can also ask follow up questions to the user"
            "to clarify the information needed. In addition, you have access to the following github commands for guangshuqi/ai-assistant repo:\n"
            f"{commands}"
            "executes command by only include the command name and inputs if any."
            )
    