# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the Telegram Bot.
    Loads sensitive information from environment variables.
    """
    # Telegram Bot Token
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("WARNING: TELEGRAM_TOKEN is not set in environment variables or .env file. Please set it.")

    # MongoDB Connection
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "acebot_db")

    # Google Gemini AI API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("WARNING: GEMINI_API_KEY is not set in environment variables or .env file. Please set it.")

    # Google Drive Service Account Credentials Path
    # Ensure 'credentials.json' is in the same directory as your bot's main script
    GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH", "credentials.json")

    # Telegram User IDs for Payment Moderators (replace with actual IDs)
    # These users will receive payment verification requests and can use the /approve command.
    PAYMENT_MODERATORS = [
        int(os.getenv("MOD_ID_1", "8188221245")), # Replace with actual moderator ID
        # Add more moderator IDs as needed
    ]
    if 123456789 in PAYMENT_MODERATORS:
        print("WARNING: PAYMENT_MODERATORS are default. Replace with actual Telegram user IDs.")


    # Google Drive Folder IDs for Resources
    # IMPORTANT: Replace these with your actual Google Drive folder IDs.
    # Each folder should contain the respective educational materials.
    DRIVE_FOLDER_IDS = {
        # Textbooks
        "natural_grade9_textbooks": "1BnHNB6qq81BJ5TffaL1pIFhpnKkTvQJx",
        "natural_grade10_textbooks": "YOUR_NATURAL_GRADE10_TEXTBOOKS_FOLDER_ID",
        "natural_grade11_textbooks": "YOUR_NATURAL_GRADE11_TEXTBOOKS_FOLDER_ID",
        "natural_grade12_textbooks": "YOUR_NATURAL_GRADE12_TEXTBOOKS_FOLDER_ID",
        "social_grade9_textbooks": "YOUR_SOCIAL_GRADE9_TEXTBOOKS_FOLDER_ID",
        "social_grade10_textbooks": "YOUR_SOCIAL_GRADE10_TEXTBOOKS_FOLDER_ID",
        "social_grade11_textbooks": "YOUR_SOCIAL_GRADE11_TEXTBOOKS_FOLDER_ID",
        "social_grade12_textbooks": "YOUR_SOCIAL_GRADE12_TEXTBOOKS_FOLDER_ID",

        # Teacher's Guides
        "natural_grade9_teachers_guide": "YOUR_NATURAL_GRADE9_GUIDE_FOLDER_ID",
        "natural_grade10_teachers_guide": "YOUR_NATURAL_GRADE10_GUIDE_FOLDER_ID",
        "natural_grade11_teachers_guide": "YOUR_NATURAL_GRADE11_GUIDE_FOLDER_ID",
        "natural_grade12_teachers_guide": "YOUR_NATURAL_GRADE12_GUIDE_FOLDER_ID",
        "social_grade9_teachers_guide": "YOUR_SOCIAL_GRADE9_GUIDE_FOLDER_ID",
        "social_grade10_teachers_guide": "YOUR_SOCIAL_GRADE10_GUIDE_FOLDER_ID",
        "social_grade11_teachers_guide": "YOUR_SOCIAL_GRADE11_GUIDE_FOLDER_ID",
        "social_grade12_teachers_guide": "YOUR_SOCIAL_GRADE12_GUIDE_FOLDER_ID",

        # Short Notes
        "natural_math_notes": "YOUR_NATURAL_MATH_NOTES_FOLDER_ID",
        "natural_english_notes": "YOUR_NATURAL_ENGLISH_NOTES_FOLDER_ID",
        "natural_physics_notes": "YOUR_NATURAL_PHYSICS_NOTES_FOLDER_ID",
        "natural_biology_notes": "YOUR_NATURAL_BIOLOGY_NOTES_FOLDER_ID",
        "natural_chemistry_notes": "YOUR_NATURAL_CHEMISTRY_NOTES_FOLDER_ID",
        "natural_aptitude_notes": "YOUR_NATURAL_APTITUDE_NOTES_FOLDER_ID",
        "social_math_notes": "YOUR_SOCIAL_MATH_NOTES_FOLDER_ID",
        "social_english_notes": "YOUR_SOCIAL_ENGLISH_NOTES_FOLDER_ID",
        "social_geography_notes": "YOUR_SOCIAL_GEOGRAPHY_NOTES_FOLDER_ID",
        "social_history_notes": "YOUR_SOCIAL_HISTORY_NOTES_FOLDER_ID",
        "social_economics_notes": "YOUR_SOCIAL_ECONOMICS_NOTES_FOLDER_ID",
        "social_aptitude_notes": "YOUR_SOCIAL_APTITUDE_NOTES_FOLDER_ID",

        # Cheat Sheets
        "natural_math_cheats": "YOUR_NATURAL_MATH_CHEATS_FOLDER_ID",
        "natural_english_cheats": "YOUR_NATURAL_ENGLISH_CHEATS_FOLDER_ID",
        "natural_physics_cheats": "YOUR_NATURAL_PHYSICS_CHEATS_FOLDER_ID",
        "natural_biology_cheats": "YOUR_NATURAL_BIOLOGY_CHEATS_FOLDER_ID",
        "natural_chemistry_cheats": "YOUR_NATURAL_CHEMISTRY_CHEATS_FOLDER_ID",
        "natural_aptitude_cheats": "YOUR_NATURAL_APTITUDE_CHEATS_FOLDER_ID",
        "social_math_cheats": "YOUR_SOCIAL_MATH_CHEATS_FOLDER_ID",
        "social_english_cheats": "YOUR_SOCIAL_ENGLISH_CHEATS_FOLDER_ID",
        "social_geography_cheats": "YOUR_SOCIAL_GEOGRAPHY_CHEATS_FOLDER_ID",
        "social_history_cheats": "YOUR_SOCIAL_HISTORY_CHEATS_FOLDER_ID",
        "social_economics_cheats": "YOUR_SOCIAL_ECONOMICS_CHEATS_FOLDER_ID",
        "social_aptitude_cheats": "YOUR_SOCIAL_APTITUDE_CHEATS_FOLDER_ID",

        # Quizzes
        "natural_math_quizzes": "YOUR_NATURAL_MATH_QUIZZES_FOLDER_ID",
        "natural_english_quizzes": "YOUR_NATURAL_ENGLISH_QUIZZES_FOLDER_ID",
        "natural_physics_quizzes": "YOUR_NATURAL_PHYSICS_QUIZZES_FOLDER_ID",
        "natural_biology_quizzes": "YOUR_NATURAL_BIOLOGY_QUIZZES_FOLDER_ID",
        "natural_chemistry_quizzes": "YOUR_NATURAL_CHEMISTRY_QUIZZES_FOLDER_ID",
        "natural_aptitude_quizzes": "YOUR_NATURAL_APTITUDE_QUIZZES_FOLDER_ID",
        "social_math_quizzes": "YOUR_SOCIAL_MATH_QUIZZES_FOLDER_ID",
        "social_english_quizzes": "YOUR_SOCIAL_ENGLISH_QUIZZES_FOLDER_ID",
        "social_geography_quizzes": "YOUR_SOCIAL_GEOGRAPHY_QUIZZES_FOLDER_ID",
        "social_history_quizzes": "YOUR_SOCIAL_HISTORY_QUIZZES_FOLDER_ID",
        "social_economics_quizzes": "YOUR_SOCIAL_ECONOMICS_QUIZZES_FOLDER_ID",
        "social_aptitude_quizzes": "YOUR_SOCIAL_APTITUDE_QUIZZES_FOLDER_ID",

        # Past Exams
        **{f"natural_{year}_exam": f"YOUR_NATURAL_{year}_EXAM_FOLDER_ID" for year in range(2000, 2018)},
        **{f"social_{year}_exam": f"YOUR_SOCIAL_{year}_EXAM_FOLDER_ID" for year in range(2000, 2018)},

        # Exam Tips
        "natural_exam_tips": "YOUR_NATURAL_EXAM_TIPS_FOLDER_ID",
        "social_exam_tips": "YOUR_SOCIAL_EXAM_TIPS_FOLDER_ID",

        # Study Tips
        "natural_study_tips": "YOUR_NATURAL_STUDY_TIPS_FOLDER_ID",
        "social_study_tips": "YOUR_SOCIAL_STUDY_TIPS_FOLDER_ID",
    }


class MenuItems:
    """
    Defines the text for various menu buttons to ensure consistency across the bot.
    """
    RESOURCES = "📚 Resources"
    QUIZZES = "🧠 Quizzes"
    MOTIVATION = "✨ Motivation"
    AI_CHAT = "🤖 AI Chat"
    PAST_EXAMS = "📝 Past Exams"
    EXAM_TIPS = "💡 Exam Tips"
    STUDY_TIPS = "📖 Study Tips"
    ASSIGNMENT_HELP = "✍️ Assignment Help"
    UPGRADE = "💎 Upgrade"
    HELP = "🆘 Help"
    CONTACT_US = "📧 Contact Us"
    INVITE_AND_EARN = "🤝 Invite and Earn"
    EXIT_AI_CHAT = "⬅️ Exit AI Chat"
    TEXT_BOOKS = "📖 Text Books"
    SHORT_NOTES = "📝 Short Notes"