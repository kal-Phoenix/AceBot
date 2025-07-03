# handlers/user_handlers.py
import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from services.gemini_ai import GeminiService
from config import Config, MenuItems as MI
from keyboards import Keyboards
from utils.speeches import SPEECHES
from handlers import payment_handlers  # Import payment_handlers for upgrade button

logger = logging.getLogger(__name__)

# Initialize services globally or pass them around if preferred
drive_service = GoogleDriveService()
gemini_service = GeminiService()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Welcomes user and prompts for stream selection or shows main menu."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user:
        # Create a new user if they don't exist in the database
        db_user = User(user_id=user.id, username=user.username)
        db_user.save()
        logger.info(f"New user created: {user.id} ({user.username})")

    # If user hasn't selected a stream, prompt them
    if not db_user.stream:
        reply_keyboard = [["Natural", "Social"]]
        await update.message.reply_text(
            "Welcome! Please select your stream:",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,  # Hide keyboard after selection
                resize_keyboard=True
            )
        )
        logger.info(f"User {user.id} prompted for stream selection.")
        return

    # If stream is already set, show the main menu
    await update.message.reply_text(
        f"Hello {user.first_name}! Choose an option:",
        reply_markup=Keyboards.main_menu()
    )
    logger.info(f"User {user.id} shown main menu.")


async def handle_stream_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's selection of 'Natural' or 'Social' stream."""
    user = update.effective_user
    stream = update.message.text.lower()  # Get the selected stream (e.g., "natural")

    if stream not in ["natural", "social"]:
        await update.message.reply_text("Please select Natural or Social")
        logger.warning(f"User {user.id} sent invalid stream selection: {stream}")
        return

    db_user = User.find(user.id)
    if db_user:
        db_user.stream = stream
        db_user.save()
        logger.info(f"User {user.id} stream set to {stream.capitalize()}.")
    else:
        # This case should ideally not happen if /start is always processed first
        db_user = User(user_id=user.id, username=user.username, stream=stream)
        db_user.save()
        logger.warning(f"User {user.id} not found, created with stream {stream}.")

    await update.message.reply_text(
        f"Stream set to {stream.capitalize()}! Choose an option:",
        reply_markup=Keyboards.main_menu()
    )


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
        await start(update, context)
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
        await handle_cheat_sheets(update, context)
        logger.info(f"User {user.id} selected Cheat Sheets.")
    elif text == "⬅️ Back to Main Menu":
        await start(update, context)  # Go back to main menu
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
        await start(update, context)
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
        await start(update, context)
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
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for short notes.")
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
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for cheat sheets.")
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
    text = update.message.text.lower()

    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for cheat sheet selection.")
        return

    # Map display names to internal keys for folder IDs
    subject_map = {
        "math formulas": "math_cheats",
        "english tips": "english_cheats",
        "physics formulas": "physics_cheats",
        "biology cheats": "biology_cheats",
        "chemistry cheats": "chemistry_cheats",
        "aptitude tricks": "aptitude_cheats",
        "geography cheats": "geography_cheats",
        "history cheats": "history_cheats",
        "economics cheats": "economics_cheats"
    }

    folder_key_suffix = subject_map.get(text)
    if not folder_key_suffix:
        await update.message.reply_text("Invalid cheat sheet selection.")
        logger.warning(f"User {user.id} sent invalid cheat sheet selection: {text}")
        return

    folder_key = f"{db_user.stream}_{folder_key_suffix}"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Cheat sheets not available for {text.capitalize()} yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text("No cheat sheets found.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return

    message = f"📚 {text.title()}:\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.resources_menu())
    logger.info(f"User {user.id} received cheat sheets for {text}.")


async def handle_quizzes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user to select a subject for quizzes."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for quizzes menu.")
        return

    # Set pending action for quiz subject selection
    db_user.pending_action = "select_quiz_subject"
    db_user.save()
    logger.info(f"User {user.id} set pending_action to 'select_quiz_subject'.")

    await update.message.reply_text(
        f"Select subject for {db_user.stream.capitalize()} stream quizzes:",
        reply_markup=Keyboards.quizzes_menu(db_user.stream)
    )


async def _process_quiz_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User,
                                          subject_text: str):
    """Processes the selected subject for quizzes and provides links."""
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
        await update.message.reply_text("Invalid subject selected for quizzes.")
        logger.warning(f"User {db_user.user_id} sent invalid quiz subject: {subject_text}")
        return

    folder_key = f"{db_user.stream}_{subject_key}_quizzes"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Quizzes not available for {subject_text.capitalize()} yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text("No quizzes found for this subject.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return

    message = f"🧠 {subject_text.capitalize()} Quizzes ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
    logger.info(f"User {db_user.user_id} received quizzes for {subject_text}.")


async def handle_past_exams_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the menu for past exam years."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for past exams menu.")
        return

    # Set pending action for past exam year selection
    db_user.pending_action = "select_exam_year"
    db_user.save()
    logger.info(f"User {user.id} set pending_action to 'select_exam_year'.")

    await update.message.reply_text(
        "Select exam year:",
        reply_markup=Keyboards.past_exams_years_menu()
    )
    logger.info(f"User {user.id} shown past exams year menu.")


async def _process_past_exam_year_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User,
                                            year_text: str):
    """Processes the selected exam year and provides links to the past exam."""
    try:
        year = int(year_text)
        if not (2000 <= year <= 2017):
            await update.message.reply_text("Invalid year selected. Please choose a year between 2000 and 2017.")
            logger.warning(f"User {db_user.user_id} sent invalid exam year: {year_text}")
            return
    except ValueError:
        await update.message.reply_text("Invalid year format. Please select a year from the menu.")
        logger.warning(f"User {db_user.user_id} sent non-integer exam year: {year_text}")
        return

    # Construct the key for Config.DRIVE_FOLDER_IDS
    folder_key = f"{db_user.stream}_{year}_exam"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Past exam for {year} not available for {db_user.stream.capitalize()} stream yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text(f"No past exam files found for {year}.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return

    message = f"📚 Past Exam {year} ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
    logger.info(f"User {db_user.user_id} received past exam for {year}.")


async def handle_exam_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches and displays exam tips based on the user's stream."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for exam tips.")
        return

    folder_key = f"{db_user.stream}_exam_tips"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Exam tips not available for {db_user.stream.capitalize()} stream yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {user.id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text(f"No exam tips found for {db_user.stream.capitalize()} stream.")
        logger.info(f"No files found in folder {folder_id} for user {user.id}.")
        return

    message = f"💡 Exam Tips ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
    logger.info(f"User {user.id} received exam tips.")


async def handle_study_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches and displays study tips based on the user's stream."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for study tips.")
        return

    folder_key = f"{db_user.stream}_study_tips"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)

    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Study tips not available for {db_user.stream.capitalize()} stream yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {user.id}.")
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text(f"No study tips found for {db_user.stream.capitalize()} stream.")
        logger.info(f"No files found in folder {folder_id} for user {user.id}.")
        return

    message = f"📖 Study Tips ({db_user.stream.capitalize()}):\n\n"
    for file in files:
        message += f"📄 {file['name']}\n🔗 {file['webViewLink']}\n\n"

    await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
    logger.info(f"User {user.id} received study tips.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all general text messages, routing them based on current user state (pending_action)
    or menu selections.
    """
    text = update.message.text
    user = update.effective_user
    db_user = User.find(user.id)

    # Ensure user and stream are set, otherwise restart the flow
    if not db_user or not db_user.stream:
        await start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for general message.")
        return

    # Define common_subjects here so it's always accessible
    common_subjects = ["Mathematics", "English", "Physics", "Biology", "Chemistry", "Aptitude",
                       "Geography", "History", "Economics"]

    # Handle main menu item selections first
    if text == MI.RESOURCES:
        await handle_resources(update, context)
    elif text == MI.QUIZZES:
        await handle_quizzes_menu(update, context)
    elif text == MI.MOTIVATION:
        selected_speech = random.choice(SPEECHES)

        # Format the speech with quote and author
        if ' - ' in selected_speech:
            parts = selected_speech.rsplit(' - ', 1)
            quote = parts[0].strip()
            author = parts[1].strip()
            message = f"💬 \"{quote}\"\n\n— {author}"
        else:
            message = f"💬 \"{selected_speech}\""  # Fallback if no author is present

        await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested motivation.")
    elif text == MI.AI_CHAT:
        # Set pending action for AI chat
        db_user.pending_action = "ai_chat"
        db_user.save()
        # Show only the AI chat menu
        await update.message.reply_text("🤖 Ask me anything about your subjects! Type your question:",
                                        reply_markup=Keyboards.ai_chat_menu())
        logger.info(f"User {user.id} entered AI chat mode.")
    elif text == MI.PAST_EXAMS:
        await handle_past_exams_menu(update, context)  # Route to new handler for past exams
        logger.info(f"User {user.id} requested past exams menu.")
    elif text == MI.EXAM_TIPS:
        await handle_exam_tips(update, context)  # Route to new handler for exam tips
        logger.info(f"User {user.id} requested exam tips.")
    elif text == MI.STUDY_TIPS:
        await handle_study_tips(update, context)  # Route to new handler for study tips
        logger.info(f"User {user.id} requested study tips.")
    elif text == MI.ASSIGNMENT_HELP:
        await update.message.reply_text("Assignment help coming soon! ✍️", reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested assignment help.")
    elif text == MI.UPGRADE:
        # This will trigger the upgrade_command handler via main.py's CommandHandler
        await payment_handlers.upgrade_command(update, context)
        logger.info(f"User {user.id} requested upgrade.")
    elif text == MI.HELP:
        await update.message.reply_text("For assistance, please contact support. 🆘", reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested help.")
    elif text == MI.CONTACT_US:
        await update.message.reply_text("You can reach us at support@acebot.com 📧", reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested contact info.")
    elif text == MI.SHORT_NOTES:  # Explicitly handle Short Notes here
        await handle_short_notes(update, context)
        logger.info(f"User {user.id} requested short notes menu.")
    elif text == MI.TEXT_BOOKS:  # NEW: Explicitly handle Text Books here
        await handle_text_books_menu(update, context)
        logger.info(f"User {user.id} requested text books menu.")
    elif text == "⬅️ Back to Main Menu":
        db_user.pending_action = None  # Clear any pending action
        db_user.save()
        await start(update, context)  # Effectively go back to main menu
        logger.info(f"User {user.id} navigated back to main menu.")
    elif text == "⬅️ Back to Resources":
        db_user.pending_action = None  # Clear any pending action
        db_user.save()
        await handle_resources(update, context)  # Go back to resources menu
        logger.info(f"User {user.id} navigated back to resources menu.")
    elif text == MI.EXIT_AI_CHAT:  # Handle exiting AI chat mode
        db_user.pending_action = None  # Clear AI chat pending action
        db_user.save()
        await update.message.reply_text("👋 Exiting AI Chat. How else can I help you?",
                                        reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} exited AI chat mode.")
    # Now, check for pending actions that expect a specific type of text input
    elif db_user.pending_action == "select_exam_year" and text.isdigit():
        await _process_past_exam_year_selection(update, context, db_user, text)
        db_user.pending_action = None  # Clear pending action after processing
        db_user.save()
        logger.info(f"User {user.id} processed pending action 'select_exam_year' with year '{text}'.")
    elif text in common_subjects and db_user.pending_action:
        if db_user.pending_action == "select_notes_subject":
            await _process_notes_subject_selection(update, context, db_user, text.lower())
        elif db_user.pending_action == "select_quiz_subject":
            await _process_quiz_subject_selection(update, context, db_user, text.lower())

        # Clear pending action after processing
        db_user.pending_action = None
        db_user.save()
        logger.info(f"User {user.id} processed pending action '{db_user.pending_action}' with subject '{text}'.")
    elif db_user.pending_action == "ai_chat":
        # If in AI chat mode, send message to Gemini
        await update.message.reply_chat_action("typing")  # This sends the "typing..." status
        await update.message.reply_text("Typing... ✍️", reply_markup=Keyboards.ai_chat_menu())  # Keep AI menu
        response_text = await gemini_service.chat_with_gemini(user.id, text)  # Call without history
        await update.message.reply_text(response_text, reply_markup=Keyboards.ai_chat_menu())  # Keep AI menu
        logger.info(f"User {user.id} received AI response.")
        # Keep pending_action as 'ai_chat' to continue conversation
    else:
        # Default response for unrecognized messages
        await update.message.reply_text(
            "I didn't understand that. Please choose from the menu options or type a command.",
            reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} sent unrecognized message: {text}")

