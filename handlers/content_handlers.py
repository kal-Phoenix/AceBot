# handlers/content_handlers.py
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from config import Config, MenuItems as MI
from keyboards import Keyboards
from handlers import user_handlers  # For calling start() on error

logger = logging.getLogger(__name__)
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"

# Initialize Google Drive service
drive_service = GoogleDriveService()




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
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            "🧠 *Quizzes* are exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Practice quizzes by grade\n"
            "• Subject-specific tests\n"
            "• Instant feedback\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
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

    # Determine grade parameter for channel search
    grade_param = "mixed" if mixed else f"grade{grade_value}"

    # Construct the key for Config.DRIVE_FOLDER_IDS
    if mixed:
        folder_key = f"{db_user.stream}_{subject_key}_mixed_quiz"
    else:
        folder_key = f"{db_user.stream}_{subject_key}_grade{grade_value}_quiz"
    
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)
    
    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Quizzes for {subject_key.capitalize()} {grade_text} not available for {db_user.stream.capitalize()} stream yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return
    
    files = drive_service.list_files(folder_id, is_premium_content=True)  # Quizzes are premium
    if not files:
        await update.message.reply_text(f"No quizzes found for {subject_key.capitalize()} {grade_text}.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return
    
    message = f"🧠 Quizzes - {subject_key.capitalize()} {grade_text} ({db_user.stream.capitalize()}):\n\n"
    buttons = []
    
    for file in files:
        message += f"📄 {file['name']}\n"
        
        # Add view button (quizzes are premium - view only, no download/screenshot)
        buttons.append([InlineKeyboardButton(f"👁️ View {file['name']}", url=file['view_only_url'])])
        message += "\n"

    await update.message.reply_text(
        message, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else Keyboards.main_menu()
    )
    logger.info(f"User {db_user.user_id} accessed quizzes for {subject_key} {grade_text}.")

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
    """Displays the menu for past exam organization options."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for past exams menu.")
        return

    # Set pending action for past exam organization selection
    db_user.pending_action = "select_exam_organization"
    db_user.save()
    logger.info(f"User {user.id} set pending_action to 'select_exam_organization'.")

    await update.message.reply_text(
        "How would you like to browse past exams?",
        reply_markup=Keyboards.past_exams_organization_menu()
    )
    logger.info(f"User {user.id} shown past exams organization menu.")


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
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            f"📚 *Past Exam {year}* is exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Recent exam papers\n"
            "• Answer keys\n"
            "• High-quality scans\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
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

    # Check if this is a premium year (2014-2017)
    is_premium_year = year in [2014, 2015, 2016, 2017]
    
    files = drive_service.list_files(folder_id, is_premium_content=is_premium_year)  # Premium years are restricted
    if not files:
        await update.message.reply_text(f"No past exam files found for {year}.")
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return
    
    message = f"📚 Past Exam {year} ({db_user.stream.capitalize()}):\n\n"
    buttons = []
    
    for file in files:
        message += f"📄 {file['name']}\n"
        
        # Add view button based on premium status
        if db_user.is_premium or not is_premium_year:
            buttons.append([InlineKeyboardButton(f"👁️ View {file['name']}", url=file['view_only_url'])])
        else:
            buttons.append([InlineKeyboardButton(f"💎 Upgrade to View {file['name']}", callback_data="upgrade")])
        message += "\n"

    await update.message.reply_text(
        message, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else Keyboards.main_menu()
    )
    logger.info(f"User {db_user.user_id} received past exam for {year}.")


async def _process_past_exam_organization_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User, organization_text: str):
    """Processes the selected organization method for past exams."""
    if organization_text == MI.ORGANIZED_BY_YEAR:
        # Set pending action for past exam year selection
        db_user.pending_action = "select_exam_year"
        db_user.save()
        logger.info(f"User {db_user.user_id} selected year-based organization.")
        
        await update.message.reply_text(
            "Select exam year:",
            reply_markup=Keyboards.past_exams_years_menu()
        )
        logger.info(f"User {db_user.user_id} shown past exams year menu.")
        
    elif organization_text == MI.ORGANIZED_BY_TOPICS:
        # Set pending action for past exam topic selection
        db_user.pending_action = "select_exam_topic"
        db_user.save()
        logger.info(f"User {db_user.user_id} selected topic-based organization.")
        
        await update.message.reply_text(
            "Select subject to browse past exams by topic:",
            reply_markup=Keyboards.past_exams_topics_menu(db_user.stream)
        )
        logger.info(f"User {db_user.user_id} shown past exams topics menu.")
    else:
        await update.message.reply_text("Invalid selection. Please choose from the menu options.")
        logger.warning(f"User {db_user.user_id} sent invalid organization selection: {organization_text}")


async def _process_past_exam_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user: User, topic_text: str):
    """Processes the selected topic for past exams and provides links to topic-based past exams."""
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
    
    subject_key = subject_map.get(topic_text.lower())
    if not subject_key:
        await update.message.reply_text("Invalid subject selected for past exams.")
        logger.warning(f"User {db_user.user_id} sent invalid topic selection: {topic_text}")
        return
    
    # Construct the key for Config.DRIVE_FOLDER_IDS
    folder_key = f"{db_user.stream}_{subject_key}_past_exams"
    folder_id = Config.DRIVE_FOLDER_IDS.get(folder_key)
    
    if not folder_id or folder_id.startswith("YOUR_"):  # Check for placeholder IDs
        await update.message.reply_text(
            f"Past exam for {topic_text.capitalize()} topics not available for {db_user.stream.capitalize()} stream yet. "
            f"Please ensure the Google Drive folder ID is configured correctly in config.py."
        )
        logger.info(f"No valid folder ID found or placeholder used for {folder_key} for user {db_user.user_id}.")
        return
    
    files = drive_service.list_files(folder_id)
    if not files:
        await update.message.reply_text(
            f"No past exam files found for {topic_text.capitalize()} topics yet.",
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"No files found in folder {folder_id} for user {db_user.user_id}.")
        return
    
    message = f"📚 Past Exams by Topic - {topic_text.capitalize()} ({db_user.stream.capitalize()}):\n\n"
    buttons = []
    
    for file in files:
        message += f"📄 {file['name']}\n"
        
        # Add view button (topic-based past exams use view_only_url)
        buttons.append([InlineKeyboardButton(f"👁️ View {file['name']}", url=file['view_only_url'])])
        message += "\n"
    
    await update.message.reply_text(
        message, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else Keyboards.main_menu()
    )
    logger.info(f"User {db_user.user_id} received topic-based past exams for {topic_text}.")


async def handle_exam_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches and displays exam tips based on the user's stream."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for exam tips.")
        return

    # PREMIUM CHECK for Exam Tips - Block access entirely for non-premium users
    if not db_user.is_premium:
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            "💡 *Exam Tips* are exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Proven exam strategies\n"
            "• Time management tips\n"
            "• Success techniques\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
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

    files = drive_service.list_files(folder_id, is_premium_content=True)  # Exam tips are premium
    if not files:
        await update.message.reply_text(f"No exam tips found for {db_user.stream.capitalize()} stream.")
        logger.info(f"No files found in folder {folder_id} for user {user.id}.")
        return

    message = f"💡 Exam Tips ({db_user.stream.capitalize()}):\n\n"
    buttons = []
    
    for file in files:
        message += f"📄 {file['name']}\n"
        
        # Add view button (exam tips are premium - use view_only_url)
        buttons.append([InlineKeyboardButton(f"👁️ View {file['name']}", url=file['view_only_url'])])
        message += "\n"

    await update.message.reply_text(
        message, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else Keyboards.main_menu()
    )
    logger.info(f"User {user.id} received exam tips.")


async def handle_study_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches and displays study tips based on the user's stream."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await user_handlers.start(update, context)
        logger.warning(f"User {user.id} inconsistent state, restarting flow for study tips.")
        return

    # PREMIUM CHECK for Study Tips - Block access entirely for non-premium users
    if not db_user.is_premium:
        await update.message.reply_text(
            "✨ *Premium Content* ✨\n\n"
            "📖 *Study Tips* are exclusive to our premium members!\n\n"
            "🎯 *What you'll get:*\n"
            "• Effective study methods\n"
            "• Learning strategies\n"
            "• Productivity tips\n\n"
            "💎 *Upgrade to Premium* to unlock this content and much more!\n\n"
            "🚀 Ready to boost your studies?",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
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

    files = drive_service.list_files(folder_id, is_premium_content=True)  # Study tips are premium
    if not files:
        await update.message.reply_text(f"No study tips found for {db_user.stream.capitalize()} stream.")
        logger.info(f"No files found in folder {folder_id} for user {user.id}.")
        return

    message = f"📖 Study Tips ({db_user.stream.capitalize()}):\n\n"
    buttons = []
    
    for file in files:
        message += f"📄 {file['name']}\n"
        
        # Add view button (study tips are premium - use view_only_url)
        buttons.append([InlineKeyboardButton(f"👁️ View {file['name']}", url=file['view_only_url'])])
        message += "\n"

    await update.message.reply_text(
        message, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else Keyboards.main_menu()
    )
    logger.info(f"User {user.id} received study tips.")