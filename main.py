# main.py
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PicklePersistence, CallbackQueryHandler
from handlers import user_handlers, payment_handlers, resource_handlers, content_handlers, invite_handlers
from config import Config, MenuItems
from telegram import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    persistence = PicklePersistence(filepath="bot_data.pickle")

    application = Application.builder().token(Config.TELEGRAM_TOKEN).persistence(persistence).build()

    # Command handlers
    application.add_handler(CommandHandler("start", user_handlers.start))

    # Message handlers for specific text/regex
    application.add_handler(MessageHandler(filters.Regex(r"^(Natural|Social)$"), user_handlers.handle_stream_selection))

    application.add_handler(
        MessageHandler(filters.Regex(r"^(📚 Teacher's Guide|🧮 Cheat Sheets)$"),
                       resource_handlers.handle_resource_selection))

    application.add_handler(
        MessageHandler(filters.Regex(r"^Grade (9|10|11|12) (Textbooks|Guide)$"),
                       resource_handlers.handle_grade_selection)
    )

    application.add_handler(
        MessageHandler(filters.Regex(r"^(🧮 Math Formulas|📝 English Tips|⚛ Physics Formulas|"
                                     r"🧬 Biology Cheats|🧪 Chemistry Cheats|🧠 Aptitude Tricks|"
                                     r"🗺 Geography Cheats|📜 History Cheats|💹 Economics Cheats)$"),
                       resource_handlers.handle_cheat_sheet_selection)
    )

    # Handler for photos (payment proof)
    application.add_handler(MessageHandler(filters.PHOTO, payment_handlers.process_payment_proof))

    # Callback query handlers for admin buttons
    application.add_handler(CallbackQueryHandler(payment_handlers.approve_payment_callback, pattern=r"^approve_\d+$"))
    application.add_handler(CallbackQueryHandler(payment_handlers.decline_payment_callback, pattern=r"^decline_\d+$"))

    # --- NEW: Callback handlers for withdrawal approval ---
    application.add_handler(CallbackQueryHandler(invite_handlers.approve_withdrawal_callback,
                                                 pattern=r"^approve_withdrawal_\d+_\d+\.?\d*$"))
    application.add_handler(
        CallbackQueryHandler(invite_handlers.decline_withdrawal_callback, pattern=r"^decline_withdrawal_\d+$"))
    # --- END NEW ---

    # General text handler - MUST BE LAST among message handlers
    # This handler uses the logic in user_handlers.handle_message to route menu buttons and pending actions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_handlers.handle_message))

    logger.info("Bot is running with updated features!")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()