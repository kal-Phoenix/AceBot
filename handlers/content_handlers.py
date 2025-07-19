# handlers/content_handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from config import Config
from keyboards import Keyboards
from handlers import user_handlers  # For calling start() on error

logger = logging.getLogger(__name__)
drive_service = GoogleDriveService()
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"

# --- NEW: Sample quiz data structure ---
# In a real application, this might come from a JSON file or a database.
DUMMY_QUIZZES = {
    'natural_mathematics': [
        {
            'question': "What is the value of π (pi) to two decimal places?",
            'options': ["3.12", "3.14", "3.16", "3.18"],
            'correct_option_id': 1
        },
        {
            'question': "What is the square root of 64?",
            'options': ["6", "7", "8", "9"],
            'correct_option_id': 2
        }
    ],
    'social_history': [
        {
            'question': "In which century did the Battle of Adwa take place?",
            'options': ["18th", "19th", "20th"],
            'correct_option_id': 1
        }
    ]
}


# --- END NEW ---


async def handle_quizzes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user to select a subject for quizzes."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for quizzes menu.")
        return

    # PREMIUM CHECK for Quizzes
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to access Quizzes.")
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
    """Processes the selected subject for quizzes and provides interactive quiz polls."""
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {db_user.user_id} attempted to process Quizzes selection.")
        return

    # Map display names to internal keys for the quiz data
    subject_key_map = {
        "mathematics": "mathematics",
        "history": "history",
        # Add other subjects here as quizzes are created
    }

    subject_key = subject_key_map.get(subject_text.lower())
    if not subject_key:
        await update.message.reply_text(
            f"Interactive quizzes for {subject_text.capitalize()} are not yet available. Please check back later.",
            reply_markup=Keyboards.main_menu())
        return

    quiz_key = f"{db_user.stream}_{subject_key}"
    questions = DUMMY_QUIZZES.get(quiz_key)

    if not questions:
        await update.message.reply_text("No quizzes found for this subject.", reply_markup=Keyboards.main_menu())
        logger.info(f"No quiz data found for key {quiz_key} for user {db_user.user_id}.")
        return

    await update.message.reply_text(f"🧠 Here are your {subject_text.capitalize()} quizzes. Good luck!",
                                    reply_markup=Keyboards.main_menu())

    for quiz_item in questions:
        try:
            await context.bot.send_poll(
                chat_id=db_user.user_id,
                question=quiz_item['question'],
                options=quiz_item['options'],
                type='quiz',
                correct_option_id=quiz_item['correct_option_id'],
                is_anonymous=False
            )
        except Exception as e:
            logger.error(f"Failed to send poll to user {db_user.user_id}: {e}")

    logger.info(f"User {db_user.user_id} received interactive quizzes for {subject_text}.")


async def handle_past_exams_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the menu for past exam years."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
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

    # PREMIUM CHECK for specific Past Exam Years (2014, 2015, 2016, 2017)
    if year in [2014, 2015, 2016, 2017] and not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {db_user.user_id} attempted to access premium exam year {year}.")
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
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for exam tips.")
        return

    # PREMIUM CHECK for Exam Tips
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to access Exam Tips.")
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
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for study tips.")
        return

    # PREMIUM CHECK for Study Tips
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {user.id} attempted to access Study Tips.")
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