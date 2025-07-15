# handlers/invite_handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import User
import re # Ensure 're' is imported for potential future regex use, though not directly used in this helper.

logger = logging.getLogger(__name__)

# Helper function to escape special MarkdownV2 characters for plain text parts
def escape_markdown_v2_text(text: str) -> str:
    """Escapes MarkdownV2 special characters in a given string."""
    # List of characters to escape: _ * [ ] ( ) ~ ` > # + - = | { } . ! \
    # The order of replacement matters, especially for '\'!
    text = text.replace('\\', '\\\\') # Escape backslashes first
    text = text.replace('_', '\\_')
    text = text.replace('*', '\\*')
    text = text.replace('[', '\\[')
    text = text.replace(']', '\\]')
    text = text.replace('(', '\\(')
    text = text.replace(')', '\\)')
    text = text.replace('~', '\\~')
    text = text.replace('`', '\\`')
    text = text.replace('>', '\\>')
    text = text.replace('#', '\\#')
    text = text.replace('+', '\\+')
    text = text.replace('-', '\\-')
    text = text.replace('=', '\\=')
    text = text.replace('|', '\\|')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('.', '\\.') # This is crucial for numerical values
    text = text.replace('!', '\\!')
    return text

async def handle_invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'Invite and Earn' button.
    Generates a user's referral link and shows their earnings.
    """
    user = update.effective_user
    bot_username = (await context.bot.get_me()).username
    db_user = User.find(user.id)

    if not db_user:
        # This case should be rare, but as a safeguard
        from handlers import user_handlers
        await user_handlers.start(update, context)
        return

    # The user's ID is their unique referral code
    referral_code = user.id
    referral_link = f"https://t.me/{bot_username}?start={referral_code}"

    # Construct the message with proper MarkdownV2 escaping
    message = (
        "🤝 *Invite & Earn*\n\n"
        # Escape plain text parts
        f"{escape_markdown_v2_text('Share your unique referral link with your friends.')} "
        f"{escape_markdown_v2_text('When a new user joins through your link and upgrades to a premium membership, you will earn ')}*50 ETB*\\!\n\n"
        f"🔗 *Your Referral Link:*\n"
        f"`{referral_link}`\n\n" # Referral link in code block, content is fine
        f"📈 *Your Stats:*\n"
        f"∙ *Successful Referrals:* {db_user.referral_count}\n"
        # Escape the formatted balance and 'ETB'
        f"∙ *Current Balance:* {escape_markdown_v2_text(f'{db_user.referral_balance:.2f}')} {escape_markdown_v2_text('ETB')}\n\n"
        f"{escape_markdown_v2_text('Keep sharing to earn more!')}"
    )

    await update.message.reply_text(message, parse_mode='MarkdownV2')
    logger.info(f"User {user.id} accessed their invite link and stats.")