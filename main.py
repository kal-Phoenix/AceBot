# main.py
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PicklePersistence, CallbackQueryHandler
from handlers import user_handlers, payment_handlers
from config import Config, MenuItems # Import MenuItems directly
from telegram import Update # Import Update for allowed_updates

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
    # Keeping persistence as it's useful for pending_action and other user data.
    persistence = PicklePersistence(filepath="bot_data.pickle")

    # Create the Application and pass your bot's token and persistence.
    # Ensure Config.TELEGRAM_TOKEN is set in config.py
    application = Application.builder().token(Config.TELEGRAM_TOKEN).persistence(persistence).build()

    # Command handlers
    application.add_handler(CommandHandler("start", user_handlers.start))
    # Removed CommandHandler for /approve as it's now handled by inline callbacks
    # application.add_handler(CommandHandler("upgrade", payment_handlers.upgrade_command)) # Handled by MessageHandler now

    # Message handlers
    # Handler for stream selection (Natural|Social)
    application.add_handler(MessageHandler(filters.Regex(r"^(Natural|Social)$"), user_handlers.handle_stream_selection))

    # Handler for the main "Resources" menu item
    application.add_handler(MessageHandler(filters.Regex(MenuItems.RESOURCES), user_handlers.handle_resources))

    # Handler for resource types that lead directly to grade/subject selection within handle_resource_selection
    application.add_handler(MessageHandler(filters.Regex(r"^(📚|🧮)"), user_handlers.handle_resource_selection))

    # Handler for grade selection (e.g., "Grade 9 Textbooks", "Grade 10 Guide")
    application.add_handler(
        MessageHandler(filters.Regex(r"^Grade (9|10|11|12) (Textbooks|Guide)$"), user_handlers.handle_grade_selection)
    )

    # Handler for specific cheat sheet selections (these are the subject buttons after "Cheat Sheets")
    application.add_handler(
        MessageHandler(filters.Regex(r"^(🧮 Math Formulas|📝 English Tips|⚛ Physics Formulas|"
                                      r"🧬 Biology Cheats|🧪 Chemistry Cheats|🧠 Aptitude Tricks|"
                                      r"🗺 Geography Cheats|📜 History Cheats|💹 Economics Cheats)$"),
                       user_handlers.handle_cheat_sheet_selection)
    )

    # NEW: Handler for the "Upgrade" menu button
    application.add_handler(MessageHandler(filters.Regex(MenuItems.UPGRADE), payment_handlers.upgrade_command))

    # NEW: Handler for payment status choice ("Yes, I have paid" / "No, I haven't paid yet")
    application.add_handler(MessageHandler(filters.Regex(r"^(✅ Yes, I have paid|❌ No, I haven't paid yet)$"), payment_handlers.handle_payment_status_choice))

    # NEW: Handler for payment screenshots
    application.add_handler(MessageHandler(filters.PHOTO, payment_handlers.process_payment_proof))

    # Callback query handlers for admin approval/decline buttons
    application.add_handler(CallbackQueryHandler(payment_handlers.approve_payment_callback, pattern=r"^approve_\d+$"))
    application.add_handler(CallbackQueryHandler(payment_handlers.decline_payment_callback, pattern=r"^decline_\d+$"))


    # This general text handler will now manage all other text messages that are not commands,
    # including:
    # - Main menu selections (e.g., "📝 Past Exams", "📝 Short Notes", "📖 Study Tips", "💡 Exam Tips", "📖 Text Books")
    # - Subject choices based on pending_action (for Short Notes, Quizzes, etc.)
    # - "Back" buttons
    # - AI chat interaction when the pending_action is set to 'ai_chat'.
    # - User's full name input for payment
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_handlers.handle_message))

    # Log that the bot is starting
    logger.info("Bot is running with updated features!")

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()