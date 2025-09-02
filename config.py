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
    GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH", "credentials.json")

    ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "YOUR_ADMIN_BOT_TOKEN_HERE")
    if ADMIN_BOT_TOKEN == "YOUR_ADMIN_BOT_TOKEN_HERE":
        print("WARNING: ADMIN_BOT_TOKEN is not set in environment variables or .env file. Please set it.")
    ADMIN_IDS = [8188221245]
    # Telegram User IDs for Payment Moderators
    PAYMENT_MODERATORS = [
        int(os.getenv("MOD_ID_1", "8188221245")),
    ]
    if 123456789 in PAYMENT_MODERATORS:
        print("WARNING: PAYMENT_MODERATORS are default. Replace with actual Telegram user IDs.")

    # Withdrawal Configuration
    MIN_WITHDRAWAL_AMOUNT = 50.0

    # Available banks for withdrawal
    AVAILABLE_BANKS = [
        "Bank of Abyssinia", "Wegagen Bank", "Dashen Bank",
        "Oromia International Bank", "Commercial Bank of Ethiopia (CBE)",
        "Hibret Bank", "Awash Bank", "Telebirr"
    ]

    # Bank account details for premium upgrades
    BANK_ACCOUNTS = {
        "Commercial Bank of Ethiopia (CBE)": os.getenv("CBE_ACCOUNT", "YOUR_CBE_ACCOUNT_NUMBER"),
        "Dashen Bank": os.getenv("DASHEN_ACCOUNT", "YOUR_DASHEN_ACCOUNT_NUMBER"),
        "Bank of Abyssinia": os.getenv("BOA_ACCOUNT", "YOUR_BOA_ACCOUNT_NUMBER"),
        "Awash Bank": os.getenv("AWASH_ACCOUNT", "YOUR_AWASH_ACCOUNT_NUMBER"),
        "Oromia International Bank": os.getenv("OROMIA_ACCOUNT", "YOUR_OROMIA_ACCOUNT_NUMBER"),
        "Hibret Bank": os.getenv("HIBIR_ACCOUNT", "YOUR_HIBIR_ACCOUNT_NUMBER"),
        "Telebirr": os.getenv("TELEBIRR_ACCOUNT", "YOUR_TELEBIRR_NUMBER")
    }
    BENEFICIARY_NAME = os.getenv("BENEFICIARY_NAME", "YOUR_NAME_OR_COMPANY_NAME")
    if BENEFICIARY_NAME == "YOUR_NAME_OR_COMPANY_NAME":
        print("WARNING: BENEFICIARY_NAME is not set in environment variables or .env file. Please set it.")

    # =============================================================================
    # 📁 GOOGLE DRIVE FOLDER IDS CONFIGURATION
    # =============================================================================
    # This section contains all Google Drive folder IDs for different resources.
    # Replace "YOUR_*_FOLDER_ID" with actual Google Drive folder IDs.
    # 
    # 📋 FOLDER STRUCTURE:
    #   - {stream}_{grade}_{resource_type}     (for grade-specific resources)
    #   - {stream}_{subject}_{resource_type}   (for subject-specific resources)
    #   - {stream}_{year}_exam                 (for year-specific past exams)
    # 
    # 🎯 STREAMS: natural, social
    # 📚 RESOURCES: textbooks, teachers_guide, notes, cheats, quizzes, past_exams
    # 📖 SUBJECTS: math, english, physics, biology, chemistry, aptitude, geography, history, economics
    # 🎓 GRADES: grade9, grade10, grade11, grade12, mixed
    # 📅 YEARS: 2000-2017 (for past exams)
    # =============================================================================
    
    DRIVE_FOLDER_IDS = {
        # =============================================================================
        # 📚 TEXTBOOKS (Free Resources)
        # =============================================================================
        # Grade-specific textbooks for both Natural and Social streams
        
        # Natural Stream Textbooks
        "natural_grade9_textbooks": "1BnHNB6qq81BJ5TffaL1pIFhpnKkTvQJx",  # ✅ Configured
        "natural_grade10_textbooks": "YOUR_NATURAL_GRADE10_TEXTBOOKS_FOLDER_ID",
        "natural_grade11_textbooks": "YOUR_NATURAL_GRADE11_TEXTBOOKS_FOLDER_ID",
        "natural_grade12_textbooks": "YOUR_NATURAL_GRADE12_TEXTBOOKS_FOLDER_ID",
        
        # Social Stream Textbooks
        "social_grade9_textbooks": "YOUR_SOCIAL_GRADE9_TEXTBOOKS_FOLDER_ID",
        "social_grade10_textbooks": "YOUR_SOCIAL_GRADE10_TEXTBOOKS_FOLDER_ID",
        "social_grade11_textbooks": "YOUR_SOCIAL_GRADE11_TEXTBOOKS_FOLDER_ID",
        "social_grade12_textbooks": "YOUR_SOCIAL_GRADE12_TEXTBOOKS_FOLDER_ID",
        
        # =============================================================================
        # 📖 TEACHER'S GUIDES (Free Resources)
        # =============================================================================
        # Grade-specific teacher's guides for both streams
        
        # Natural Stream Teacher's Guides
        "natural_grade9_teachers_guide": "YOUR_NATURAL_GRADE9_GUIDE_FOLDER_ID",
        "natural_grade10_teachers_guide": "YOUR_NATURAL_GRADE10_GUIDE_FOLDER_ID",
        "natural_grade11_teachers_guide": "YOUR_NATURAL_GRADE11_GUIDE_FOLDER_ID",
        "natural_grade12_teachers_guide": "YOUR_NATURAL_GRADE12_GUIDE_FOLDER_ID",
        
        # Social Stream Teacher's Guides
        "social_grade9_teachers_guide": "YOUR_SOCIAL_GRADE9_GUIDE_FOLDER_ID",
        "social_grade10_teachers_guide": "YOUR_SOCIAL_GRADE10_GUIDE_FOLDER_ID",
        "social_grade11_teachers_guide": "YOUR_SOCIAL_GRADE11_GUIDE_FOLDER_ID",
        "social_grade12_teachers_guide": "YOUR_SOCIAL_GRADE12_GUIDE_FOLDER_ID",
        
        # =============================================================================
        # 📝 SHORT NOTES (Premium Resources)
        # =============================================================================
        # Subject-specific short notes for both streams
        
        # Natural Stream Short Notes
        "natural_math_notes": "1ACN3bhZRv_XzuU7X1hwIvlUbBo24mTS_",
        "natural_english_notes": "YOUR_NATURAL_ENGLISH_NOTES_FOLDER_ID",
        "natural_physics_notes": "YOUR_NATURAL_PHYSICS_NOTES_FOLDER_ID",
        "natural_biology_notes": "YOUR_NATURAL_BIOLOGY_NOTES_FOLDER_ID",
        "natural_chemistry_notes": "YOUR_NATURAL_CHEMISTRY_NOTES_FOLDER_ID",
        "natural_aptitude_notes": "YOUR_NATURAL_APTITUDE_NOTES_FOLDER_ID",
        
        # Social Stream Short Notes
        "social_math_notes": "YOUR_SOCIAL_MATH_NOTES_FOLDER_ID",
        "social_english_notes": "YOUR_SOCIAL_ENGLISH_NOTES_FOLDER_ID",
        "social_geography_notes": "YOUR_SOCIAL_GEOGRAPHY_NOTES_FOLDER_ID",
        "social_history_notes": "YOUR_SOCIAL_HISTORY_NOTES_FOLDER_ID",
        "social_economics_notes": "YOUR_SOCIAL_ECONOMICS_NOTES_FOLDER_ID",
        "social_aptitude_notes": "YOUR_SOCIAL_APTITUDE_NOTES_FOLDER_ID",
        
        # =============================================================================
        # 🧮 CHEAT SHEETS (Premium Resources)
        # =============================================================================
        # Subject-specific cheat sheets for both streams
        
        # Natural Stream Cheat Sheets
        "natural_math_cheats": "YOUR_NATURAL_MATH_CHEATS_FOLDER_ID",
        "natural_english_cheats": "YOUR_NATURAL_ENGLISH_CHEATS_FOLDER_ID",
        "natural_physics_cheats": "YOUR_NATURAL_PHYSICS_CHEATS_FOLDER_ID",
        "natural_biology_cheats": "YOUR_NATURAL_BIOLOGY_CHEATS_FOLDER_ID",
        "natural_chemistry_cheats": "YOUR_NATURAL_CHEMISTRY_CHEATS_FOLDER_ID",
        "natural_aptitude_cheats": "YOUR_NATURAL_APTITUDE_CHEATS_FOLDER_ID",
        
        # Social Stream Cheat Sheets
        "social_math_cheats": "YOUR_SOCIAL_MATH_CHEATS_FOLDER_ID",
        "social_english_cheats": "YOUR_SOCIAL_ENGLISH_CHEATS_FOLDER_ID",
        "social_geography_cheats": "YOUR_SOCIAL_GEOGRAPHY_CHEATS_FOLDER_ID",
        "social_history_cheats": "YOUR_SOCIAL_HISTORY_CHEATS_FOLDER_ID",
        "social_economics_cheats": "YOUR_SOCIAL_ECONOMICS_CHEATS_FOLDER_ID",
        "social_aptitude_cheats": "YOUR_SOCIAL_APTITUDE_CHEATS_FOLDER_ID",
        
        # =============================================================================
        # 🧠 QUIZZES (Premium Resources)
        # =============================================================================
        # Grade and subject-specific quizzes for both streams
        
        # Natural Stream Quizzes - Mathematics
        "natural_math_grade9_quizzes": "YOUR_NATURAL_MATH_GRADE9_QUIZZES_FOLDER_ID",
        "natural_math_grade10_quizzes": "YOUR_NATURAL_MATH_GRADE10_QUIZZES_FOLDER_ID",
        "natural_math_grade11_quizzes": "YOUR_NATURAL_MATH_GRADE11_QUIZZES_FOLDER_ID",
        "natural_math_grade12_quizzes": "YOUR_NATURAL_MATH_GRADE12_QUIZZES_FOLDER_ID",
        "natural_math_mixed_quizzes": "YOUR_NATURAL_MATH_MIXED_QUIZZES_FOLDER_ID",
        
        # Natural Stream Quizzes - English
        "natural_english_grade9_quizzes": "YOUR_NATURAL_ENGLISH_GRADE9_QUIZZES_FOLDER_ID",
        "natural_english_grade10_quizzes": "YOUR_NATURAL_ENGLISH_GRADE10_QUIZZES_FOLDER_ID",
        "natural_english_grade11_quizzes": "YOUR_NATURAL_ENGLISH_GRADE11_QUIZZES_FOLDER_ID",
        "natural_english_grade12_quizzes": "YOUR_NATURAL_ENGLISH_GRADE12_QUIZZES_FOLDER_ID",
        "natural_english_mixed_quizzes": "YOUR_NATURAL_ENGLISH_MIXED_QUIZZES_FOLDER_ID",
        
        # Natural Stream Quizzes - Physics
        "natural_physics_grade9_quizzes": "YOUR_NATURAL_PHYSICS_GRADE9_QUIZZES_FOLDER_ID",
        "natural_physics_grade10_quizzes": "YOUR_NATURAL_PHYSICS_GRADE10_QUIZZES_FOLDER_ID",
        "natural_physics_grade11_quizzes": "YOUR_NATURAL_PHYSICS_GRADE11_QUIZZES_FOLDER_ID",
        "natural_physics_grade12_quizzes": "YOUR_NATURAL_PHYSICS_GRADE12_QUIZZES_FOLDER_ID",
        "natural_physics_mixed_quizzes": "YOUR_NATURAL_PHYSICS_MIXED_QUIZZES_FOLDER_ID",
        
        # Natural Stream Quizzes - Biology
        "natural_biology_grade9_quizzes": "YOUR_NATURAL_BIOLOGY_GRADE9_QUIZZES_FOLDER_ID",
        "natural_biology_grade10_quizzes": "YOUR_NATURAL_BIOLOGY_GRADE10_QUIZZES_FOLDER_ID",
        "natural_biology_grade11_quizzes": "YOUR_NATURAL_BIOLOGY_GRADE11_QUIZZES_FOLDER_ID",
        "natural_biology_grade12_quizzes": "YOUR_NATURAL_BIOLOGY_GRADE12_QUIZZES_FOLDER_ID",
        "natural_biology_mixed_quizzes": "YOUR_NATURAL_BIOLOGY_MIXED_QUIZZES_FOLDER_ID",
        
        # Natural Stream Quizzes - Chemistry
        "natural_chemistry_grade9_quizzes": "YOUR_NATURAL_CHEMISTRY_GRADE9_QUIZZES_FOLDER_ID",
        "natural_chemistry_grade10_quizzes": "YOUR_NATURAL_CHEMISTRY_GRADE10_QUIZZES_FOLDER_ID",
        "natural_chemistry_grade11_quizzes": "YOUR_NATURAL_CHEMISTRY_GRADE11_QUIZZES_FOLDER_ID",
        "natural_chemistry_grade12_quizzes": "YOUR_NATURAL_CHEMISTRY_GRADE12_QUIZZES_FOLDER_ID",
        "natural_chemistry_mixed_quizzes": "YOUR_NATURAL_CHEMISTRY_MIXED_QUIZZES_FOLDER_ID",
        
        # Natural Stream Quizzes - Aptitude
        "natural_aptitude_grade9_quizzes": "YOUR_NATURAL_APTITUDE_GRADE9_QUIZZES_FOLDER_ID",
        "natural_aptitude_grade10_quizzes": "YOUR_NATURAL_APTITUDE_GRADE10_QUIZZES_FOLDER_ID",
        "natural_aptitude_grade11_quizzes": "YOUR_NATURAL_APTITUDE_GRADE11_QUIZZES_FOLDER_ID",
        "natural_aptitude_grade12_quizzes": "YOUR_NATURAL_APTITUDE_GRADE12_QUIZZES_FOLDER_ID",
        "natural_aptitude_mixed_quizzes": "YOUR_NATURAL_APTITUDE_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - Mathematics
        "social_math_grade9_quizzes": "YOUR_SOCIAL_MATH_GRADE9_QUIZZES_FOLDER_ID",
        "social_math_grade10_quizzes": "YOUR_SOCIAL_MATH_GRADE10_QUIZZES_FOLDER_ID",
        "social_math_grade11_quizzes": "YOUR_SOCIAL_MATH_GRADE11_QUIZZES_FOLDER_ID",
        "social_math_grade12_quizzes": "YOUR_SOCIAL_MATH_GRADE12_QUIZZES_FOLDER_ID",
        "social_math_mixed_quizzes": "YOUR_SOCIAL_MATH_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - English
        "social_english_grade9_quizzes": "YOUR_SOCIAL_ENGLISH_GRADE9_QUIZZES_FOLDER_ID",
        "social_english_grade10_quizzes": "YOUR_SOCIAL_ENGLISH_GRADE10_QUIZZES_FOLDER_ID",
        "social_english_grade11_quizzes": "YOUR_SOCIAL_ENGLISH_GRADE11_QUIZZES_FOLDER_ID",
        "social_english_grade12_quizzes": "YOUR_SOCIAL_ENGLISH_GRADE12_QUIZZES_FOLDER_ID",
        "social_english_mixed_quizzes": "YOUR_SOCIAL_ENGLISH_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - Geography
        "social_geography_grade9_quizzes": "YOUR_SOCIAL_GEOGRAPHY_GRADE9_QUIZZES_FOLDER_ID",
        "social_geography_grade10_quizzes": "YOUR_SOCIAL_GEOGRAPHY_GRADE10_QUIZZES_FOLDER_ID",
        "social_geography_grade11_quizzes": "YOUR_SOCIAL_GEOGRAPHY_GRADE11_QUIZZES_FOLDER_ID",
        "social_geography_grade12_quizzes": "YOUR_SOCIAL_GEOGRAPHY_GRADE12_QUIZZES_FOLDER_ID",
        "social_geography_mixed_quizzes": "YOUR_SOCIAL_GEOGRAPHY_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - History
        "social_history_grade9_quizzes": "YOUR_SOCIAL_HISTORY_GRADE9_QUIZZES_FOLDER_ID",
        "social_history_grade10_quizzes": "YOUR_SOCIAL_HISTORY_GRADE10_QUIZZES_FOLDER_ID",
        "social_history_grade11_quizzes": "YOUR_SOCIAL_HISTORY_GRADE11_QUIZZES_FOLDER_ID",
        "social_history_grade12_quizzes": "YOUR_SOCIAL_HISTORY_GRADE12_QUIZZES_FOLDER_ID",
        "social_history_mixed_quizzes": "YOUR_SOCIAL_HISTORY_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - Economics
        "social_economics_grade9_quizzes": "YOUR_SOCIAL_ECONOMICS_GRADE9_QUIZZES_FOLDER_ID",
        "social_economics_grade10_quizzes": "YOUR_SOCIAL_ECONOMICS_GRADE10_QUIZZES_FOLDER_ID",
        "social_economics_grade11_quizzes": "YOUR_SOCIAL_ECONOMICS_GRADE11_QUIZZES_FOLDER_ID",
        "social_economics_grade12_quizzes": "YOUR_SOCIAL_ECONOMICS_GRADE12_QUIZZES_FOLDER_ID",
        "social_economics_mixed_quizzes": "YOUR_SOCIAL_ECONOMICS_MIXED_QUIZZES_FOLDER_ID",
        
        # Social Stream Quizzes - Aptitude
        "social_aptitude_grade9_quizzes": "YOUR_SOCIAL_APTITUDE_GRADE9_QUIZZES_FOLDER_ID",
        "social_aptitude_grade10_quizzes": "YOUR_SOCIAL_APTITUDE_GRADE10_QUIZZES_FOLDER_ID",
        "social_aptitude_grade11_quizzes": "YOUR_SOCIAL_APTITUDE_GRADE11_QUIZZES_FOLDER_ID",
        "social_aptitude_grade12_quizzes": "YOUR_SOCIAL_APTITUDE_GRADE12_QUIZZES_FOLDER_ID",
        "social_aptitude_mixed_quizzes": "YOUR_SOCIAL_APTITUDE_MIXED_QUIZZES_FOLDER_ID",
        
        # =============================================================================
        # 📝 PAST EXAMS (Mixed Free/Premium Resources)
        # =============================================================================
        # Year-specific past exams (2000-2017: Free, 2014-2017: Premium)
        
        # Natural Stream Past Exams (2000-2017)
        **{f"natural_{year}_exam": f"YOUR_NATURAL_{year}_EXAM_FOLDER_ID" for year in range(2000, 2018)},
        
        # Social Stream Past Exams (2000-2017)
        **{f"social_{year}_exam": f"YOUR_SOCIAL_{year}_EXAM_FOLDER_ID" for year in range(2000, 2018)},
        
        # =============================================================================
        # 📚 TOPIC-BASED PAST EXAMS (Future Feature)
        # =============================================================================
        # Subject-specific past exams organized by topics
        
        # Natural Stream Topic-Based Past Exams
        "natural_math_past_exams": "YOUR_NATURAL_MATH_PAST_EXAMS_FOLDER_ID",
        "natural_english_past_exams": "YOUR_NATURAL_ENGLISH_PAST_EXAMS_FOLDER_ID",
        "natural_physics_past_exams": "YOUR_NATURAL_PHYSICS_PAST_EXAMS_FOLDER_ID",
        "natural_biology_past_exams": "YOUR_NATURAL_BIOLOGY_PAST_EXAMS_FOLDER_ID",
        "natural_chemistry_past_exams": "YOUR_NATURAL_CHEMISTRY_PAST_EXAMS_FOLDER_ID",
        "natural_aptitude_past_exams": "YOUR_NATURAL_APTITUDE_PAST_EXAMS_FOLDER_ID",
        
        # Social Stream Topic-Based Past Exams
        "social_math_past_exams": "YOUR_SOCIAL_MATH_PAST_EXAMS_FOLDER_ID",
        "social_english_past_exams": "YOUR_SOCIAL_ENGLISH_PAST_EXAMS_FOLDER_ID",
        "social_geography_past_exams": "YOUR_SOCIAL_GEOGRAPHY_PAST_EXAMS_FOLDER_ID",
        "social_history_past_exams": "YOUR_SOCIAL_HISTORY_PAST_EXAMS_FOLDER_ID",
        "social_economics_past_exams": "YOUR_SOCIAL_ECONOMICS_PAST_EXAMS_FOLDER_ID",
        "social_aptitude_past_exams": "YOUR_SOCIAL_APTITUDE_PAST_EXAMS_FOLDER_ID",
        
        # =============================================================================
        # 💡 EXAM TIPS (Premium Resources)
        # =============================================================================
        # Stream-specific exam tips and strategies
        
        "natural_exam_tips": "YOUR_NATURAL_EXAM_TIPS_FOLDER_ID",
        "social_exam_tips": "YOUR_SOCIAL_EXAM_TIPS_FOLDER_ID",
        
        # =============================================================================
        # 📖 STUDY TIPS (Premium Resources)
        # =============================================================================
        # Stream-specific study tips and techniques
        
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
    ANOTHER_QUIZ = "🔁 Another Quiz"
    EXIT_QUIZZES = "⬅️ Exit Quizzes"
    TEXT_BOOKS = "📖 Text Books"
    SHORT_NOTES = "📝 Short Notes"
    SHARE_INVITE = "↗️ Share Invite"
    REQUEST_WITHDRAWAL = "💰 Request Withdrawal"
    BACK_TO_MAIN_MENU = "⬅️ Back to Main Menu"
    ORGANIZED_BY_YEAR = "📅 Organized by Year"
    ORGANIZED_BY_TOPICS = "📚 Organized by Topics"