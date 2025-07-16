# handlers/invite_handlers.py
import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.models import User
from keyboards import Keyboards
from config import Config, MenuItems as MI
from handlers import user_handlers

logger = logging.getLogger(__name__)


# Helper function to escape special MarkdownV2 characters
def escape_markdown_v2_text(text: str) -> str:
    """Escapes MarkdownV2 special characters in a given string."""
    escape_chars = r'_*[]()~`>#+-.=|{}!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)


async def handle_invite_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'Invite and Earn' button press from the main menu.
    Displays the invite options menu.
    """
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user:
        await user_handlers.start(update, context)
        return

    message = (
        "🤝 *Invite & Earn*\n\n"
        f"{escape_markdown_v2_text('Here you can get your referral link to share with friends or withdraw your earnings.')}\n\n"
        f"📈 *Your Stats:*\n"
        f"∙ *Successful Referrals:* {db_user.referral_count}\n"
        f"∙ *Current Balance:* {escape_markdown_v2_text(f'{db_user.referral_balance:.2f} ETB')}\n\n"
        f"{escape_markdown_v2_text('Please choose an option below:')}"
    )

    await update.message.reply_text(
        message,
        parse_mode='MarkdownV2',
        reply_markup=Keyboards.invite_menu()
    )
    logger.info(f"User {user.id} accessed the Invite & Earn menu.")


async def handle_share_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'Share Invite' button.
    Generates and displays the user's referral link.
    """
    user = update.effective_user
    bot_username = (await context.bot.get_me()).username
    db_user = User.find(user.id)

    if not db_user:
        await user_handlers.start(update, context)
        return

    referral_code = user.id
    referral_link = f"https://t.me/{bot_username}?start={referral_code}"
    share_url = f"https://t.me/{bot_username}?start={referral_code}"

    share_text = (
        "Hey! I'm using this awesome Telegram bot to prepare for the Ethiopian University Entrance Examination (UEE). "
        "It has resources, quizzes, and even an AI tutor! You should check it out. "
        "Join using my link to get started!"
    )

    message = (
        "🔗 *Your Referral Link:*\n\n"
        f"{escape_markdown_v2_text('Share this link with your friends. When they join and upgrade to premium, you earn 50 ETB!')}\n\n"
        f"`{referral_link}`\n\n"
        f"{escape_markdown_v2_text('Click the button below to easily share it on Telegram.')}"
    )

    await update.message.reply_text(
        message,
        parse_mode='MarkdownV2',
        reply_markup=Keyboards.share_menu(share_url, share_text)
    )
    logger.info(f"User {user.id} requested their referral link to share.")


async def handle_withdraw_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the 'Request Withdrawal' button press."""
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user:
        await user_handlers.start(update, context)
        return

    min_amount = Config.MIN_WITHDRAWAL_AMOUNT

    if db_user.withdrawal_request_pending:
        await update.message.reply_text(
            "⏳ You already have a pending withdrawal request under review by an admin. Please be patient.",
            reply_markup=Keyboards.invite_menu()
        )
        return

    if db_user.referral_balance < min_amount:
        await update.message.reply_text(
            f"⚠️ You need at least {min_amount:.2f} ETB in your balance to make a withdrawal request. "
            f"Your current balance is {db_user.referral_balance:.2f} ETB.",
            reply_markup=Keyboards.invite_menu()
        )
        return

    db_user.pending_action = "awaiting_bank_for_withdrawal"
    db_user.save()

    await update.message.reply_text(
        "Please select the bank where you want to receive your funds:",
        reply_markup=Keyboards.withdrawal_banks_menu()
    )
    logger.info(f"User {user.id} initiated a withdrawal request.")


async def handle_bank_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the selected bank and asks for the account number."""
    user = update.effective_user
    db_user = User.find(user.id)
    bank_name = update.message.text

    if not db_user or db_user.pending_action != "awaiting_bank_for_withdrawal":
        # Safeguard if user is not in the correct state
        await user_handlers.start(update, context)
        return

    # Store the selected bank in the context for the next step
    context.user_data['withdrawal_bank'] = bank_name
    db_user.pending_action = "awaiting_account_number_for_withdrawal"
    db_user.save()

    await update.message.reply_text(
        f"You selected *{escape_markdown_v2_text(bank_name)}*.\n\nPlease enter your *full account number*.",
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info(f"User {user.id} selected bank: {bank_name}")


async def handle_account_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the account number and sends the request to admins."""
    user = update.effective_user
    db_user = User.find(user.id)
    account_number = update.message.text

    if not db_user or db_user.pending_action != "awaiting_account_number_for_withdrawal":
        await user_handlers.start(update, context)
        return

    bank_name = context.user_data.get('withdrawal_bank')
    if not bank_name:
        # Safeguard if bank name was lost
        await update.message.reply_text("Something went wrong. Please start the withdrawal process again.",
                                        reply_markup=Keyboards.invite_menu())
        db_user.pending_action = None
        db_user.save()
        return

    # All checks passed, process the request
    db_user.pending_action = None
    db_user.withdrawal_request_pending = True
    db_user.save()

    withdrawal_amount = db_user.referral_balance

    await update.message.reply_text(
        "✅ Thank you! Your withdrawal request has been submitted for admin review. "
        "We will notify you once it's processed. This can take up to 48 hours.",
        reply_markup=Keyboards.main_menu()
    )

    # Notify admins
    for admin_id in Config.PAYMENT_MODERATORS:
        try:
            admin_message = (
                f"🚨 *New Withdrawal Request* 🚨\n\n"
                f"*From User:* {escape_markdown_v2_text(user.first_name)} (@{user.username or 'N/A'})\n"
                f"*User ID:* `{user.id}`\n"
                f"*Amount to Withdraw:* {escape_markdown_v2_text(f'{withdrawal_amount:.2f} ETB')}\n\n"
                f"*Bank:* {escape_markdown_v2_text(bank_name)}\n"
                f"*Account Number:* `{escape_markdown_v2_text(account_number)}`\n\n"
                f"Please verify and process the payment."
            )
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                reply_markup=Keyboards.admin_withdrawal_approval_keyboard(user.id, withdrawal_amount),
                parse_mode='MarkdownV2'
            )
        except Exception as e:
            logger.error(f"Failed to send withdrawal notification to admin {admin_id}: {e}")

    logger.info(f"User {user.id} submitted withdrawal request for {withdrawal_amount} ETB to {bank_name}.")
    # Clean up context
    del context.user_data['withdrawal_bank']


async def approve_withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin's 'Approve' button for a withdrawal."""
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    requester_user_id = int(data[2])
    amount_to_deduct = float(data[3])

    db_user = User.find(requester_user_id)

    if not db_user or not db_user.withdrawal_request_pending:
        await query.edit_message_text(
            text=query.message.text_markdown_v2 + f"\n\n*⚠️ Request for user ID {requester_user_id} not found or already processed.*",
            parse_mode='MarkdownV2'
        )
        return

    # Process the withdrawal
    db_user.referral_balance -= amount_to_deduct
    db_user.withdrawal_request_pending = False
    db_user.save()

    # Notify user
    try:
        await context.bot.send_message(
            chat_id=requester_user_id,
            text=f"✅ Your withdrawal request for *{amount_to_deduct:.2f} ETB* has been approved and processed! The funds should appear in your account shortly.",
            parse_mode='MarkdownV2'
        )
    except Exception as e:
        logger.error(f"Failed to send withdrawal approval notification to user {requester_user_id}: {e}")

    # Update admin message
    await query.edit_message_text(
        text=query.message.text_markdown_v2 + f"\n\n*✅ Approved by {query.from_user.first_name}.*\n*Amount: {amount_to_deduct:.2f} ETB*",
        parse_mode='MarkdownV2'
    )
    logger.info(f"Withdrawal for user {requester_user_id} approved by admin {query.from_user.id}.")


async def decline_withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin's 'Decline' button for a withdrawal."""
    query = update.callback_query
    await query.answer()

    requester_user_id = int(query.data.split('_')[2])
    db_user = User.find(requester_user_id)

    if not db_user or not db_user.withdrawal_request_pending:
        await query.edit_message_text(
            text=query.message.text_markdown_v2 + f"\n\n*⚠️ Request for user ID {requester_user_id} not found or already processed.*",
            parse_mode='MarkdownV2'
        )
        return

    # Reset the flag, but do not deduct balance
    db_user.withdrawal_request_pending = False
    db_user.save()

    # Notify user
    try:
        await context.bot.send_message(
            chat_id=requester_user_id,
            text="😔 Your withdrawal request could not be approved at this time. This might be due to an issue with the provided account details. Please double-check them and try again later. If you believe this is an error, contact support.",
        )
    except Exception as e:
        logger.error(f"Failed to send withdrawal decline notification to user {requester_user_id}: {e}")

    # Update admin message
    await query.edit_message_text(
        text=query.message.text_markdown_v2 + f"\n\n*❌ Declined by {query.from_user.first_name}.*",
        parse_mode='MarkdownV2'
    )
    logger.info(f"Withdrawal for user {requester_user_id} declined by admin {query.from_user.id}.")