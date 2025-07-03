# payment_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from database.models import User
from config import Config


async def upgrade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = User.find(user.id)

    if db_user and db_user.is_premium:
        await update.message.reply_text("🎉 You're already a premium user!")
        return

    await update.message.reply_text(
        "💎 Upgrade to Premium to unlock:\n"
        "- All past exam papers with solutions\n"
        "- Exclusive study guides\n"
        "- Priority AI chat support\n\n"
        "To upgrade, please send a screenshot of your payment receipt."
    )


async def handle_payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]  # Get highest resolution photo

    # Save payment proof to user record
    db_user = User.find(user.id)
    if not db_user:
        db_user = User(user_id=user.id, username=user.username)

    db_user.payment_proof = photo.file_id
    db_user.payment_pending = True
    db_user.save()

    # Notify moderators
    for mod_id in Config.PAYMENT_MODERATORS:
        try:
            await context.bot.send_photo(
                chat_id=mod_id,
                photo=photo.file_id,
                caption=f"Payment verification request from @{user.username} ({user.id})"
            )
        except Exception as e:
            print(f"Failed to notify moderator {mod_id}: {e}")

    await update.message.reply_text(
        "✅ Thank you! Your payment proof has been submitted for verification. "
        "You'll be notified once approved (usually within 24 hours)."
    )