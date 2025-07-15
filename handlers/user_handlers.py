# handlers/user_handlers.py
import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.models import User
from services.google_drive import GoogleDriveService
from services.gemini_ai import GeminiService
from config import MenuItems as MI
from keyboards import Keyboards
from utils.speeches import SPEECHES
from handlers import payment_handlers, resource_handlers, content_handlers

logger = logging.getLogger(__name__)

# Initialize services globally or pass them around if preferred
drive_service = GoogleDriveService()
gemini_service = GeminiService()

# Define the premium message
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"

# Define your username and assignment help description
YOUR_USERNAME = "@YourUsername"  # Replace with your actual Telegram username
ASSIGNMENT_HELP_DESCRIPTION = (
    "🌟 Assignment Help for Entrance Exams 🌟\n"
    "We know entrance exam prep can feel overwhelming, but don’t stress! We’re here to support you with personalized assistance. "
    "Contact me for help with assignments or study tips tailored to your exam. Reach out at {} and let’s work together to succeed! 😊"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Welcomes user and prompts for stream selection or shows main menu."""
    user = update.effective_user
    db_user = User.find(user.id)

    # --- ADD THIS BLOCK TO HANDLE REFERRALS ---
    referral_code = None
    if context.args:
        try:
            potential_code = int(context.args[0])
            # Check if a user with this ID exists and is not the current user
            if potential_code != user.id and User.find(potential_code):
                 referral_code = potential_code
        except (ValueError, IndexError):
            pass # Ignore invalid codes
    # --- END OF BLOCK ---

    if not db_user:
        # Create a new user if they don't exist in the database
        db_user = User(user_id=user.id, username=user.username)
        # --- ADD THIS LINE TO SAVE THE REFERRER ---
        if referral_code:
            db_user.referred_by = referral_code
            logger.info(f"New user {user.id} was referred by {referral_code}.")
        # --- END OF LINE ---
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
        await resource_handlers.handle_resources(update, context)
    elif text == MI.QUIZZES:
        # PREMIUM CHECK for Quizzes
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access Quizzes from main menu.")
            return
        await content_handlers.handle_quizzes_menu(update, context)
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
        # PREMIUM CHECK for AI Chat initiation
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access AI Chat.")
            return

        # Set pending action for AI chat
        db_user.pending_action = "ai_chat"
        db_user.save()
        # Show only the AI chat menu
        await update.message.reply_text("🤖 Ask me anything about your subjects! Type your question:",
                                        reply_markup=Keyboards.ai_chat_menu())
        logger.info(f"User {user.id} entered AI chat mode.")
    elif text == MI.PAST_EXAMS:
        await content_handlers.handle_past_exams_menu(update, context)  # Route to new handler for past exams
        logger.info(f"User {user.id} requested past exams menu.")
    elif text == MI.EXAM_TIPS:
        # PREMIUM CHECK for Exam Tips
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access Exam Tips.")
            return
        await content_handlers.handle_exam_tips(update, context)  # Route to new handler for exam tips
        logger.info(f"User {user.id} requested exam tips.")
    elif text == MI.STUDY_TIPS:
        # PREMIUM CHECK for Study Tips
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access Study Tips.")
            return
        await content_handlers.handle_study_tips(update, context)  # Route to new handler for study tips
        logger.info(f"User {user.id} requested study tips.")
    elif text == MI.ASSIGNMENT_HELP:
        await update.message.reply_text(
            ASSIGNMENT_HELP_DESCRIPTION.format(YOUR_USERNAME),
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"User {user.id} requested assignment help.")
    elif text == MI.UPGRADE:
        # This will trigger the upgrade_command handler via main.py's MessageHandler regex
        await payment_handlers.upgrade_command(update, context)
        logger.info(f"User {user.id} requested upgrade.")
    elif text == MI.HELP:
        await update.message.reply_text("For assistance, please contact support. 🆘", reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested help.")
    elif text == MI.CONTACT_US:
        await update.message.reply_text("You can reach us at support@acebot.com 📧", reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} requested contact info.")
    elif text == MI.SHORT_NOTES:  # Explicitly handle Short Notes here
        # PREMIUM CHECK for Short Notes
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to access Short Notes from main menu.")
            return
        await resource_handlers.handle_short_notes(update, context)
        logger.info(f"User {user.id} requested short notes menu.")
    elif text == MI.TEXT_BOOKS:  # Explicitly handle Text Books here
        await resource_handlers.handle_text_books_menu(update, context)
        logger.info(f"User {user.id} requested text books menu.")
    elif text == "⬅️ Back to Main Menu":
        db_user.pending_action = None  # Clear any pending action
        db_user.save()
        await start(update, context)  # Effectively go back to main menu
        logger.info(f"User {user.id} navigated back to main menu.")
    elif text == "⬅️ Back to Resources":
        db_user.pending_action = None  # Clear any pending action
        db_user.save()
        await resource_handlers.handle_resources(update, context)  # Go back to resources menu
        logger.info(f"User {user.id} navigated back to resources menu.")
    elif text == MI.EXIT_AI_CHAT:  # Handle exiting AI chat mode
        db_user.pending_action = None  # Clear AI chat pending action
        db_user.save()
        await update.message.reply_text("👋 Exiting AI Chat. How else can I help you?",
                                        reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} exited AI chat mode.")
    # Now, check for pending actions that expect a specific type of text input
    elif db_user.pending_action == "select_exam_year" and text.isdigit():
        await content_handlers._process_past_exam_year_selection(update, context, db_user, text)
        db_user.pending_action = None  # Clear pending action after processing
        db_user.save()
        logger.info(f"User {user.id} processed pending action 'select_exam_year' with year '{text}'.")
    elif text in common_subjects and db_user.pending_action:
        if db_user.pending_action == "select_notes_subject":
            # PREMIUM CHECK for Short Notes subject selection (safe, but initial check is primary)
            if not db_user.is_premium:
                await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
                logger.info(f"Non-premium user {user.id} attempted to process Short Notes subject selection.")
                db_user.pending_action = None # Clear action
                db_user.save()
                return
            await resource_handlers._process_notes_subject_selection(update, context, db_user, text.lower())
        elif db_user.pending_action == "select_quiz_subject":
            # PREMIUM CHECK for Quiz subject selection (safe, but initial check is primary)
            if not db_user.is_premium:
                await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
                logger.info(f"Non-premium user {user.id} attempted to process Quiz subject selection.")
                db_user.pending_action = None # Clear action
                db_user.save()
                return
            await content_handlers._process_quiz_subject_selection(update, context, db_user, text.lower())

        # Clear pending action after processing
        db_user.pending_action = None
        db_user.save()
        logger.info(f"User {user.id} processed pending action '{db_user.pending_action}' with subject '{text}'.")
    elif db_user.pending_action == "ai_chat":
        # PREMIUM CHECK for AI chat continued interaction (safe, but initial check is primary)
        if not db_user.is_premium:
            await update.message.reply_text(PREMIUM_MESSAGE, reply_markup=Keyboards.main_menu())
            logger.info(f"Non-premium user {user.id} attempted to continue AI Chat (lost premium?).")
            db_user.pending_action = None # Clear action
            db_user.save()
            return

        # If in AI chat mode, send message to Gemini without history
        await update.message.reply_chat_action("typing")  # This sends the "typing..." status
        response_text = await gemini_service.chat_with_gemini(user.id, text)
        await update.message.reply_text(response_text, reply_markup=Keyboards.ai_chat_menu())  # Keep AI menu
        logger.info(f"User {user.id} received AI response.")
        # Keep pending_action as 'ai_chat' to continue conversation (each turn is fresh)
    # NEW: Payment related pending actions for text input
    elif db_user.pending_action == "await_payment_status_choice":
        await payment_handlers.handle_payment_status_choice(update, context)
        logger.info(f"User {user.id} handled payment status choice.")
    elif db_user.pending_action == "await_name_for_payment":
        await payment_handlers.process_name_for_payment(update, context)
        logger.info(f"User {user.id} processed name for payment.")
    else:
        # Default response for unrecognized messages
        await update.message.reply_text(
            "I didn't understand that. Please choose from the menu options or type a command.",
            reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} sent unrecognized message: {text}")