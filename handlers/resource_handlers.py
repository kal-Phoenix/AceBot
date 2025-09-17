# handlers/resource_handlers.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.models import User
from services.telegram_channel import TelegramChannelService
from config import Config
from keyboards import Keyboards
from handlers import user_handlers # For calling start() on error

logger = logging.getLogger(__name__)
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"

# Initialize Telegram Channel service
channel_service = TelegramChannelService()

async def handle_resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the resources menu."""
    await update.message.reply_text(
        "Select resource type:",
        reply_markup=Keyboards.resources_menu()
    )
    logger.info(f"User {update.effective_user.id} shown resources menu.")

async def handle_resource_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles selection from the resources menu (Teacher's Guide, Cheat Sheets)
    that are specifically routed here by main.py's regex.
    """
    user = update.effective_user
    db_user = User.find(user.id)
    text = update.message.text

    if not db_user or not db_user.stream:
        # If user state is inconsistent, restart the flow
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow.")
        return

    # Route to specific handlers based on resource type
    if text == "📚 Teacher's Guide":
        await update.message.reply_text(
            "Select grade level for Teacher's Guide:",
            reply_markup=Keyboards.grades_menu("Guide")
        )
        logger.info(f"User {user.id} selected Teacher's Guide.")
    elif text == "🧮 Cheat Sheets":
        # PREMIUM CHECK for Cheat Sheets
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access Cheat Sheets.")
            return

        await handle_cheat_sheets(update, context)
        logger.info(f"User {user.id} selected Cheat Sheets.")
    elif text == "⬅️ Back to Main Menu":
        await user_handlers.start(update, context)  # Go back to main menu
        logger.info(f"User {user.id} navigated back to main menu from resources.")
    else:
        await update.message.reply_text("Invalid resource type selected.")
        logger.warning(f"User {user.id} sent invalid resource type to handle_resource_selection: {text}")

async def handle_text_books_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the grade selection menu for Textbooks."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for textbooks menu.")
        return

    await update.message.reply_text(
        "Select grade level for Textbooks:",
        reply_markup=Keyboards.grades_menu("Textbooks")
    )
    logger.info(f"User {user.id} selected Text Books and shown grade menu.")

async def handle_grade_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles selection of a specific grade level for textbooks or guides."""
    user = update.effective_user
    db_user = User.find(user.id)
    text = update.message.text
    logger.info(f"handle_grade_selection received text: '{text}' for user {user.id}")

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for grade selection.")
        return

    # Determine resource type based on button text
    if "Textbooks" in text:
        resource_type = "textbooks"
        display_name = "Textbooks"
    elif "Guide" in text:
        resource_type = "guide"
        display_name = "Teacher's Guides"
    else:
        await update.message.reply_text("Invalid selection. Please choose a valid grade button.")
        logger.warning(f"User {user.id} sent invalid grade selection format: {text}")
        return

    grade = text.split()[1]  # Extract grade number (e.g., "9", "10")
    
    # Store grade and resource type for curriculum selection
    context.user_data['selected_grade'] = grade
    context.user_data['selected_resource_type'] = resource_type
    context.user_data['display_name'] = display_name
    
    # Show curriculum selection menu
    await update.message.reply_text(
        f"Select curriculum type for Grade {grade} {display_name}:",
        reply_markup=Keyboards.curriculum_menu(grade, display_name)
    )
    logger.info(f"User {user.id} shown curriculum menu for Grade {grade} {display_name}.")

async def handle_curriculum_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles curriculum selection (Old/New) and delivers files."""
    user = update.effective_user
    db_user = User.find(user.id)
    text = update.message.text
    
    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        return
    
    # Get stored data from context
    grade = context.user_data.get('selected_grade')
    resource_type = context.user_data.get('selected_resource_type')
    display_name = context.user_data.get('display_name')
    
    if not grade or not resource_type:
        await update.message.reply_text("Something went wrong. Please start over.", reply_markup=Keyboards.resources_menu())
        return
    
    # Determine curriculum type
    if text == "Old Curriculum":
        curriculum = "old"
    elif text == "New Curriculum":
        curriculum = "new"
    else:
        await update.message.reply_text("Please select Old Curriculum or New Curriculum.")
        return
    
    # Send files based on curriculum choice
    if resource_type == "textbooks":
        sent_files = await channel_service.get_textbooks(context, db_user.stream, f"{grade}_{curriculum}", user.id)
    elif resource_type == "guide":
        sent_files = await channel_service.get_teachers_guide(context, db_user.stream, f"{grade}_{curriculum}", user.id)
    else:
        sent_files = []
    
    if not sent_files:
        await update.message.reply_text(
            f"No {display_name.lower()} found for Grade {grade} {curriculum.capitalize()} Curriculum ({db_user.stream.capitalize()}) yet. "
            f"Please check the content or contact support.",
            reply_markup=Keyboards.resources_menu()
        )
        return
    
    # Send confirmation message
    sent_count = len([file for file in sent_files if file.get('sent')])
    failed_count = len([file for file in sent_files if not file.get('sent')])
    
    if sent_count > 0:
        await update.message.reply_text(
            f"✅ Sent {sent_count} {display_name.lower()} for Grade {grade} {curriculum.capitalize()} Curriculum ({db_user.stream.capitalize()})!\n\n"
            f"📁 Files have been sent directly to your chat above."
            + (f"\n\n⚠️ {failed_count} files failed to send." if failed_count > 0 else ""),
            reply_markup=Keyboards.resources_menu()
        )
        logger.info(f"Sent {sent_count} {display_name.lower()} ({curriculum}) to user {user.id}.")
    else:
        await update.message.reply_text(
            f"❌ Failed to send {display_name.lower()}. Please try again or contact support.",
            reply_markup=Keyboards.resources_menu()
        )
    
    # Clear stored data
    context.user_data.pop('selected_grade', None)
    context.user_data.pop('selected_resource_type', None)
    context.user_data.pop('display_name', None)

async def handle_short_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user to select a subject for short notes."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for short notes.")
        return

    # PREMIUM CHECK for Short Notes
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to access Short Notes.")
        return

    # Set pending action to indicate that the next text message will be a subject selection for notes
    db_user.pending_action = "select_notes_subject"
    db_user.save()
    logger.info(f"User {user.id} set pending_action to 'select_notes_subject'.")

    await update.message.reply_text(
        f"Select subject for {db_user.stream.capitalize()} stream notes:",
        reply_markup=Keyboards.subjects_menu(db_user.stream)
    )

async def _process_notes_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User,
                                           subject_text: str):
    """Processes the selected subject for short notes and provides links."""
    # PREMIUM CHECK for Short Notes - Block access entirely for non-premium users
    if not db_user.is_premium:
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            "📚 *Short Notes* are exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Comprehensive study notes\n"
            "• Subject-specific materials\n"
            "• High-quality content\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"Non-premium user {db_user.user_id} attempted to access Short Notes.")
        return

    # Map display names to internal keys
    subject_map = {
        "mathematics": "math",
        "english": "english",
        "physics": "physics",
        "biology": "biology",
        "chemistry": "chemistry",
        "aptitude": "aptitude",
        "geography": "geography",
        "history": "history",
        "economics": "economics"
    }

    subject_key = subject_map.get(subject_text.lower())
    if not subject_key:
        await update.message.reply_text("Invalid subject selected for notes.")
        logger.warning(f"User {db_user.user_id} sent invalid notes subject: {subject_text}")
        return

    # Forward files directly from private channel to user
    forwarded_content = await channel_service.get_notes(context, db_user.stream, subject_key, db_user.user_id)
    
    if not forwarded_content:
        await update.message.reply_text(
            f"Short notes for {subject_text.capitalize()} not available for {db_user.stream.capitalize()} stream yet. "
            f"Please check the content or contact support."
        )
        logger.info(f"No notes content found for {subject_key} {db_user.stream} for user {db_user.user_id}.")
        return
    
    # Send confirmation message after sending files
    sent_count = len([file for file in forwarded_content if file.get('sent')])
    failed_count = len([file for file in forwarded_content if not file.get('sent')])
    
    if sent_count > 0:
        await update.message.reply_text(
            f"✅ Sent {sent_count} short notes for {subject_text.capitalize()} ({db_user.stream.capitalize()})!\n\n"
            f"📁 Files have been sent directly to your chat above. You can download, view, or share them as needed."
            + (f"\n\n⚠️ {failed_count} files failed to send." if failed_count > 0 else ""),
            reply_markup=Keyboards.resources_menu()
        )
        logger.info(f"Sent {sent_count} notes to user {db_user.user_id}.")
    else:
        await update.message.reply_text(
            f"❌ Failed to send short notes. Please try again or contact support.",
            reply_markup=Keyboards.resources_menu()
        )
    logger.info(f"User {db_user.user_id} accessed short notes for {subject_text}.")

async def handle_cheat_sheets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user to select a cheat sheet type."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for cheat sheets.")
        return

    # PREMIUM CHECK for Cheat Sheets - Block access entirely for non-premium users
    if not db_user.is_premium:
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            "🧮 *Cheat Sheets* are exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Quick reference guides\n"
            "• Formula collections\n"
            "• Study shortcuts\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"Non-premium user {user.id} attempted to access Cheat Sheets.")
        return

    await update.message.reply_text(
        f"Select {db_user.stream.capitalize()} stream cheat sheet:",
        reply_markup=Keyboards.cheat_sheets_menu(db_user.stream)
    )
    logger.info(f"User {user.id} shown cheat sheets menu.")

async def handle_cheat_sheet_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the selected cheat sheet type and provides links."""
    user = update.effective_user
    db_user = User.find(user.id)
    text = update.message.text

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for cheat sheet selection.")
        return

    # PREMIUM CHECK for Cheat Sheets
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to process Cheat Sheets selection.")
        return

    # Map display names to subject keys
    subject_key_map = {
        "🧮 Math Formulas": "math",
        "📝 English Tips": "english",
        "⚛ Physics Formulas": "physics",
        "🧬 Biology Cheats": "biology",
        "🧪 Chemistry Cheats": "chemistry",
        "🧠 Aptitude Tricks": "aptitude",
        "🗺 Geography Cheats": "geography",
        "📜 History Cheats": "history",
        "💹 Economics Cheats": "economics"
    }

    subject_key = subject_key_map.get(text)
    if not subject_key:
        await update.message.reply_text("Invalid cheat sheet selection.")
        logger.warning(f"User {user.id} sent invalid cheat sheet selection: {text}")
        return

    # Forward files directly from private channel to user
    forwarded_content = await channel_service.get_cheat_sheets(context, db_user.stream, subject_key, user.id)
    
    if not forwarded_content:
        await update.message.reply_text(
            f"Cheat sheets for {subject_key.capitalize()} not available for {db_user.stream.capitalize()} stream yet. "
            f"Please check the content or contact support."
        )
        logger.info(f"No cheat sheets content found for {subject_key} {db_user.stream} for user {user.id}.")
        return
    
    # Send confirmation message after sending files
    sent_count = len([file for file in forwarded_content if file.get('sent')])
    failed_count = len([file for file in forwarded_content if not file.get('sent')])
    
    if sent_count > 0:
        await update.message.reply_text(
            f"✅ Sent {sent_count} cheat sheets for {subject_key.capitalize()} ({db_user.stream.capitalize()})!\n\n"
            f"📁 Files have been sent directly to your chat above. You can download, view, or share them as needed."
            + (f"\n\n⚠️ {failed_count} files failed to send." if failed_count > 0 else ""),
            reply_markup=Keyboards.resources_menu()
        )
        logger.info(f"Sent {sent_count} cheat sheets to user {user.id}.")
    else:
        await update.message.reply_text(
            f"❌ Failed to send cheat sheets. Please try again or contact support.",
            reply_markup=Keyboards.resources_menu()
        )
    logger.info(f"User {user.id} accessed cheat sheets for {subject_key}.")