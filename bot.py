from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
import os
import time
import logging

# Setup logging to track errors in Replit
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# Bot Configuration
API_ID = 28519661  # Replace with your API ID
API_HASH = "d47c74c8a596fd3048955b322304109d"  # Replace with your API Hash
BOT_TOKEN = "7620991709:AAEaPfZWjauYBN5zU1d64RYiwqPPiM-3gjA"  # Replace with your bot token

bot = Client("powerful_media_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Ensure the downloads directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Logger for yt-dlp
class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)


# YT-DLP Options
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

# Emoji toggling
emoji_toggle = 0  # Tracks which emoji to display

# User Statistics
user_statistics = {}

# Stylish Inline Buttons
def generate_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")]
    ])


# Welcome Message with Combined Buttons
def generate_welcome_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Subscribe to Our Channel", url="https://t.me/your_channel")],
        [
            InlineKeyboardButton("💬 Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("❓ Support", url="https://t.me/contact_support"),
        ],
        [InlineKeyboardButton("Explore Our Bots", url="https://t.me/more_bots")],
    ])


# Welcome Message with Image and Buttons
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    # Log the user's name and ID
    logging.info(f"{user_name} (ID: {user_id}) started the bot.")
    
    # Update user statistics
    user_statistics[user_id] = user_statistics.get(user_id, 0) + 1

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


# Help Command
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


# General URL Handler
@bot.on_message(filters.text & filters.private)
async def download_handler(client, message):
    global emoji_toggle
    url = message.text.strip()
    user_id = message.from_user.id

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL. Make sure it starts with http:// or https://.")
        return
    
    # Alternate between 🚀 and ⚡ for each new URL
    temp_emoji = "🚀" if emoji_toggle % 2 == 0 else "⚡"
    emoji_toggle += 1

    # Send temporary emoji and wait 2 seconds
    progress_msg = await message.reply_text(temp_emoji)
    time.sleep(2)
    await progress_msg.edit_text("🔄 **Processing your request... Please wait!**")

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

    # Update user statistics
    user_statistics[user_id] = user_statistics.get(user_id, 0) + 1


# Download MP3 Command
@bot.on_message(filters.command("mp3") & filters.private)
async def download_audio(client, message):
    global emoji_toggle
    url = message.text.split(" ", 1)[-1].strip()

    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL. Make sure it starts with http:// or https://.")
        return

    # Alternate between 🚀 and ⚡ for each new URL
    temp_emoji = "🚀" if emoji_toggle % 2 == 0 else "⚡"
    emoji_toggle += 1

    # Send temporary emoji and wait 2 seconds
    progress_msg = await message.reply_text(temp_emoji)
    time.sleep(2)
    await progress_msg.edit_text("🎵 **Processing your MP3 request... Please wait!**")

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


# Statistics Command (Admin Only)
@bot.on_message(filters.command("statics") & filters.private)
async def view_statistics(client, message):
    admin_id = 123456789  # Replace with your Telegram ID
    user_id = message.from_user.id

    if user_id != admin_id:
        await message.reply_text("❌ You are not authorized to view statistics.")
        return

    stats = "\n".join([f"User ID: {uid} | Interactions: {count}" for uid, count in user_statistics.items()])
    stats_message = f"📊 **User Statistics:**\n\n{stats if stats else 'No interactions yet.'}"
    await message.reply_text(stats_message)


# Error handling for Replit
@bot.on_callback_query()
async def handle_callback(client, callback_query):
    try:
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error handling callback query: {e}")


# Bot Run
print("🚀 Bot is now running... Ready to serve users!")
bot.run()
