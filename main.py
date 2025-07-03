# main.py
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PicklePersistence
from handlers import user_handlers, admin_handlers, payment_handlers
from config import Config, MenuItems # Import MenuItems directly

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create a PicklePersistence object to store user data (e.g., chat history for AI)
    # This will store data in a file named 'bot_data.pickle'
    persistence = PicklePersistence(filepath="bot_data.pickle")

    # Create the Application and pass your bot's token and persistence.
    # Ensure Config.TELEGRAM_TOKEN is set in config.py
    application = Application.builder().token(Config.TELEGRAM_TOKEN).persistence(persistence).build()

    # Command handlers
    application.add_handler(CommandHandler("start", user_handlers.start))
    application.add_handler(CommandHandler("approve", admin_handlers.approve_payment))
    application.add_handler(CommandHandler("upgrade", payment_handlers.upgrade_command))

    # Message handlers
    # Handler for stream selection (Natural|Social)
    application.add_handler(MessageHandler(filters.Regex(r"^(Natural|Social)$"), user_handlers.handle_stream_selection))

    # Handler for the main "Resources" menu item
    # Use MenuItems directly here
    application.add_handler(MessageHandler(filters.Regex(MenuItems.RESOURCES), user_handlers.handle_resources))

    # Handler for resource type selection (Text Books, Teacher's Guide, Cheat Sheets)
    # UPDATED: Removed '📖' and '📝' from this regex.
    # '📖 Text Books' is still caught by '📖'.
    # '📝 Short Notes' and '📝 Past Exams' are now handled by the general MessageHandler.
    application.add_handler(MessageHandler(filters.Regex(r"^(📚|🧮)"), user_handlers.handle_resource_selection))

    # Handler for grade selection (e.g., "Grade 9 Textbooks")
    application.add_handler(
        MessageHandler(filters.Regex(r"^Grade (9|10|11|12) (Textbooks|Guide)$"), user_handlers.handle_grade_selection)
    )

    # Handler for specific cheat sheet selections
    application.add_handler(
        MessageHandler(filters.Regex(r"^(🧮 Math Formulas|📝 English Tips|⚛ Physics Formulas|"
                                      r"🧬 Biology Cheats|🧪 Chemistry Cheats|🧠 Aptitude Tricks|"
                                      r"🗺 Geography Cheats|📜 History Cheats|💹 Economics Cheats)$"),
                       user_handlers.handle_cheat_sheet_selection)
    )

    # Handler for payment screenshots
    application.add_handler(MessageHandler(filters.PHOTO, payment_handlers.handle_payment_screenshot))

    # This general text handler will now manage all other text messages that are not commands,
    # including main menu selections (like "📝 Past Exams", "📝 Short Notes", "📖 Study Tips"),
    # subject choices based on pending_action, and "back" buttons.
    # It also handles AI chat interaction when the pending_action is set to 'ai_chat'.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_handlers.handle_message))

    # Log that the bot is starting
    logger.info("Bot is running with updated features!")

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

