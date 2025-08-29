# keyboards.py
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import MenuItems as MI, Config
import math

class Keyboards:
    """
    A collection of static methods to generate different ReplyKeyboardMarkup objects
    for the Telegram bot's user interface.
    """

    @staticmethod
    def main_menu():
        """Generates the main menu keyboard."""
        return ReplyKeyboardMarkup([
            [MI.RESOURCES, MI.QUIZZES],
            [MI.MOTIVATION, MI.AI_CHAT],
            [MI.PAST_EXAMS, MI.EXAM_TIPS],
            [MI.STUDY_TIPS, MI.ASSIGNMENT_HELP],
            [MI.UPGRADE, MI.INVITE_AND_EARN],
            [MI.HELP, MI.CONTACT_US]
        ], resize_keyboard=True)

    @staticmethod
    def invite_menu():
        """Generates the menu for the 'Invite and Earn' feature."""
        return ReplyKeyboardMarkup([
            [MI.SHARE_INVITE, MI.REQUEST_WITHDRAWAL],
            [MI.BACK_TO_MAIN_MENU]
        ], resize_keyboard=True)

    @staticmethod
    def invite_inline_menu():
        """Generates an inline menu for the 'Invite and Earn' feature."""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("↗️ Share Invite", callback_data="share_invite"),
                InlineKeyboardButton("💰 Request Withdrawal", callback_data="request_withdrawal")
            ],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main_menu")]
        ])

    @staticmethod
    def share_menu(share_url: str, share_text: str):
        """Generates an inline keyboard with a button to share the referral link."""
        from urllib.parse import quote
        encoded_text = quote(share_text)

        return InlineKeyboardMarkup([
            [InlineKeyboardButton("↗️ Share on Telegram",
                                  url=f"https://t.me/share/url?url={share_url}&text={encoded_text}")]
        ])

    @staticmethod
    def withdrawal_banks_menu():
        """Generates a menu of available banks for withdrawal."""
        banks = Config.AVAILABLE_BANKS
        keyboard = [banks[i:i + 2] for i in range(0, len(banks), 2)]
        keyboard.append([MI.BACK_TO_MAIN_MENU])
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def withdrawal_banks_inline_menu():
        """Generates an inline menu of available banks for withdrawal."""
        banks = Config.AVAILABLE_BANKS
        keyboard = [[InlineKeyboardButton(bank, callback_data=f"bank_{bank}")] for bank in banks]
        keyboard.append([InlineKeyboardButton("⬅️ Back to Invite Menu", callback_data="back_to_invite_menu")])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def admin_withdrawal_approval_keyboard(user_id: int, amount: float):
        """Generates an inline keyboard for admin to approve or decline a withdrawal request."""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Sent", callback_data=f"approve_withdrawal_{user_id}_{amount}"),
                InlineKeyboardButton("❌ Not Sent", callback_data=f"decline_withdrawal_{user_id}")
            ]
        ])

    @staticmethod
    def resources_menu():
        """Generates the resources menu keyboard."""
        return ReplyKeyboardMarkup([
            ["📖 Text Books", "📚 Teacher's Guide"],
            ["📝 Short Notes", "🧮 Cheat Sheets"],
            [MI.BACK_TO_MAIN_MENU]
        ], resize_keyboard=True)

    @staticmethod
    def grades_menu(purpose: str):
        """
        Generates a menu for selecting grade levels (9-12).
        :param purpose: A string to append to the grade (e.g., "Textbooks", "Guide").
        """
        return ReplyKeyboardMarkup([
            [f"Grade 9 {purpose}", f"Grade 10 {purpose}"],
            [f"Grade 11 {purpose}", f"Grade 12 {purpose}"],
            ["⬅️ Back to Resources"]
        ], resize_keyboard=True)

    @staticmethod
    def subjects_menu(stream: str):
        """
        Generates a menu for selecting subjects based on the user's stream.
        :param stream: The user's academic stream ('natural' or 'social').
        """
        back_button = "⬅️ Back to Resources"
        if stream == "natural":
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Physics", "Biology"],
                ["Chemistry", "Aptitude"],
                [back_button]
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Geography", "History"],
                ["Economics", "Aptitude"],
                [back_button]
            ], resize_keyboard=True)

    @staticmethod
    def cheat_sheets_menu(stream: str):
        """
        Generates a menu for selecting cheat sheet types based on the user's stream.
        :param stream: The user's academic stream ('natural' or 'social').
        """
        back_button = "⬅️ Back to Resources"
        if stream == "natural":
            return ReplyKeyboardMarkup([
                ["🧮 Math Formulas", "📝 English Tips"],
                ["⚛ Physics Formulas", "🧬 Biology Cheats"],
                ["🧪 Chemistry Cheats", "🧠 Aptitude Tricks"],
                [back_button]
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["🧮 Math Formulas", "📝 English Tips"],
                ["🗺 Geography Cheats", "📜 History Cheats"],
                ["💹 Economics Cheats", "🧠 Aptitude Tricks"],
                [back_button]
            ], resize_keyboard=True)

    @staticmethod
    def quizzes_menu(stream: str):
        """
        Generates a menu for selecting quiz subjects based on the user's stream.
        :param stream: The user's academic stream ('natural' or 'social').
        """
        if stream == "natural":
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Physics", "Biology"],
                ["Chemistry", "Aptitude"],
                [MI.BACK_TO_MAIN_MENU]
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Geography", "History"],
                ["Economics", "Aptitude"],
                [MI.BACK_TO_MAIN_MENU]
            ], resize_keyboard=True)

    @staticmethod
    def quiz_grades_menu():
        """
        Generates a menu for selecting quiz grades (9-12 or Mixed).
        """
        return ReplyKeyboardMarkup([
            ["Grade 9", "Grade 10"],
            ["Grade 11", "Grade 12"],
            ["Mixed"],
            [MI.BACK_TO_MAIN_MENU]
        ], resize_keyboard=True)

    @staticmethod
    def quiz_post_menu():
        """Menu shown after sending a quiz file."""
        return ReplyKeyboardMarkup([
            [MI.ANOTHER_QUIZ, MI.EXIT_QUIZZES]
        ], resize_keyboard=True)

    @staticmethod
    def past_exams_years_menu():
        """
        Generates a menu for selecting past exam years (2000-2017).
        """
        years = list(range(2000, 2018))
        keyboard = []
        for i in range(0, len(years), 4):
            keyboard.append([str(year) for year in years[i:i + 4]])
        keyboard.append([MI.BACK_TO_MAIN_MENU])
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def ai_chat_menu():
        """
        Generates a special menu for AI chat mode, with only an exit button.
        """
        return ReplyKeyboardMarkup([
            [MI.EXIT_AI_CHAT]
        ], resize_keyboard=True)

    @staticmethod
    def upgrade_menu():
        """
        Generates the menu for the upgrade process, asking about payment status.
        """
        return ReplyKeyboardMarkup([
            ["✅ Yes, I have paid"],
            ["❌ No, I haven't paid yet"],
            [MI.BACK_TO_MAIN_MENU]
        ], resize_keyboard=True)

    @staticmethod
    def admin_payment_approval_keyboard(user_id: int):
        """
        Generates an inline keyboard for admin to approve or decline a payment request.
        """
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user_id}")
            ]
        ])