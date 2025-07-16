# handlers/user_handlers.py
import random
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from services.gemini_ai import GeminiService
from config import Config, MenuItems as MI
from keyboards import Keyboards
from utils.speeches import SPEECHES
from handlers import payment_handlers, resource_handlers, content_handlers, invite_handlers

logger = logging.getLogger(__name__)

# Initialize services
drive_service = GoogleDriveService()
gemini_service = GeminiService()

# Define messages
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"
YOUR_USERNAME = "@YourUsername"
ASSIGNMENT_HELP_DESCRIPTION = (
    "🌟 Assignment Help for Entrance Exams 🌟\n"
    "We know entrance exam prep can feel overwhelming, but don’t stress! We’re here to support you with personalized assistance. "
    "Contact me for help with assignments or study tips tailored to your exam. Reach out at {} and let’s work together to succeed! 😊"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Welcomes user and prompts for stream selection or shows main menu."""
    user = update.effective_user
    db_user = User.find(user.id)
    referral_code = None
    if context.args:
        try:
            potential_code = int(context.args[0])
            if potential_code != user.id and User.find(potential_code):
                referral_code = potential_code
        except (ValueError, IndexError):
            pass

    if not db_user:
        db_user = User(user_id=user.id, username=user.username)
        if referral_code:
            db_user.referred_by = referral_code
            logger.info(f"New user {user.id} was referred by {referral_code}.")
        db_user.save()
        logger.info(f"New user created: {user.id} ({user.username})")

    if not db_user.stream:
        reply_keyboard = [["Natural", "Social"]]
        await update.message.reply_text(
            "Welcome! Please select your stream:",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
        logger.info(f"User {user.id} prompted for stream selection.")
        return

    db_user.pending_action = None
    db_user.save()
    await update.message.reply_text(
        f"Hello {user.first_name}! Choose an option:",
        reply_markup=Keyboards.main_menu()
    )
    logger.info(f"User {user.id} shown main menu.")


async def handle_stream_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's selection of 'Natural' or 'Social' stream."""
    user = update.effective_user
    stream = update.message.text.lower()

    if stream not in ["natural", "social"]:
        await update.message.reply_text("Please select Natural or Social")
        return

    db_user = User.find(user.id)
    if db_user:
        db_user.stream = stream
        db_user.save()
    else:
        db_user = User(user_id=user.id, username=user.username, stream=stream)
        db_user.save()

    await update.message.reply_text(
        f"Stream set to {stream.capitalize()}! Choose an option:",
        reply_markup=Keyboards.main_menu()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all general text messages, routing them based on current user state or menu selections.
    """
    text = update.message.text
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or not db_user.stream:
        await start(update, context)
        return

    common_subjects = ["Mathematics", "English", "Physics", "Biology", "Chemistry", "Aptitude",
                       "Geography", "History", "Economics"]

    # Handle main menu item selections
    if text == MI.RESOURCES:
        await resource_handlers.handle_resources(update, context)
    elif text == MI.QUIZZES:
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            return
        await content_handlers.handle_quizzes_menu(update, context)
    elif text == MI.MOTIVATION:
        selected_speech = random.choice(SPEECHES)
        if ' - ' in selected_speech:
            parts = selected_speech.rsplit(' - ', 1)
            message = f"💬 \"{parts[0].strip()}\"\n\n— {parts[1].strip()}"
        else:
            message = f"💬 \"{selected_speech}\""
        await update.message.reply_text(message, reply_markup=Keyboards.main_menu())
    elif text == MI.AI_CHAT:
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            return
        db_user.pending_action = "ai_chat"
        db_user.save()
        await update.message.reply_text("🤖 Ask me anything about your subjects! Type your question:",
                                        reply_markup=Keyboards.ai_chat_menu())
    elif text == MI.PAST_EXAMS:
        await content_handlers.handle_past_exams_menu(update, context)
    elif text == MI.EXAM_TIPS:
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            return
        await content_handlers.handle_exam_tips(update, context)
    elif text == MI.STUDY_TIPS:
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            return
        await content_handlers.handle_study_tips(update, context)
    elif text == MI.ASSIGNMENT_HELP:
        await update.message.reply_text(ASSIGNMENT_HELP_DESCRIPTION.format(YOUR_USERNAME),
                                        reply_markup=Keyboards.main_menu())
    elif text == MI.UPGRADE:
        await payment_handlers.upgrade_command(update, context)
    # --- NEW: Route to Invite & Earn Menu ---
    elif text == MI.INVITE_AND_EARN:
        await invite_handlers.handle_invite_menu(update, context)
    # --- END NEW ---
    elif text == MI.HELP:
        await update.message.reply_text("For assistance, please contact support. 🆘", reply_markup=Keyboards.main_menu())
    elif text == MI.CONTACT_US:
        await update.message.reply_text("You can reach us at support@acebot.com 📧", reply_markup=Keyboards.main_menu())
    elif text == MI.SHORT_NOTES:
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            return
        await resource_handlers.handle_short_notes(update, context)
    elif text == MI.TEXT_BOOKS:
        await resource_handlers.handle_text_books_menu(update, context)
    elif text == MI.BACK_TO_MAIN_MENU or text == "⬅️ Back to Main Menu":
        await start(update, context)
    elif text == "⬅️ Back to Resources":
        await resource_handlers.handle_resources(update, context)
    elif text == MI.EXIT_AI_CHAT:
        db_user.pending_action = None
        db_user.save()
        await update.message.reply_text("👋 Exiting AI Chat. How else can I help you?",
                                        reply_markup=Keyboards.main_menu())

    # --- NEW: Handle Invite & Withdrawal flow ---
    elif text == MI.SHARE_INVITE:
        await invite_handlers.handle_share_request(update, context)
    elif text == MI.REQUEST_WITHDRAWAL:
        await invite_handlers.handle_withdraw_request(update, context)
    # --- END NEW ---

    # Handle pending actions
    elif db_user.pending_action == "awaiting_bank_for_withdrawal" and text in Config.AVAILABLE_BANKS:
        await invite_handlers.handle_bank_selection(update, context)
    elif db_user.pending_action == "awaiting_account_number_for_withdrawal":
        await invite_handlers.handle_account_number(update, context)
    elif db_user.pending_action == "await_payment_status_choice":
        await payment_handlers.handle_payment_status_choice(update, context)
    elif db_user.pending_action == "await_name_for_payment":
        await payment_handlers.process_name_for_payment(update, context)
    elif db_user.pending_action == "select_exam_year" and text.isdigit():
        await content_handlers._process_past_exam_year_selection(update, context, db_user, text)
        db_user.pending_action = None
        db_user.save()
    elif text in common_subjects and db_user.pending_action in ["select_notes_subject", "select_quiz_subject"]:
        if db_user.pending_action == "select_notes_subject":
            if not db_user.is_premium:
                await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            else:
                await resource_handlers._process_notes_subject_selection(update, context, db_user, text.lower())
        elif db_user.pending_action == "select_quiz_subject":
            if not db_user.is_premium:
                await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            else:
                await content_handlers._process_quiz_subject_selection(update, context, db_user, text.lower())
        db_user.pending_action = None
        db_user.save()
    elif db_user.pending_action == "ai_chat":
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            db_user.pending_action = None
            db_user.save()
            return
        await update.message.reply_chat_action("typing")
        response_text = await gemini_service.chat_with_gemini(user.id, text)
        await update.message.reply_text(response_text, reply_markup=Keyboards.ai_chat_menu())
    else:
        # Default response for unrecognized messages when no pending action matches
        if not db_user.pending_action:
            await update.message.reply_text(
                "I didn't understand that. Please choose from the menu options.",
                reply_markup=Keyboards.main_menu())
            logger.info(f"User {user.id} sent unrecognized message: {text}")