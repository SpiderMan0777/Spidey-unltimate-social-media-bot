import os
import time
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# Set up logging to track errors and actions
logging.basicConfig(level=logging.INFO)

# Replit uses environment variables for sensitive info, so we retrieve them from there
API_ID = os.environ.get("API_ID")  # Set this in Replit secrets
API_HASH = os.environ.get("API_HASH")  # Set this in Replit secrets
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Set this in Replit secrets

# Bot client initialization
bot = Client(
    "powerful_media_downloader_bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Ensure the 'downloads' directory exists (for saving media files)
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Logger class for yt-dlp to handle video/audio download logs
class MyLogger:
    def debug(self, msg):
        pass  # Ignore debug messages

    def warning(self, msg):
        logging.warning(f"WARNING: {msg}")

    def error(self, msg):
        logging.error(f"ERROR: {msg}")

# yt-dlp options for downloading videos
ydl_opts_video = {
    "format": "bestvideo+bestaudio/best",  # Get the best quality video + audio
    "outtmpl": "downloads/%(title)s.%(ext)s",  # Downloaded file template
    "quiet": True,
    "logger": MyLogger(),  # Use custom logger
}

# yt-dlp options for downloading audio in MP3 format
ydl_opts_audio = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    }],
}

# Emoji toggle for alternating between two emojis
emoji_toggle = 0  # Tracks which emoji to display

# Stylish Inline Buttons (for user interaction)
def generate_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")]
    ])

# Welcome buttons for /start message
def generate_welcome_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")],
    ])

# Welcome command (/start)
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    await message.reply_photo(
        photo="https://i.ibb.co/dt3C6pq/6744c613.jpg",  # Replace with your image URL
        caption=(
            f"👋 **Welcome {user_name} to the Ultimate Media Downloader Bot!**\n\n"
            "🎥 Download videos in the highest quality.\n\n"
            "✨ Simply send me any YouTube, Instagram, or Facebook link and let me handle the rest!\n\n"
            "**__Powered by: @Hacker_x_official_777__**"
        ),
        reply_markup=generate_welcome_buttons()
    )

# General URL handler for downloading video/audio
@bot.on_message(filters.text & filters.private)
async def download_handler(client, message):
    global emoji_toggle
    url = message.text.strip()

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL that starts with http:// or https://.")
        return

    # Alternate between 🚀 and ⚡ emojis
    temp_emoji = "🚀" if emoji_toggle % 2 == 0 else "⚡"
    emoji_toggle += 1

    # Send temporary emoji and update after 2 seconds
    progress_msg = await message.reply_text(temp_emoji)
    time.sleep(2)
    await progress_msg.edit_text("🔄 **Processing your request... Please wait!**")

    try:
        # Download the video
        with YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)
            await message.reply_video(
                video_file,
                caption=f"🎥 **{info.get('title', 'Untitled')}**\n\n✅ Your video is ready to watch or share!",
                reply_markup=generate_buttons()
            )
            os.remove(video_file)  # Clean up by deleting the downloaded video file

    except Exception as e:
        await message.reply_text(f"❌ **Failed to download video:** {str(e)}")

# MP3 download command
@bot.on_message(filters.command("mp3") & filters.private)
async def download_audio(client, message):
    global emoji_toggle
    url = message.text.split(" ", 1)[-1].strip()

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL that starts with http:// or https://.")
        return

    # Alternate between 🚀 and ⚡ emojis
    temp_emoji = "🚀" if emoji_toggle % 2 == 0 else "⚡"
    emoji_toggle += 1

    # Send temporary emoji and update after 2 seconds
    progress_msg = await message.reply_text(temp_emoji)
    time.sleep(2)
    await progress_msg.edit_text("🎵 **Processing your MP3 request... Please wait!**")

    try:
        # Download the audio
        with YoutubeDL(ydl_opts_audio) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)
            await message.reply_audio(
                audio_file,
                caption=f"🎶 **{info.get('title', 'Untitled')}**\n\n🎧 Enjoy your high-quality MP3!",
                reply_markup=generate_buttons()
            )
            os.remove(audio_file)  # Clean up by deleting the downloaded audio file

    except Exception as e:
        await message.reply_text(f"❌ **Failed to download MP3:** {str(e)}")

# Run the bot
print("🚀 Bot is running...")
bot.run()
