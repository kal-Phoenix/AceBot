# handlers/invite_handlers.py
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.models import User
from keyboards import Keyboards
from config import Config, MenuItems as MI
from handlers import user_handlers

logger = logging.getLogger(__name__)

def escape_markdown_v2_text(text: str) -> str:
    """Escapes MarkdownV2 special characters in a given string."""
    if not text:
        return 'N/A'
    escape_chars = r'_*[]()~`>#+-.=|{}!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in str(text))

async def handle_invite_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'Invite and Earn' button press from the main menu.
    Displays the invite options menu with inline buttons.
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

    # Use inline keyboard for Share and Withdraw buttons
    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("↗️ Share Invite", callback_data="share_invite"),
            InlineKeyboardButton("💰 Request Withdrawal", callback_data="request_withdrawal")
        ],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main_menu")]
    ])

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=inline_keyboard
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode='MarkdownV2',
            reply_markup=inline_keyboard
        )
    logger.info(f"User {user.id} accessed the Invite & Earn menu.")

async def handle_inline_invite_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles inline button presses for the Invite and Earn menu."""
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    data = query.data

    if data == "share_invite":
        await handle_share_request(update, context)
    elif data == "request_withdrawal":
        await handle_withdraw_request(update, context)
    elif data == "back_to_main_menu":
        await user_handlers.start(update, context)

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

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.share_menu(share_url, share_text)
        )
    else:
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
        message = (
            "⏳ *Pending Withdrawal Request*\n\n"
            f"{escape_markdown_v2_text('You already have a pending withdrawal request under review by an admin. Please be patient.')}"
        )
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                parse_mode='MarkdownV2',
                reply_markup=Keyboards.invite_inline_menu()
            )
        else:
            await update.message.reply_text(
                message,
                parse_mode='MarkdownV2',
                reply_markup=Keyboards.invite_inline_menu()
            )
        return

    if db_user.referral_balance < min_amount:
        message = (
            "⚠️ *Insufficient Balance*\n\n"
            f"{escape_markdown_v2_text(f'You need at least {min_amount:.2f} ETB to make a withdrawal request. ')}"
            f"{escape_markdown_v2_text(f'Your current balance is {db_user.referral_balance:.2f} ETB.')}"
        )
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                parse_mode='MarkdownV2',
                reply_markup=Keyboards.invite_inline_menu()
            )
        else:
            await update.message.reply_text(
                message,
                parse_mode='MarkdownV2',
                reply_markup=Keyboards.invite_inline_menu()
            )
        return

    db_user.pending_action = "awaiting_bank_for_withdrawal"
    db_user.save()

    message = (
        "🏦 *Select Bank*\n\n"
        f"{escape_markdown_v2_text('Please select the bank where you want to receive your funds:')}"
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.withdrawal_banks_inline_menu()
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.withdrawal_banks_inline_menu()
        )
    logger.info(f"User {user.id} initiated a withdrawal request.")

async def handle_bank_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the selected bank (via callback or plain text) and asks for the account number."""
    user = update.effective_user
    db_user = User.find(user.id)
    query = getattr(update, 'callback_query', None)
    if query:
        await query.answer()
        bank_name = query.data.replace("bank_", "")
    else:
        bank_name = update.message.text

    if not db_user or db_user.pending_action != "awaiting_bank_for_withdrawal":
        await user_handlers.start(update, context)
        return

    context.user_data['withdrawal_bank'] = bank_name
    db_user.pending_action = "awaiting_account_number_for_withdrawal"
    db_user.save()

    message = (
        f"🏦 *Selected Bank: {escape_markdown_v2_text(bank_name)}*\n\n"
        f"{escape_markdown_v2_text('Please enter your full account number:')}"
    )
    if query:
        await query.edit_message_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=None
        )
    else:
        await update.message.reply_text(
            text=message,
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardRemove()
        )
    logger.info(f"User {user.id} selected bank: {bank_name}")

async def handle_account_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the account number and asks for the account holder's name."""
    user = update.effective_user
    db_user = User.find(user.id)
    account_number = update.message.text.strip()

    if not db_user or db_user.pending_action != "awaiting_account_number_for_withdrawal":
        await user_handlers.start(update, context)
        return

    # Validate account number
    if not account_number or len(account_number) < 5 or len(account_number) > 30:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Please enter a valid account number (5-30 characters).')}",
            parse_mode='MarkdownV2'
        )
        return

    # Remove any non-alphanumeric characters for security
    account_number = ''.join(char for char in account_number if char.isalnum())
    
    if not account_number:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Please enter a valid account number with alphanumeric characters only.')}",
            parse_mode='MarkdownV2'
        )
        return

    bank_name = context.user_data.get('withdrawal_bank')
    if not bank_name:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Something went wrong. Please start the withdrawal process again.')}",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.invite_inline_menu()
        )
        db_user.pending_action = None
        db_user.save()
        return

    context.user_data['withdrawal_account_number'] = account_number
    db_user.pending_action = "awaiting_account_holder_for_withdrawal"
    db_user.save()

    message = (
        f"🏦 *Selected Bank: {escape_markdown_v2_text(bank_name)}*\n"
        f"💳 *Account Number: {escape_markdown_v2_text(account_number)}*\n\n"
        f"{escape_markdown_v2_text('Please enter the full name of the account holder:')}"
    )
    await update.message.reply_text(
        text=message,
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info(f"User {user.id} provided account number for {bank_name}, awaiting account holder's name.")

async def handle_account_holder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the account holder's name and sends the withdrawal request to admins."""
    user = update.effective_user
    db_user = User.find(user.id)
    account_holder = update.message.text.strip()

    if not db_user or db_user.pending_action != "awaiting_account_holder_for_withdrawal":
        await user_handlers.start(update, context)
        return

    # Validate account holder name
    if not account_holder or len(account_holder) < 2 or len(account_holder) > 100:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Please enter a valid account holder name (2-100 characters).')}",
            parse_mode='MarkdownV2'
        )
        return

    # Remove excessive whitespace and validate characters
    account_holder = ' '.join(account_holder.split())
    if not all(char.isalpha() or char.isspace() for char in account_holder):
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Please enter a valid name using only letters and spaces.')}",
            parse_mode='MarkdownV2'
        )
        return

    bank_name = context.user_data.get('withdrawal_bank')
    account_number = context.user_data.get('withdrawal_account_number')
    if not bank_name or not account_number:
        await update.message.reply_text(
            f"{escape_markdown_v2_text('Something went wrong. Please start the withdrawal process again.')}",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.invite_inline_menu()
        )
        db_user.pending_action = None
        db_user.save()
        return

    db_user.pending_action = None
    db_user.withdrawal_request_pending = True
    db_user.withdrawal_bank = bank_name
    db_user.withdrawal_account_number = account_number
    db_user.withdrawal_account_holder = account_holder
    db_user.save()

    withdrawal_amount = db_user.referral_balance

    await update.message.reply_text(
        "✅ *Withdrawal Request Submitted*\n\n"
        f"{escape_markdown_v2_text('Thank you! Your withdrawal request has been submitted for admin review. ')}"
        f"{escape_markdown_v2_text('We will notify you once it is processed. This can take up to 48 hours.')}",
        parse_mode='MarkdownV2',
        reply_markup=Keyboards.main_menu()
    )

    # Notify all admins
    username = user.username or 'N/A'
    admin_message = (
        f"🚨 *New Withdrawal Request* 🚨\n\n"
        f"*From User:* {escape_markdown_v2_text(user.first_name)} \\({escape_markdown_v2_text(f'@{username}')}\\)\n"
        f"*User ID:* `{user.id}`\n"
        f"*Amount to Withdraw:* {escape_markdown_v2_text(f'{withdrawal_amount:.2f} ETB')}\n"
        f"*Bank:* {escape_markdown_v2_text(bank_name)}\n"
        f"*Account Number:* `{escape_markdown_v2_text(account_number)}`\n"
        f"*Account Holder:* {escape_markdown_v2_text(account_holder)}\n\n"
        f"{escape_markdown_v2_text('Please verify and process the payment.')}"
    )

    successful_notifications = 0
    for admin_id in Config.PAYMENT_MODERATORS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                reply_markup=Keyboards.admin_withdrawal_approval_keyboard(user.id, withdrawal_amount),
                parse_mode='MarkdownV2'
            )
            successful_notifications += 1
            logger.info(f"Withdrawal notification sent to admin {admin_id} for user {user.id}.")
        except Exception as e:
            logger.error(f"Failed to send withdrawal notification to admin {admin_id}: {e}")

    if successful_notifications == 0:
        await update.message.reply_text(
            "⚠️ *Error*\n\n"
            f"{escape_markdown_v2_text('Failed to notify admins. Please try again or contact support.')}",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        db_user.withdrawal_request_pending = False
        db_user.withdrawal_bank = None
        db_user.withdrawal_account_number = None
        db_user.withdrawal_account_holder = None
        db_user.save()
        logger.error(f"No admins were notified for withdrawal request from user {user.id}.")
        return

    logger.info(f"User {user.id} submitted withdrawal request for {withdrawal_amount} ETB to {bank_name}.")
    if 'withdrawal_bank' in context.user_data:
        del context.user_data['withdrawal_bank']
    if 'withdrawal_account_number' in context.user_data:
        del context.user_data['withdrawal_account_number']

async def approve_withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin's 'Sent' button for a withdrawal, prompting for a screenshot."""
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

    context.user_data['withdrawal_user_id'] = requester_user_id
    context.user_data['withdrawal_amount'] = amount_to_deduct
    context.user_data['admin_action'] = "awaiting_withdrawal_screenshot"

    # Escape the entire original message to ensure no unescaped characters remain
    original_message = query.message.text_markdown_v2
    await query.edit_message_text(
        text=f"{original_message}\n\n{escape_markdown_v2_text('📸 Please send the screenshot of the payment confirmation.')}",
        parse_mode='MarkdownV2'
    )
    logger.info(f"Admin {query.from_user.id} initiated withdrawal approval for user {requester_user_id}, awaiting screenshot.")

async def process_withdrawal_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the screenshot sent by the admin and notifies the user."""
    admin = update.effective_user
    if 'admin_action' not in context.user_data or context.user_data['admin_action'] != "awaiting_withdrawal_screenshot":
        await update.message.reply_text(
            "⚠️ No pending withdrawal screenshot request.",
            parse_mode='MarkdownV2'
        )
        return

    if not update.message.photo:
        await update.message.reply_text(
            "📸 *Please send an actual photo of the payment confirmation.*",
            parse_mode='MarkdownV2'
        )
        return

    requester_user_id = context.user_data.get('withdrawal_user_id')
    amount_to_deduct = context.user_data.get('withdrawal_amount')
    photo_file_id = update.message.photo[-1].file_id

    db_user = User.find(requester_user_id)
    if not db_user or not db_user.withdrawal_request_pending:
        await update.message.reply_text(
            f"⚠️ *Request for user ID {requester_user_id} not found or already processed.*",
            parse_mode='MarkdownV2'
        )
        return

    db_user.referral_balance -= amount_to_deduct
    db_user.withdrawal_request_pending = False
    db_user.withdrawal_bank = None
    db_user.withdrawal_account_number = None
    db_user.withdrawal_account_holder = None
    db_user.save()

    try:
        await context.bot.send_photo(
            chat_id=requester_user_id,
            photo=photo_file_id,
            caption=(
                f"✅ *Withdrawal Successful*\n\n"
                f"{escape_markdown_v2_text(f'Your withdrawal request for {amount_to_deduct:.2f} ETB has been approved and processed! ')}"
                f"{escape_markdown_v2_text('The funds should appear in your account shortly. Here is the payment confirmation:')}"
            ),
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
    except Exception as e:
        logger.error(f"Failed to send withdrawal approval notification to user {requester_user_id}: {e}")

    await update.message.reply_text(
        f"✅ *Withdrawal Processed*\n\n"
        f"{escape_markdown_v2_text(f'Withdrawal for user ID {requester_user_id} ({amount_to_deduct:.2f} ETB) has been approved and the screenshot sent.')}",
        parse_mode='MarkdownV2'
    )
    logger.info(f"Withdrawal for user {requester_user_id} approved by admin {admin.id} with screenshot.")

    del context.user_data['withdrawal_user_id']
    del context.user_data['withdrawal_amount']
    del context.user_data['admin_action']

async def decline_withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin's 'Not Sent' button for a withdrawal."""
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

    db_user.withdrawal_request_pending = False
    db_user.withdrawal_bank = None
    db_user.withdrawal_account_number = None
    db_user.withdrawal_account_holder = None
    db_user.save()

    try:
        await context.bot.send_message(
            chat_id=requester_user_id,
            text=(
                "😔 *Withdrawal Request Declined*\n\n"
                f"{escape_markdown_v2_text('Your withdrawal request could not be approved at this time. ')}"
                f"{escape_markdown_v2_text('This might be due to an issue with the provided account details. Please double-check them and try again later. ')}"
                f"{escape_markdown_v2_text('If you believe this is an error, contact support.')}"
            ),
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
    except Exception as e:
        logger.error(f"Failed to send withdrawal decline notification to user {requester_user_id}: {e}")

    await query.edit_message_text(
        text=query.message.text_markdown_v2 + f"\n\n*❌ Declined by {query.from_user.first_name}.*",
        parse_mode='MarkdownV2'
    )
    logger.info(f"Withdrawal for user {requester_user_id} declined by admin {query.from_user.id}.")