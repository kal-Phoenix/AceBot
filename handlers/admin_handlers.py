# admin_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from database.crud import approve_premium
from config import Config

async def approve_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in Config.PAYMENT_MODERATORS:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        user_id = int(context.args[0])
        if approve_premium(user_id):
            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 Your premium subscription has been approved! "
                     "You now have access to all premium features."
            )
            await update.message.reply_text(f"Successfully approved premium for user {user_id}")
        else:
            await update.message.reply_text("User not found or already premium")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /approve <user_id>")