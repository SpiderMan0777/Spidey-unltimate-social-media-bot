import os
import time
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# Initialize logging for better debugging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot Configuration
API_ID = 28519661  # Replace with your API ID
API_HASH = "d47c74c8a596fd3048955b322304109d"  # Replace with your API Hash
BOT_TOKEN = "7620991709:AAEaPfZWjauYBN5zU1d64RYiwqPPiM-3gjA"  # Replace with your bot token

# Ensure 'downloads' directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Create the bot client
bot = Client(
    "powerful_media_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./"  # Set workdir to ensure session files are saved in the right place
)

# Custom logger for yt-dlp
class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

# yt-dlp Options for Video and Audio
ydl_opts_video = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": True,
    "logger": MyLogger(),
}

ydl_opts_audio = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
}

# Function to generate inline buttons
def generate_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")]
    ])

# Function to generate welcome message buttons
def generate_welcome_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")],
    ])

# Start Command - Displays a welcome message with image and buttons
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    # Log user interaction
    logging.info(f"User {user_name} (ID: {user_id}) started the bot.")
    
    # Send welcome message with image and buttons
    await message.reply_photo(
        photo="https://i.ibb.co/dt3C6pq/6744c613.jpg",  # Replace with your image URL
        caption=(
            "👋 **Welcome to the Ultimate Media Downloader Bot!**\n\n"
            "🎥 Download videos in the highest quality.\n\n"
            "✨ Simply send me any YouTube, Instagram, or Facebook link and let me handle the rest!\n\n"
            "**__Powered by: @Hacker_x_official_777__**"
        ),
        reply_markup=generate_welcome_buttons()
    )

# Help Command - Provides bot instructions
@bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    help_text = (
        "**🤖 Bot Commands and Features:**\n\n"
        "/start - Welcome message\n"
        "/mp3 - Download MP3 from YouTube\n"
        "/statics - Admin-only: View user statistics\n\n"
        "💡 *Simply send any YouTube, Instagram, or Facebook link to download videos or audio.*"
    )
    await message.reply_text(help_text, reply_markup=generate_buttons())

# General URL Handler - Downloads video or audio based on user input
@bot.on_message(filters.text & filters.private)
async def download_handler(client, message):
    url = message.text.strip()

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL. Make sure it starts with http:// or https://.")
        return

    # Send a processing message
    progress_msg = await message.reply_text("🔄 **Processing your request... Please wait!**")

    try:
        # Download video
        with YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)
            await message.reply_video(
                video_file,
                caption=f"🎥 **{info.get('title', 'Untitled')}**\n\n✅ Your video is ready to watch or share!\n\n**__Powered by: @Hacker_x_official_777__**",
                reply_markup=generate_buttons()
            )
            os.remove(video_file)

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await message.reply_text(f"❌ **Failed to download video:** {str(e)}")

# Download MP3 Command - Extracts and sends audio from a YouTube video
@bot.on_message(filters.command("mp3") & filters.private)
async def download_audio(client, message):
    url = message.text.split(" ", 1)[-1].strip()

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL. Make sure it starts with http:// or https://.")
        return

    # Send a processing message
    progress_msg = await message.reply_text("🎵 **Processing your MP3 request... Please wait!**")

    try:
        # Download audio
        with YoutubeDL(ydl_opts_audio) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)
            await message.reply_audio(
                audio_file,
                caption=f"🎶 **{info.get('title', 'Untitled')}**\n\n🎧 Enjoy your high-quality MP3!",
                reply_markup=generate_buttons()
            )
            os.remove(audio_file)

    except Exception as e:
        logging.error(f"Error downloading MP3: {e}")
        await message.reply_text(f"❌ **Failed to download MP3:** {str(e)}")

# Run the bot
if __name__ == "__main__":
    try:
        logging.info("🚀 Bot is starting...")
        bot.run()  # Start the bot
    except Exception as e:
        logging.critical(f"Bot failed to start: {e}")
