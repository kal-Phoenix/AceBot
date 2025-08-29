# handlers/content_handlers.py
import logging
import random
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


async def _process_quiz_grade_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User, grade_text: str):
    """After grade selection, fetch one quiz from Drive and show post options."""
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        return

    subject_key = context.user_data.get("quiz_subject")
    if not subject_key:
        await handle_quizzes_menu(update, context)
        return

    # Determine grade filter
    grade_value = None
    if grade_text.startswith("Grade "):
        try:
            grade_value = int(grade_text.split()[1])
        except Exception:
            grade_value = None
    mixed = grade_text.lower() == "mixed"

    # Build Drive folder key
    folder_key = f"{db_user.stream}_{subject_key}_quizzes"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)
    if not folder_id or folder_id.startswith("YOUR_"):
        await update.message.reply_text(
            "Quizzes not available yet for this subject. Configure Drive folder IDs.",
            reply_markup=Keyboards.main_menu()
        )
        return

    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text("No quiz files found.")
        return

    # Filter by grade if possible (simple filename contains strategy)
    candidates = files
    if not mixed and grade_value is not None:
        candidates = [f for f in files if str(grade_value) in f.get('name', '')] or files

    selected = random.choice(candidates)
    name = selected.get('name')
    link = selected.get('webViewLink') or selected.get('id')

    await update.message.reply_text(
        f"📄 {name}\n🔗 {link}",
        reply_markup=Keyboards.quiz_post_menu()
    )

    db_user.pending_action = "quiz_post_options"
    db_user.save()

async def _process_quiz_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User,
                                          subject_text: str):
    """Processes subject, then prompts user to choose a grade for the quiz."""
    if not db_user.is_premium:
        await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
        logger.info(f"Non-premium user {db_user.user_id} attempted to process Quizzes selection.")
        return

    subject_key_map = {
        "mathematics": "math",
        "english": "english",
        "physics": "physics",
        "biology": "biology",
        "chemistry": "chemistry",
        "aptitude": "aptitude",
        "geography": "geography",
        "history": "history",
        "economics": "economics",
    }

    subject_key = subject_key_map.get(subject_text.lower())
    if not subject_key:
        await update.message.reply_text(
            f"Quizzes for {subject_text.capitalize()} are not yet available.",
            reply_markup=Keyboards.main_menu())
        return

    # Save and prompt for grade selection
    context.user_data["quiz_subject"] = subject_key
    db_user.pending_action = "select_quiz_grade"
    db_user.save()
    await update.message.reply_text(
        "Choose the grade for the quiz:",
        reply_markup=Keyboards.quiz_grades_menu()
    )


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