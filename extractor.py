#!/usr/bin/env python3
"""
File ID Extractor Bot - Clean Version

Simple bot to extract file_ids for AceBot configuration.
This bot extracts file IDs from forwarded files and displays them in a clean format.
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv("EXTRACTOR_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    if update.callback_query:
        return
        
    welcome_text = """
🔧 **File ID Extractor Bot**

Welcome! This bot helps you extract file IDs for your AceBot configuration.

**How to use:**
1. Forward any file from your content channel to this bot
2. The bot will extract and display the file ID
3. Copy the file ID to your config.py

**Supported file types:**
📄 Documents (PDF, DOC, etc.)
🖼️ Photos (JPG, PNG, etc.)
🎵 Audio files
🎥 Video files

**Example output:**
```
File: Grade_9_Math.pdf
File ID: BQACAgQAAyEFAASkzI5MAAMxaMq6FPhMHdlGN2_B3NDTKz1JjEgAAlcZAALhtlhSPzyJU_cXm8c2BA
```

Ready to extract file IDs! 🚀
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document files."""
    document = update.message.document
    
    # Get file information
    file_name = document.file_name or "Unknown Document"
    file_size = document.file_size or 0
    file_id = document.file_id
    
    # Format file size
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    # Create response
    response = f"""📄 **Document Information**

**File Name:** `{file_name}`
**File Size:** {size_str}
**File ID:** `{file_id}`

**For config.py:**
```python
{{"file_id": "{file_id}", "name": "{file_name}", "type": "document"}}
```"""
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    # Also print to console for easy copying
    print(f"\n📄 {file_name} -> {file_id}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo files."""
    # Get the highest resolution photo
    photo = update.message.photo[-1]
    
    file_id = photo.file_id
    file_size = photo.file_size or 0
    width = photo.width
    height = photo.height
    
    # Format file size
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    # Create response
    response = f"""🖼️ **Photo Information**

**Dimensions:** {width}×{height}
**File Size:** {size_str}
**File ID:** `{file_id}`

**For config.py:**
```python
{{"file_id": "{file_id}", "name": "Photo", "type": "photo"}}
```"""
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    # Also print to console for easy copying
    print(f"\n🖼️ Photo -> {file_id}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio files."""
    audio = update.message.audio
    
    file_name = audio.file_name or "Audio File"
    file_id = audio.file_id
    duration = audio.duration or 0
    file_size = audio.file_size or 0
    
    # Format duration
    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes}:{seconds:02d}"
    
    # Format file size
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    # Create response
    response = f"""🎵 **Audio Information**

**File Name:** `{file_name}`
**Duration:** {duration_str}
**File Size:** {size_str}
**File ID:** `{file_id}`

**For config.py:**
```python
{{"file_id": "{file_id}", "name": "{file_name}", "type": "audio"}}
```"""
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    # Also print to console for easy copying
    print(f"\n🎵 {file_name} -> {file_id}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video files."""
    video = update.message.video
    
    file_name = video.file_name or "Video File"
    file_id = video.file_id
    duration = video.duration or 0
    file_size = video.file_size or 0
    width = video.width
    height = video.height
    
    # Format duration
    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes}:{seconds:02d}"
    
    # Format file size
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    # Create response
    response = f"""🎥 **Video Information**

**File Name:** `{file_name}`
**Duration:** {duration_str}
**Dimensions:** {width}×{height}
**File Size:** {size_str}
**File ID:** `{file_id}`

**For config.py:**
```python
{{"file_id": "{file_id}", "name": "{file_name}", "type": "video"}}
```"""
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    # Also print to console for easy copying
    print(f"\n🎥 {file_name} -> {file_id}")

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle other message types."""
    await update.message.reply_text(
        "❌ **Unsupported file type**\n\n"
        "Please send one of these supported file types:\n"
        "📄 Documents (PDF, DOC, etc.)\n"
        "🖼️ Photos (JPG, PNG, etc.)\n"
        "🎵 Audio files\n"
        "🎥 Video files",
        parse_mode='Markdown'
    )

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("❌ Error: EXTRACTOR_BOT_TOKEN not found in environment variables")
        print("Please set EXTRACTOR_BOT_TOKEN in your .env file")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other_messages))
    
    print("🚀 File ID Extractor Bot starting...")
    print("📱 Bot is ready to extract file IDs!")
    print("✅ Send files to extract their file IDs")
    
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()
