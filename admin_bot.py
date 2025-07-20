# admin_bot.py
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import Forbidden, BadRequest

from database.models import User
from config import Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def escape_markdown_v2_text(text: str) -> str:
    """Escapes MarkdownV2 special characters in a given string."""
    if not text:
        return 'N/A'
    escape_chars = r'_*[]()~`>#+-.=|{}!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in str(text))


async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is an authorized admin."""
    user_id = update.effective_user.id
    if user_id not in Config.ADMIN_IDS:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Access denied. You are not an authorized administrator.')}",
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardRemove()
        )
        logger.warning(f"Unauthorized access attempt by user {user_id}.")
        return False
    return True


# --- Main menu keyboard definition ---
ADMIN_MAIN_MENU = ReplyKeyboardMarkup([
    ["List Users", "View User"],
    ["Delete User", "Block User"],
    ["Stats", "Broadcast"],
    ["Wipe All Users"]
], resize_keyboard=True, one_time_keyboard=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command and displays the main menu with reply keyboard."""
    if not await check_admin(update, context):
        return

    context.user_data.clear()  # Clear any pending state
    message = (
        "👋 Welcome to AceBot Admin Panel 👋\n\n"
        "This bot allows authorized administrators to manage user data for the AceBot platform.\n\n"
        "Use the buttons below or commands to select an action:"
    )

    await update.message.reply_text(
        text=message,
        parse_mode=None,
        reply_markup=ADMIN_MAIN_MENU
    )
    logger.info(f"Admin {update.effective_user.id} started the admin bot.")


# --- /stats command handler ---
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays database statistics."""
    if not await check_admin(update, context):
        return

    users = User.all()
    total_users = len(users)
    premium_users = sum(1 for u in users if u.is_premium)
    pending_payment = sum(1 for u in users if u.payment_pending)
    pending_withdrawal = sum(1 for u in users if u.withdrawal_request_pending)

    stats_message = (
        f"📊 *Bot Statistics* 📊\n\n"
        f"*Total Users:* `{total_users}`\n"
        f"*Premium Users:* `{premium_users}`\n"
        f"*Pending Payment Approvals:* `{pending_payment}`\n"
        f"*Pending Withdrawal Requests:* `{pending_withdrawal}`"
    )

    await update.message.reply_text(
        text=stats_message,
        parse_mode='MarkdownV2',
        reply_markup=ADMIN_MAIN_MENU
    )
    logger.info(f"Admin {update.effective_user.id} requested stats.")


# --- /broadcast command handler ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates the broadcast process."""
    if not await check_admin(update, context):
        return

    context.user_data['pending_command'] = 'broadcast_message'
    await update.message.reply_text(
        "Please send the message you want to broadcast to all users. "
        "This message will be sent as is. To cancel, type /cancel.",
        reply_markup=ReplyKeyboardRemove()
    )


async def cancel_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels any pending action."""
    if not await check_admin(update, context):
        return
    context.user_data.clear()
    await update.message.reply_text(
        "Action cancelled. Returning to main menu.",
        reply_markup=ADMIN_MAIN_MENU
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles text messages for menu selections, user_id inputs, or other pending commands."""
    if not await check_admin(update, context):
        return

    text = update.message.text.strip()
    back_menu = ReplyKeyboardMarkup([["Back"]], resize_keyboard=True)

    # --- Handle pending broadcast message ---
    if context.user_data.get('pending_command') == 'broadcast_message':
        context.user_data.clear()
        await update.message.reply_text(f"Broadcasting message to all users. This may take a while...",
                                        reply_markup=ADMIN_MAIN_MENU)

        users = User.all()
        sent_count = 0
        failed_count = 0

        for user in users:
            try:
                await context.bot.send_message(chat_id=user.user_id, text=text)
                sent_count += 1
            except (Forbidden, BadRequest):
                # User has blocked the bot or chat not found
                failed_count += 1
            await asyncio.sleep(0.1)  # Avoid hitting rate limits

        await update.message.reply_text(
            f"📢 Broadcast complete!\n\n"
            f"✅ Sent to: {sent_count} users\n"
            f"❌ Failed for: {failed_count} users (likely blocked the bot)",
            reply_markup=ADMIN_MAIN_MENU
        )
        logger.info(f"Admin {update.effective_user.id} finished broadcast. Sent: {sent_count}, Failed: {failed_count}")
        return

    # Handle main menu selections
    if 'pending_command' not in context.user_data:
        if text == "List Users":
            users = User.all()
            if not users:
                await update.message.reply_text(
                    f"{escape_markdown_v2_text('No users found in the database.')}",
                    parse_mode='MarkdownV2',
                    reply_markup=ADMIN_MAIN_MENU
                )
                return

            message = f"📋 *User List* 📋\n\n"
            for user in users:
                message += (
                    f"*User ID:* `{user.user_id}`\n"
                    f"*Name:* {escape_markdown_v2_text(user.full_name or user.username or 'N/A')}\n"
                    f"*Referral Balance:* {escape_markdown_v2_text(f'{user.referral_balance:.2f} ETB')}\n"
                    f"*Blocked:* {escape_markdown_v2_text(str(user.blocked))}\n\n"
                )
            await update.message.reply_text(
                text=message,
                parse_mode='MarkdownV2',
                reply_markup=ADMIN_MAIN_MENU
            )
            logger.info(f"Admin {update.effective_user.id} listed all users.")

        elif text == "Stats":
            await stats(update, context)
            return

        elif text == "Broadcast":
            await broadcast(update, context)
            return

        elif text == "View User":
            context.user_data['pending_command'] = 'view_user'
            await update.message.reply_text(
                "Please provide the user_id to view details.",
                parse_mode=None,
                reply_markup=back_menu
            )

        elif text == "Delete User":
            context.user_data['pending_command'] = 'delete_user'
            await update.message.reply_text(
                "Please provide the user_id to delete.",
                parse_mode=None,
                reply_markup=back_menu
            )

        elif text == "Block User":
            context.user_data['pending_command'] = 'block_user'
            await update.message.reply_text(
                "Please provide the user_id to block or unblock (optionally add 'true' or 'false', e.g., '123456789 true').",
                parse_mode=None,
                reply_markup=back_menu
            )

        elif text == "Wipe All Users":
            context.user_data['pending_command'] = 'wipe_all_users'
            await update.message.reply_text(
                "⚠️ Are you sure you want to wipe ALL users? This action cannot be undone.\n"
                "Type 'confirm' to proceed or anything else to cancel.",
                parse_mode=None,
                reply_markup=back_menu
            )

        else:
            await update.message.reply_text(
                "Please use the buttons to select an action.",
                parse_mode=None,
                reply_markup=ADMIN_MAIN_MENU
            )
        return

    # Handle Back button
    if text == "Back":
        context.user_data.clear()
        await update.message.reply_text(
            "Returned to main menu.",
            parse_mode=None,
            reply_markup=ADMIN_MAIN_MENU
        )
        return

    # Handle pending commands
    if context.user_data['pending_command'] == 'wipe_all_users':
        if text.lower() == 'confirm':
            count = User.delete_all()
            await update.message.reply_text(
                f"{escape_markdown_v2_text(f'Successfully wiped {count} users from the database.')}",
                parse_mode='MarkdownV2',
                reply_markup=ADMIN_MAIN_MENU
            )
            logger.info(f"Admin {update.effective_user.id} wiped all users ({count} deleted).")
        else:
            await update.message.reply_text(
                "Wipe all users cancelled.",
                parse_mode=None,
                reply_markup=ADMIN_MAIN_MENU
            )
        context.user_data.clear()
        return

    # Handle user_id inputs
    args = text.split()
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Please provide a valid user_id (numeric).')}",
            parse_mode='MarkdownV2',
            reply_markup=back_menu
        )
        return

    user_id = int(args[0])
    context.user_data['pending_user_id'] = user_id
    db_user = User.find(user_id)
    if not db_user:
        await update.message.reply_text(
            f"{escape_markdown_v2_text(f'User with ID {user_id} not found.')}",
            parse_mode='MarkdownV2',
            reply_markup=ADMIN_MAIN_MENU
        )
        context.user_data.clear()
        return

    if context.user_data['pending_command'] == 'view_user':
        message = (
            f"👤 *User Details* 👤\n\n"
            f"*User ID:* `{user_id}`\n"
            f"*Username:* {escape_markdown_v2_text(db_user.username or 'N/A')}\n"
            f"*Full Name:* {escape_markdown_v2_text(db_user.full_name or 'N/A')}\n"
            f"*Stream:* {escape_markdown_v2_text(db_user.stream or 'N/A')}\n"
            f"*Premium:* {escape_markdown_v2_text(str(db_user.is_premium))}\n"
            f"*Payment Pending:* {escape_markdown_v2_text(str(db_user.payment_pending))}\n"
            f"*Payment Proof:* {escape_markdown_v2_text(db_user.payment_proof or 'N/A')}\n"
            f"*Referral Balance:* {escape_markdown_v2_text(f'{db_user.referral_balance:.2f} ETB')}\n"
            f"*Referral Count:* {db_user.referral_count}\n"
            f"*Referred By:* {escape_markdown_v2_text(str(db_user.referred_by) or 'N/A')}\n"
            f"*Referral Credited:* {escape_markdown_v2_text(str(db_user.referral_credited))}\n"
            f"*Blocked:* {escape_markdown_v2_text(str(db_user.blocked))}\n"
            f"*Withdrawal Pending:* {escape_markdown_v2_text(str(db_user.withdrawal_request_pending))}\n"
            f"*Pending Action:* {escape_markdown_v2_text(db_user.pending_action or 'None')}\n"
            f"*Pending Admin Approval:* {escape_markdown_v2_text(str(db_user.pending_admin_approval))}\n"
            f"*Created At:* {escape_markdown_v2_text(str(db_user.created_at))}\n"
            f"*Last Active:* {escape_markdown_v2_text(str(db_user.last_active))}"
        )
        await update.message.reply_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=ADMIN_MAIN_MENU
        )
        logger.info(f"Admin {update.effective_user.id} viewed details for user {user_id}.")

    elif context.user_data['pending_command'] == 'delete_user':
        db_user.delete()
        await update.message.reply_text(
            f"{escape_markdown_v2_text(f'User with ID {user_id} has been deleted.')}",
            parse_mode='MarkdownV2',
            reply_markup=ADMIN_MAIN_MENU
        )
        logger.info(f"Admin {update.effective_user.id} deleted user {user_id}.")

    elif context.user_data['pending_command'] == 'block_user':
        block_status = args[1].lower() == 'true' if len(args) > 1 else True
        db_user.blocked = block_status
        db_user.save()
        status = 'blocked' if block_status else 'unblocked'
        await update.message.reply_text(
            f"{escape_markdown_v2_text(f'User with ID {user_id} has been {status}.')}",
            parse_mode='MarkdownV2',
            reply_markup=ADMIN_MAIN_MENU
        )
        logger.info(f"Admin {update.effective_user.id} {status} user {user_id}.")

    context.user_data.clear()


def main():
    """Run the admin bot."""
    application = Application.builder().token(Config.ADMIN_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("cancel", cancel_action))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Admin bot is running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()