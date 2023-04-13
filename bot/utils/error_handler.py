from config import ERROR_CHANNEL_ID
async def send_error_to_channel(bot, error_message):
    error_channel_id = ERROR_CHANNEL_ID  # Replace with the actual channel ID you copied
    error_channel = bot.get_channel(error_channel_id)
    await error_channel.send(f"**Error:** {error_message}")