
import discord
import os
from PIL import Image
from pathlib import Path

# Discord bot token
TOKEN = 'YOUR-TOKEN-HERE'

# Base directory to save the MJ-images folder on your desktop
BASE_DIR = str(Path.home() / 'Desktop' / 'MJ-images')

intents = discord.Intents.default()
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('Bot is ready.')

@client.event
async def on_raw_reaction_add(payload):
    # Fetch the message using the payload data
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Check if the reaction is from the bot itself or another user
    if payload.member == client.user:
        return

    # Check if the reaction is on a message with attachments
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Get the channel name
                channel_name = message.channel.name
                if not channel_name:
                    print('Error: Could not retrieve channel name.')
                    return

                # Define the base directory path
                base_dir = os.path.join(BASE_DIR, 'YOUR-FOLDER-NAME-HERE')

                # Create the base directory if it doesn't exist
                os.makedirs(base_dir, exist_ok=True)

                # Create or check for the channel directory within the base directory
                channel_dir = os.path.join(base_dir, channel_name)
                os.makedirs(channel_dir, exist_ok=True)

                # Format the image filename
                filename = f"YOUR-DESIRED-FILENAME-HERE_{channel_name}_{attachment.filename}"

                image_path = os.path.join(channel_dir, filename)

                # Download the image
                await attachment.save(image_path)
                print(f'Downloaded image: {image_path}')

                # Determine the size based on the reaction emoji
                size = (1000, 1500)  # Default size
                if str(payload.emoji) == '✅':
                    size = (1000, 1000)  # Resize to 1000x1000 for '✅'
                elif str(payload.emoji) == '⚡':
                    size = (1500, 1500)  # Resize to 1500x1500 for '⚡'

                # Upscale image
                upscaled_image = upscale_image(image_path, size)
                upscaled_image.save(image_path)
                print(f'Saved upscaled image: {image_path}')

    print(f"Reaction added by {payload.member.name}")


def upscale_image(image_path, size):
    try:
        with Image.open(image_path) as image:
            upscaled_image = image.resize(size)
            return upscaled_image
    except Exception as e:
        print(f'Error upscaling image: {image_path}')
        print(e)
        return None

client.run(TOKEN)
