# handlers/payment_handlers.py
import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.models import User
from config import Config, MenuItems as MI
from keyboards import Keyboards

logger = logging.getLogger(__name__)


async def upgrade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'Upgrade' menu button.
    Asks the user if they have paid for premium access.
    """
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user:
        # Import user_handlers here to avoid circular dependency
        from handlers import user_handlers
        await user_handlers.start(update, context)  # Ensure user exists
        return

    if db_user.is_premium:
        await update.message.reply_text(
            "🎉 You are already a premium member\\! Enjoy your full access\\.",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"User {user.id} attempted to upgrade but is already premium.")
        return

    if db_user.pending_admin_approval:
        await update.message.reply_text(
            "⏳ Your premium request is currently under review by an admin\\. Please be patient\\.",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"User {user.id} attempted to upgrade but has a pending request.")
        return

    await update.message.reply_text(
        "To upgrade to premium, please make your payment and then select 'Yes, I have paid'\\.\n\n"
        "Payment Details: \\[Your Bank Name\\]\\, Account No\\: \\[Your Account Number\\]\\, Beneficiary\\: \\[Your Name/Company Name\\]\n"
        "Alternatively, you can pay via \\[Mobile Money/Other Payment Method\\]\\: \\[Your Mobile Money Number\\]",
        parse_mode='MarkdownV2',
        reply_markup=Keyboards.upgrade_menu()
    )
    db_user.pending_action = "await_payment_status_choice"
    db_user.save()
    logger.info(f"User {user.id} initiated upgrade process, awaiting payment status choice.")


async def handle_payment_status_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's choice after pressing the 'Upgrade' button.
    Routes to name input or explains payment.
    """
    text = update.message.text
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or db_user.pending_action != "await_payment_status_choice":
        # Should not happen if flow is correct, but as a safeguard
        await update.message.reply_text("Something went wrong\\. Please try /start again\\.", parse_mode='MarkdownV2',
                                        reply_markup=Keyboards.main_menu())
        db_user.pending_action = None
        db_user.save()
        logger.warning(f"User {user.id} in unexpected state for payment status choice.")
        return

    if text == "✅ Yes, I have paid":
        await update.message.reply_text(
            "Great\\! Please tell me your *Full Name* as it appears on the payment receipt\\.",
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardRemove()  # Remove keyboard for text input
        )
        db_user.pending_action = "await_name_for_payment"
        db_user.save()
        logger.info(f"User {user.id} chose 'Yes, I have paid', awaiting name.")
    elif text == "❌ No, I haven't paid yet":
        await update.message.reply_text(
            "No problem\\! You can upgrade anytime\\. Remember the payment details:\\\n\\\n"
            "Payment Details: \\[Your Bank Name\\]\\, Account No\\: \\[Your Account Number\\]\\, Beneficiary\\: \\[Your Name/Company Name\\]\\\n"
            "Alternatively, you can pay via \\[Mobile Money/Other Payment Method\\]\\: \\[Your Mobile Money Number\\]",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        db_user.pending_action = None
        db_user.save()
        logger.info(f"User {user.id} chose 'No, I haven't paid yet'.")
    elif text == "⬅️ Back to Main Menu":
        db_user.pending_action = None
        db_user.save()
        await update.message.reply_text("Going back to main menu\\.", parse_mode='MarkdownV2',
                                        reply_markup=Keyboards.main_menu())
        logger.info(f"User {user.id} navigated back to main menu from upgrade choice.")
    else:
        await update.message.reply_text(
            "Please use the buttons provided to select your payment status\\.",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.upgrade_menu()
        )
        logger.warning(f"User {user.id} sent invalid input for payment status choice: {text}")


async def process_name_for_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes the full name provided by the user for payment.
    Then asks for the payment proof screenshot.
    """
    full_name = update.message.text
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or db_user.pending_action != "await_name_for_payment":
        # This case should ideally not happen if state management is correct
        await update.message.reply_text("Something went wrong\\. Please try /start again\\.", parse_mode='MarkdownV2',
                                        reply_markup=Keyboards.main_menu())
        db_user.pending_action = None
        db_user.save()
        logger.warning(f"User {user.id} in unexpected state for name input: {full_name}.")
        return

    db_user.full_name = full_name.strip()
    db_user.pending_action = "await_payment_proof"
    db_user.save()
    logger.info(f"User {user.id} provided name: {full_name}, awaiting payment proof.")

    await update.message.reply_text(
        f"Thank you, {full_name.strip()}\\! Now, please send the *screenshot of your payment receipt*\\.",
        parse_mode='MarkdownV2'
        # ReplyKeyboardRemove() is already active from previous step.
    )


async def process_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receives the payment proof screenshot and forwards it to admins.
    """
    user = update.effective_user
    db_user = User.find(user.id)

    if not db_user or db_user.pending_action != "await_payment_proof":
        # Ensure the user is in the correct state to send a photo
        await update.message.reply_text("Please initiate the upgrade process first using the '💎 Upgrade' button\\.",
                                        parse_mode='MarkdownV2',
                                        reply_markup=Keyboards.main_menu())
        logger.warning(f"User {user.id} sent photo when not awaiting payment proof.")
        return

    if not update.message.photo:
        await update.message.reply_text("Please send an actual *photo* of your payment receipt, not just text\\.",
                                        parse_mode='MarkdownV2')
        logger.warning(f"User {user.id} sent non-photo when awaiting payment proof.")
        return

    # Get the file ID of the largest photo
    photo_file_id = update.message.photo[-1].file_id

    db_user.payment_proof = photo_file_id
    db_user.payment_pending = True
    db_user.pending_admin_approval = True
    db_user.pending_action = None  # Clear pending action
    db_user.save()
    logger.info(f"User {user.id} submitted payment proof, request pending admin approval.")

    await update.message.reply_text(
        "Thank you\\! Your payment proof has been received and sent to the admin for review\\. "
        "We will notify you once your premium access is approved\\. This usually takes 24\\-48 hours\\.",
        parse_mode='MarkdownV2',
        reply_markup=Keyboards.main_menu()  # Return to main menu
    )

    # Notify admin(s)
    for admin_id in Config.PAYMENT_MODERATORS:
        try:
            admin_message = (
                f"🚨 \\*\\*New Premium Request\\*\\* from user {user.first_name} \\(@{user.username or 'N/A'}\\) \\(ID\\: {user.id}\\)\n\n"
                f"\\*\\*Full Name\\*\\*: {db_user.full_name}\n"
                f"\\*\\*Request Status\\*\\*: Awaiting Approval\n"
            )
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=photo_file_id,
                caption=admin_message,
                reply_markup=Keyboards.admin_payment_approval_keyboard(user.id),
                parse_mode='MarkdownV2'
            )
            logger.info(f"Payment proof from user {user.id} forwarded to admin {admin_id}.")
        except Exception as e:
            logger.error(f"Failed to send payment notification to admin {admin_id}: {e}")


# Admin Handlers (Now part of payment_handlers)

async def approve_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles admin's 'Approve' button click for a payment request.
    """
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    requester_user_id = int(query.data.split('_')[1])
    db_user = User.find(requester_user_id)

    if not db_user:
        await query.edit_message_text("User not found in database\\.", parse_mode='MarkdownV2', reply_markup=None)
        logger.warning(f"Admin tried to approve for non-existent user: {requester_user_id}")
        return

    if db_user.is_premium:
        await query.edit_message_text(
            f"🚫 This user \\(ID\\: {requester_user_id}\\) is \\*already premium\\*\\.",
            parse_mode='MarkdownV2',
            reply_markup=None
        )
        logger.info(f"Admin tried to approve already premium user {requester_user_id}.")
        return

    db_user.is_premium = True
    db_user.payment_pending = False
    db_user.pending_admin_approval = False
    db_user.payment_proof = None  # Clear proof after approval
    db_user.full_name = None  # Clear name after approval
    db_user.save()
    logger.info(f"Premium access approved for user {requester_user_id} by admin {query.from_user.id}.")

    # Notify the user
    try:
        await context.bot.send_message(
            chat_id=requester_user_id,
            text="🎉 Congratulations\\! Your premium access has been approved\\. You now have full access to all features\\!",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"User {requester_user_id} notified of premium approval.")
    except Exception as e:
        logger.error(f"Failed to notify user {requester_user_id} of premium approval: {e}")

    # Update the admin's message
    await query.edit_message_text(
        f"✅ You have approved premium access for user \\(ID\\: {requester_user_id}\\) \\({db_user.full_name or 'N/A'}\\)\\.",
        parse_mode='MarkdownV2',
        reply_markup=None  # Remove buttons after action
    )


async def decline_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles admin's 'Decline' button click for a payment request.
    """
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    requester_user_id = int(query.data.split('_')[1])
    db_user = User.find(requester_user_id)

    if not db_user:
        await query.edit_message_text("User not found in database\\.", parse_mode='MarkdownV2', reply_markup=None)
        logger.warning(f"Admin tried to decline for non-existent user: {requester_user_id}")
        return

    if not db_user.payment_pending and not db_user.pending_admin_approval:
        await query.edit_message_text(
            f"ℹ️ This request from user \\(ID\\: {requester_user_id}\\) is no longer pending or was already processed\\.",
            parse_mode='MarkdownV2',
            reply_markup=None
        )
        logger.info(f"Admin tried to decline an inactive request for user {requester_user_id}.")
        return

    db_user.is_premium = False
    db_user.payment_pending = False
    db_user.pending_admin_approval = False
    db_user.payment_proof = None  # Clear proof after decline
    db_user.full_name = None  # Clear name after decline
    db_user.save()
    logger.info(f"Premium request declined for user {requester_user_id} by admin {query.from_user.id}.")

    # Notify the user
    try:
        await context.bot.send_message(
            chat_id=requester_user_id,
            text="😔 Unfortunately, your premium request could not be approved at this time\\. "
                 "Please ensure your payment details and screenshot are clear and correct, then try again via the '💎 Upgrade' button\\. "
                 "If you believe this is an error, please contact support\\.",
            parse_mode='MarkdownV2',
            reply_markup=Keyboards.main_menu()
        )
        logger.info(f"User {requester_user_id} notified of premium decline.")
    except Exception as e:
        logger.error(f"Failed to notify user {requester_user_id} of premium decline: {e}")

    # Update the admin's message
    await query.edit_message_text(
        f"❌ Premium request for user {requester_user_id} has been \\*declined\\* by {query.from_user.first_name}\\.",
        parse_mode='MarkdownV2',
        reply_markup=None  # Remove buttons after action
    )


# Import user_handlers at the end to avoid circular dependency
from handlers import user_handlers