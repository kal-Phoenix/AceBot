# keyboards.py
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import MenuItems as MI


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
            [MI.UPGRADE, MI.HELP, MI.CONTACT_US]
        ], resize_keyboard=True)

    @staticmethod
    def resources_menu():
        """Generates the resources menu keyboard."""
        return ReplyKeyboardMarkup([
            ["📖 Text Books", "📚 Teacher's Guide"],
            ["📝 Short Notes", "🧮 Cheat Sheets"],
            ["⬅️ Back to Main Menu"]
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
        if stream == "natural":
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Physics", "Biology"],
                ["Chemistry", "Aptitude"],
                ["⬅️ Back to Resources"]
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Geography", "History"],
                ["Economics", "Aptitude"],
                ["⬅️ Back to Resources"]
            ], resize_keyboard=True)

    @staticmethod
    def cheat_sheets_menu(stream: str):
        """
        Generates a menu for selecting cheat sheet types based on the user's stream.
        :param stream: The user's academic stream ('natural' or 'social').
        """
        if stream == "natural":
            return ReplyKeyboardMarkup([
                ["🧮 Math Formulas", "📝 English Tips"],
                ["⚛ Physics Formulas", "🧬 Biology Cheats"],
                ["🧪 Chemistry Cheats", "🧠 Aptitude Tricks"],
                ["⬅️ Back to Resources"]
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["🧮 Math Formulas", "📝 English Tips"],
                ["🗺 Geography Cheats", "📜 History Cheats"],
                ["💹 Economics Cheats", "🧠 Aptitude Tricks"],
                ["⬅️ Back to Resources"]
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
                ["⬅️ Back to Main Menu"]  # Quizzes go back to main menu
            ], resize_keyboard=True)
        else:  # social stream
            return ReplyKeyboardMarkup([
                ["Mathematics", "English"],
                ["Geography", "History"],
                ["Economics", "Aptitude"],
                ["⬅️ Back to Main Menu"]  # Quizzes go back to main menu
            ], resize_keyboard=True)

    @staticmethod
    def past_exams_years_menu():
        """
        Generates a menu for selecting past exam years (2000-2017).
        """
        years = list(range(2000, 2018))  # Years from 2000 to 2017 inclusive
        keyboard = []
        # Arrange years in rows of 4 for better display
        for i in range(0, len(years), 4):
            keyboard.append([str(year) for year in years[i:i + 4]])

        keyboard.append(["⬅️ Back to Main Menu"])  # Add back button
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
    def upgrade_menu(): # NEW: Menu for upgrade process
        """
        Generates the menu for the upgrade process, asking about payment status.
        """
        return ReplyKeyboardMarkup([
            ["✅ Yes, I have paid"],
            ["❌ No, I haven't paid yet"],
            ["⬅️ Back to Main Menu"]
        ], resize_keyboard=True)

    @staticmethod
    def admin_payment_approval_keyboard(user_id: int): # NEW: Inline keyboard for admin approval
        """
        Generates an inline keyboard for admin to approve or decline a payment request.
        The callback data includes the user_id to identify the request.
        """
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user_id}")
            ]
        ])