# handlers/user_handlers.py
import random
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.models import User
from services.telegram_channel import TelegramChannelService
from services.gemini_ai import GeminiService
from config import Config, MenuItems as MI
from keyboards import Keyboards
from utils.speeches import SPEECHES
from handlers import payment_handlers, resource_handlers, content_handlers, invite_handlers

logger = logging.getLogger(__name__)

# Initialize services
channel_service = TelegramChannelService()
gemini_service = GeminiService()

# Define messages
PREMIUM_MESSAGE = "This feature is for premium users only. Please upgrade to access this content. Tap '💎 Upgrade' from the main menu to learn more!"
ASSIGNMENT_HELP_DESCRIPTION = (
    "📚 Academic Support Services 📚\n\n"
    "Struggling with challenging assignments or need guidance on exam preparation? Our experienced academic support team is here to provide personalized assistance tailored to your specific needs.\n\n"
    "We offer:\n"
    "• Assignment guidance and problem-solving strategies\n"
    "• Subject-specific study techniques\n"
    "• Exam preparation tips and best practices\n"
    "• Concept clarification and learning support\n\n"
    "For professional academic assistance, please contact our support team at @WAGM12345\n\n"
    "Let us help you achieve your academic goals! 🎯"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Welcomes user and prompts for stream selection or shows main menu."""
    user = update.effective_user
    db_user = User.find(user.id)

    # Enforce user blocking
    if db_user and db_user.blocked:
        await update.message.reply_text("Your account has been suspended. Please contact support.")
        logger.warning(f"Blocked user {user.id} tried to use /start.")
        return

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

    # Enforce user blocking
    if db_user and db_user.blocked:
        await update.message.reply_text("Your account has been suspended. Please contact support.")
        logger.warning(f"Blocked user {user.id} tried to send a message: {text}")
        return

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
        await update.message.reply_text(ASSIGNMENT_HELP_DESCRIPTION,
                                        reply_markup=Keyboards.main_menu())
    elif text == MI.UPGRADE:
        await payment_handlers.upgrade_command(update, context)
    elif text == MI.INVITE_AND_EARN:
        await invite_handlers.handle_invite_menu(update, context)
    elif text == MI.HELP:
        help_text = (
            "✨ *Welcome to the AceBot Assistant* ✨\n\n"
            "Hello\\! I'm here to help you ace your university entrance exams\\. Here is a breakdown of my features:\n\n"
            "*Main Features*:\n\n"
            "📚 *Resources* — Access a rich library of Textbooks, Teacher's Guides, and more\\. \n"
            "📝 *Past Exams* — Practice with official past examination papers from previous years\\. \n"
            "✨ *Motivation* — Get a dose of inspiration to keep you focused and driven\\.\n\n"
            "*Premium Features* \\(💎\\):\n\n"
            "🧠 *Interactive Quizzes* — Test your knowledge with subject\\-specific quizzes\\.\n"
            "🤖 *AI Tutor* — Get instant, 24/7 help with difficult concepts from our advanced AI chat\\. \n"
            "💡 *Study & Exam Tips* — Unlock exclusive strategies and tips to study smarter\\. \n"
            "📝 *Short Notes & Cheat Sheets* — Access condensed study materials for quick revision\\.\n\n"
            "*Community & Support*:\n\n"
            "🤝 *Invite & Earn* — Share the bot with friends to earn rewards\\!\n"
            "📧 *Contact Us* — Have a question or feedback? We're here to help\\. \n\n"
            "Navigate using the menu below\\. For a fresh start, you can always type /start\\."
        )
        await update.message.reply_text(help_text, parse_mode='MarkdownV2', reply_markup=Keyboards.main_menu())

    elif text == MI.CONTACT_US:
        contact_text = (
            "*Contact Support* 📞\n\n"
            "We are committed to providing exceptional support and assistance to our users\\. Our dedicated support team is available to address your inquiries, technical issues, and feedback\\.\n\n"
            "*About AceBot*:\n"
            "AceBot is developed by Kaleab Dereje and the Phoenix Team from Addis Ababa University \\(AAU\\), with the mission to enhance educational outcomes for Ethiopian university entrance exam candidates\\.\n\n"
            "*Support Channels*:\n\n"
            "• *Telegram Support*: @a\\_d\\_min\\_support\n"
            "• *Email Support*: kaleabnt369@gmail\\.com\n\n"
            "For the fastest response, please use Telegram support\\. We typically respond within 24 hours\\.\n\n"
            "Thank you for choosing AceBot for your educational journey\\! 🎓"
        )
        await update.message.reply_text(contact_text, parse_mode='MarkdownV2', reply_markup=Keyboards.main_menu())

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

    elif text == MI.SHARE_INVITE:
        await invite_handlers.handle_share_request(update, context)
    elif text == MI.REQUEST_WITHDRAWAL:
        await invite_handlers.handle_withdraw_request(update, context)

    # Handle pending actions
    elif db_user.pending_action == "awaiting_bank_for_withdrawal" and text in Config.AVAILABLE_BANKS:
        await invite_handlers.handle_bank_selection(update, context)
    elif db_user.pending_action == "awaiting_account_number_for_withdrawal":
        await invite_handlers.handle_account_number(update, context)
    elif db_user.pending_action == "awaiting_account_holder_for_withdrawal":
        await invite_handlers.handle_account_holder(update, context)
    elif db_user.pending_action == "await_payment_status_choice":
        await payment_handlers.handle_payment_status_choice(update, context)
    elif db_user.pending_action == "await_name_for_payment":
        await payment_handlers.process_name_for_payment(update, context)
    elif db_user.pending_action == "select_exam_organization" and text in [MI.ORGANIZED_BY_YEAR, MI.ORGANIZED_BY_TOPICS]:
        await content_handlers._process_past_exam_organization_selection(update, context, db_user, text)
    elif db_user.pending_action == "select_exam_year" and text.isdigit():
        # Keep pending_action so user can choose multiple years in the same menu
        await content_handlers._process_past_exam_year_selection(update, context, db_user, text)
    elif db_user.pending_action == "select_exam_topic" and text in common_subjects:
        await content_handlers._process_past_exam_topic_selection(update, context, db_user, text)
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
        # Keep pending for notes so users can pick multiple subjects in the same menu
    elif db_user.pending_action == "select_quiz_grade" and (text.startswith("Grade ") or text.lower() == "mixed"):
        await content_handlers._process_quiz_grade_selection(update, context, db_user, text)
    elif db_user.pending_action == "quiz_post_options" and text in [MI.ANOTHER_QUIZ, MI.EXIT_QUIZZES]:
        if text == MI.ANOTHER_QUIZ:
            # Restart grade prompt with same subject
            subject = context.user_data.get("quiz_subject")
            if subject:
                await update.message.reply_text("Choose the grade for the quiz:", reply_markup=Keyboards.quiz_grades_menu())
                db_user.pending_action = "select_quiz_grade"
                db_user.save()
            else:
                await content_handlers.handle_quizzes_menu(update, context)
        else:
            # Exit quizzes back to main menu
            db_user.pending_action = None
            db_user.save()
            await update.message.reply_text("Exited Quizzes.", reply_markup=Keyboards.main_menu())
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