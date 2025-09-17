#!/usr/bin/env python3
"""
File ID Extractor Bot

Simple bot to extract file_ids for AceBot configuration.
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Minimal logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Bot token
EXTRACTOR_BOT_TOKEN = os.getenv("EXTRACTOR_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    # Prevent duplicate processing by checking if this is a callback query
    if update.callback_query:
        return
        
    await update.message.reply_text(
        "🔧 File ID Extractor Bot\n\n"
        "Send me any file and I'll give you the file_id!\n\n"
        "Supported: 📄 Documents, 🖼️ Photos, 🎵 Audio, 🎥 Videos"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle ALL non-command messages in one place."""
    message = update.message
    
    # Check for any media type first
    has_media = any([
        message.document,
        message.photo,
        message.audio,
        message.video,
        message.voice,
        message.sticker,
        message.animation,
        message.video_note
    ])
    
    # Handle documents
    if message.document:
        doc = message.document
        response = f"""📄 *File Information*

• Name: {doc.file_name}
• Size: {doc.file_size / 1024 / 1024:.2f} MB

```
{doc.file_id}
```"""
        
        await message.reply_text(response, parse_mode='Markdown')
        print(f" {doc.file_name} -> {doc.file_id}")
        return
    
    # Handle photos
    if message.photo:
        photo = message.photo[-1]
        response = f"""🖼️ *Photo Information*

• Size: {photo.file_size / 1024:.2f} KB
• Dimensions: {photo.width}×{photo.height}

`{photo.file_id}`"""
        
        await message.reply_text(response, parse_mode='Markdown')
        print(f"🖼️ Photo -> {photo.file_id}")
        return
    
    # Handle audio
    if message.audio:
        audio = message.audio
        duration_min = audio.duration // 60
        duration_sec = audio.duration % 60
        response = f"""🎵 *Audio Information*

• File: {audio.file_name or 'Audio File'}
• Duration: {duration_min}:{duration_sec:02d}

`{audio.file_id}`"""
        
        await message.reply_text(response, parse_mode='Markdown')
        print(f"🎵 {audio.file_name or 'Audio'} -> {audio.file_id}")
        return
    
    # Handle video
    if message.video:
        video = message.video
        duration_min = video.duration // 60
        duration_sec = video.duration % 60
        response = f"""🎥 *Video Information*

• Duration: {duration_min}:{duration_sec:02d}
• Dimensions: {video.width}×{video.height}
• Size: {video.file_size / (1024*1024):.1f} MB

`{video.file_id}`"""
        
        await message.reply_text(response, parse_mode='Markdown')
        print(f"🎥 Video -> {video.file_id}")
        return
    
    # Handle voice
    if message.voice:
        voice = message.voice
        duration_min = voice.duration // 60
        duration_sec = voice.duration % 60
        response = f"""🎤 *Voice Message*

• Duration: {duration_min}:{duration_sec:02d}
• Size: {voice.file_size / 1024:.1f} KB

`{voice.file_id}`"""
        
        await message.reply_text(response, parse_mode='Markdown')
        print(f"🎤 Voice -> {voice.file_id}")
        return
    
    # Only process text if there's no media
    if message.text and not has_media:
        await message.reply_text(
            "📁 Send me a file to extract its file_id!\n\n"
            "Supported: 📄 Documents, 🖼️ Photos, 🎵 Audio, 🎥 Videos"
        )
        return
    
    # If we get here, it's an unsupported message type
    if not has_media:
        await message.reply_text("❌ Unsupported file type. Send documents, photos, audio, or videos.")

def main():
    """Start the bot."""
    if not EXTRACTOR_BOT_TOKEN:
        print("❌ Please set EXTRACTOR_BOT_TOKEN in .env file")
        return
    
    # Create application
    app = Application.builder().token(EXTRACTOR_BOT_TOKEN).build()

    # Add handlers - ONLY TWO HANDLERS to prevent conflicts
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, handle_message))  # Everything except commands

    print("🚀 Clean File ID Extractor starting...")
    print("📱 Bot: @file_id12bot")
    print("✅ Single response guaranteed!")
    
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n⏹️  Stopped")

if __name__ == '__main__':
    main()
