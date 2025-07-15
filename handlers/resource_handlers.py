# handlers/resource_handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from config import Config
from keyboards import Keyboards
from handlers import user_handlers # For calling start() on error

logger = logging.getLogger(__name__)
drive_service = GoogleDriveService()
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"

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
    # NOTE: "📖 Text Books" is now handled in handle_message for consistency.
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
        # This else block should ideally not be hit if main.py routing is correct.
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
    logger.info(f"handle_grade_selection received text: '{text}' for user {user.id}")  # DEBUG LOG

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for grade selection.")
        return

    # Determine resource type based on button text
    if "Textbooks" in text:
        resource_type = "textbooks"
        display_name = "Textbooks"
    elif "Guide" in text:
        resource_type = "teachers_guide"
        display_name = "Teacher's Guides"
    else:
        # This should ideally not be hit if the MessageHandler in main.py is correct.
        await update.message.reply_text("Invalid selection. Please choose a valid grade button.")
        logger.warning(f"User {user.id} sent invalid grade selection format: {text}")
        return

    grade = text.split()[1]  # Extract grade number (e.g., "9", "10")
    # Construct the key for Config.DRIVE_FOLDER_IDS
    folder_id_key = f"{db_user.stream}_grade{grade}_{resource_type}"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_id_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Resources not available for {display_name} Grade {grade} ({db_user.stream.capitalize()}) yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_id_key} for user {user.id}.")
        return

    files = drive_service.list_files(folder_id)  # Fetch files from Google Drive
    if not files:
        await update.message.reply_text(f"No resources available for {display_name} Grade {grade}.")
        logger.info(f"No files found in folder {folder_id} for user {user.id}.")
        return

    message = f"📚 {display_name} for Grade {grade} ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.resources_menu())
    logger.info(f"User {user.id} received {display_name} for Grade {grade}.")

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
    # PREMIUM CHECK for Short Notes (redundant if handle_short_notes already checks, but safe)
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {db_user.user_id} attempted to process Short Notes selection.")
        return

    # Map display names to internal keys for folder IDs
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

    subject_key = subject_map.get(subject_text.lower())  # Ensure lower case for mapping
    if not subject_key:
        await update.message.reply_text("Invalid subject selected for notes.")
        logger.warning(f"User {db_user.user_id} sent invalid notes subject: {subject_text}")
        return

    # Construct the key for Config.DRIVE_FOLDER_IDS
    folder_key = f"{db_user.stream}_{subject_key}_notes"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Notes not available for {subject_text.capitalize()} yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text("No notes available for this subject.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return

    message = f"📝 {subject_text.capitalize()} Notes ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.resources_menu())
    logger.info(f"User {db_user.user_id} received notes for {subject_text}.")

async def handle_cheat_sheets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user to select a cheat sheet type."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for cheat sheets.")
        return

    # PREMIUM CHECK for Cheat Sheets (redundant if handle_resource_selection already checks, but safe)
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to access Cheat Sheets directly.")
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

    # Map display names (with emojis) to internal keys for folder IDs
    subject_map = {
        "🧮 Math Formulas": "math_cheats",
        "📝 English Tips": "english_cheats",
        "⚛ Physics Formulas": "physics_cheats",
        "🧬 Biology Cheats": "biology_cheats",
        "🧪 Chemistry Cheats": "chemistry_cheats",
        "🧠 Aptitude Tricks": "aptitude_cheats",
        "🗺 Geography Cheats": "geography_cheats",
        "📜 History Cheats": "history_cheats",
        "💹 Economics Cheats": "economics_cheats"
    }

    # Get the folder key suffix based on the exact input text
    folder_key_suffix = subject_map.get(text)
    if not folder_key_suffix:
        await update.message.reply_text("Invalid cheat sheet selection.")
        logger.warning(f"User {user.id} sent invalid cheat sheet selection: {text}")
        return

    folder_key = f"{db_user.stream}_{folder_key_suffix}"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Cheat sheets not available for {text.replace('🧮 ', '').replace('📝 ', '').replace('⚛ ', '').replace('🧬 ', '').replace('🧪 ', '').replace('🧠 ', '').replace('🗺 ', '').replace('📜 ', '').replace('💹 ', '')} yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text("No cheat sheets found.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return

    # Extract the display name by removing the emoji prefix
    display_name = text.replace('🧮 ', '').replace('📝 ', '').replace('⚛ ', '').replace('🧬 ', '').replace('🧪 ', '').replace('🧠 ', '').replace('🗺 ', '').replace('📜 ', '').replace('💹 ', '')
    message = f"📚 {display_name}:\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.resources_menu())
    logger.info(f"User {user.id} received cheat sheets for {display_name}.")