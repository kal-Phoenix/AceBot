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

    # Google Drive Service Account Credentials Path (DEPRECATED - keeping for migration)
    GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH", "credentials.json")
    
    # Telegram Channel Configuration (NEW)
    CONTENT_CHANNEL_USERNAME = os.getenv("CONTENT_CHANNEL_USERNAME", "@acebot_content")
    CONTENT_CHANNEL_ID = os.getenv("CONTENT_CHANNEL_ID", "-1001234567890")
    if CONTENT_CHANNEL_ID == "-1001234567890":
        print("WARNING: CONTENT_CHANNEL_ID is not set in environment variables or .env file. Please set it.")

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
    # 📁 FILE IDS CONFIGURATION (TELEGRAM CHANNEL SYSTEM)
    # =============================================================================
    # This section contains all file IDs for different resources stored in your private Telegram channel.
    # Replace placeholder file_ids with actual file_ids from your extractor bot.
    # 
    # 📋 FILE STRUCTURE:
    #   - {stream}_{resource_type}_{grade}     (for grade-specific resources)
    #   - {stream}_{resource_type}_{subject}   (for subject-specific resources)
    #   - {stream}_pastexam_{year}             (for year-specific past exams)
    # 
    # 🎯 STREAMS: natural, social
    # 📚 RESOURCES: textbook, guide, notes, cheats, quiz, pastexam, examtips, studytips
    # 📖 SUBJECTS: math, english, physics, biology, chemistry, aptitude, geography, history, economics
    # 🎓 GRADES: grade9, grade10, grade11, grade12, mixed
    # 📅 YEARS: 2000-2017 (for past exams)
    # =============================================================================
    
    FILE_IDS = {
        # =============================================================================
        # 📚 TEXTBOOKS (Free Resources)
        # =============================================================================
        # Grade-specific textbooks for both Natural and Social streams
        
        # Natural Stream Textbooks - Old Curriculum
        "natural_textbook_grade9_old": [
            {"file_id": "YOUR_NATURAL_GRADE9_OLD_MATH_TEXTBOOK_FILE_ID", "name": "Grade 9 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "YOUR_NATURAL_GRADE9_OLD_PHYSICS_TEXTBOOK_FILE_ID", "name": "Grade 9 Physics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "YOUR_NATURAL_GRADE9_OLD_CHEMISTRY_TEXTBOOK_FILE_ID", "name": "Grade 9 Chemistry Textbook (Old Curriculum)", "type": "document"},
        ],
        # Natural Stream Textbooks - New Curriculum
        "natural_textbook_grade9_new": [
            {"file_id": "YOUR_NATURAL_GRADE9_NEW_MATH_TEXTBOOK_FILE_ID", "name": "Grade 9 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "YOUR_NATURAL_GRADE9_NEW_PHYSICS_TEXTBOOK_FILE_ID", "name": "Grade 9 Physics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "YOUR_NATURAL_GRADE9_NEW_CHEMISTRY_TEXTBOOK_FILE_ID", "name": "Grade 9 Chemistry Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade10_old": [
            {"file_id": "YOUR_NATURAL_GRADE10_OLD_TEXTBOOK_FILE_ID", "name": "Grade 10 Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade10_new": [
            {"file_id": "YOUR_NATURAL_GRADE10_NEW_TEXTBOOK_FILE_ID", "name": "Grade 10 Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade11_old": [
            {"file_id": "YOUR_NATURAL_GRADE11_OLD_TEXTBOOK_FILE_ID", "name": "Grade 11 Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade11_new": [
            {"file_id": "YOUR_NATURAL_GRADE11_NEW_TEXTBOOK_FILE_ID", "name": "Grade 11 Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade12_old": [
            {"file_id": "YOUR_NATURAL_GRADE12_OLD_TEXTBOOK_FILE_ID", "name": "Grade 12 Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade12_new": [
            {"file_id": "YOUR_NATURAL_GRADE12_NEW_TEXTBOOK_FILE_ID", "name": "Grade 12 Textbook (New Curriculum)", "type": "document"},
        ],
        
        # Social Stream Textbooks
        "social_textbook_grade9_old": [
            {"file_id": "YOUR_SOCIAL_GRADE9_OLD_TEXTBOOK_FILE_ID", "name": "Grade 9 Social Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade9_new": [
            {"file_id": "YOUR_SOCIAL_GRADE9_NEW_TEXTBOOK_FILE_ID", "name": "Grade 9 Social Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade10_old": [
            {"file_id": "YOUR_SOCIAL_GRADE10_OLD_TEXTBOOK_FILE_ID", "name": "Grade 10 Social Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade10_new": [
            {"file_id": "YOUR_SOCIAL_GRADE10_NEW_TEXTBOOK_FILE_ID", "name": "Grade 10 Social Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade11_old": [
            {"file_id": "YOUR_SOCIAL_GRADE11_OLD_TEXTBOOK_FILE_ID", "name": "Grade 11 Social Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade11_new": [
            {"file_id": "YOUR_SOCIAL_GRADE11_NEW_TEXTBOOK_FILE_ID", "name": "Grade 11 Social Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade12_old": [
            {"file_id": "YOUR_SOCIAL_GRADE12_OLD_TEXTBOOK_FILE_ID", "name": "Grade 12 Social Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade12_new": [
            {"file_id": "YOUR_SOCIAL_GRADE12_NEW_TEXTBOOK_FILE_ID", "name": "Grade 12 Social Textbook (New Curriculum)", "type": "document"},
        ],
        
        # =============================================================================
        # 📖 TEACHER'S GUIDES (Free Resources)
        # =============================================================================
        # Grade-specific teacher's guides for both streams
        
        # Natural Stream Teacher's Guides - Old Curriculum
        "natural_guide_grade9_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMFaMp1X9SfsUFwm_Yop3yKMgy2vIIAAiMIAAKgrcFQeu9asiE7RDM2BA", "name": "Chemistry Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgEAAyEFAASkzI5MAAMGaMp1XwlR14LIzFWbnB3NGVqJijgAAqQAA6SrKERG7RIwx57ECTYE", "name": "Geography Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgEAAyEFAASkzI5MAAMHaMp1X-m_9cGkZtbiVYwhkl3EcU0AAqkAA6SrKETAaLlVIVydhTYE", "name": "Mathematics Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgEAAyEFAASkzI5MAAMIaMp1X4RB6AG5721YixRdp1UvCLgAAqUAA6SrKESWPh1KJiwwajYE", "name": "Biology Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMJaMp1X-CVzD49AAGOg--qu2uicy4jAAIlCAACoK3BUCi7ICgozV73NgQ", "name": "Civic & Ethical Education Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMLaMp1X0Ke9w1T7zOQNRygbs8fSScAAtEJAAI0iohRiEaQi-xMsEw2BA", "name": "English Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
        ],
        # Natural Stream Teacher's Guides - New Curriculum
        "natural_guide_grade9_new": [
            {"file_id": "YOUR_NATURAL_GRADE9_NEW_GUIDE_FILE_ID", "name": "Grade 9 Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade10_old": [
            {"file_id": "YOUR_NATURAL_GRADE10_OLD_GUIDE_FILE_ID", "name": "Grade 10 Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade10_new": [
            {"file_id": "YOUR_NATURAL_GRADE10_NEW_GUIDE_FILE_ID", "name": "Grade 10 Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade11_old": [
            {"file_id": "YOUR_NATURAL_GRADE11_OLD_GUIDE_FILE_ID", "name": "Grade 11 Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade11_new": [
            {"file_id": "YOUR_NATURAL_GRADE11_NEW_GUIDE_FILE_ID", "name": "Grade 11 Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade12_old": [
            {"file_id": "YOUR_NATURAL_GRADE12_OLD_GUIDE_FILE_ID", "name": "Grade 12 Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade12_new": [
            {"file_id": "YOUR_NATURAL_GRADE12_NEW_GUIDE_FILE_ID", "name": "Grade 12 Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        
        # Social Stream Teacher's Guides
        "social_guide_grade9_old": [
            {"file_id": "YOUR_SOCIAL_GRADE9_OLD_GUIDE_FILE_ID", "name": "Grade 9 Social Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade9_new": [
            {"file_id": "YOUR_SOCIAL_GRADE9_NEW_GUIDE_FILE_ID", "name": "Grade 9 Social Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade10_old": [
            {"file_id": "YOUR_SOCIAL_GRADE10_OLD_GUIDE_FILE_ID", "name": "Grade 10 Social Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade10_new": [
            {"file_id": "YOUR_SOCIAL_GRADE10_NEW_GUIDE_FILE_ID", "name": "Grade 10 Social Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade11_old": [
            {"file_id": "YOUR_SOCIAL_GRADE11_OLD_GUIDE_FILE_ID", "name": "Grade 11 Social Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade11_new": [
            {"file_id": "YOUR_SOCIAL_GRADE11_NEW_GUIDE_FILE_ID", "name": "Grade 11 Social Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade12_old": [
            {"file_id": "YOUR_SOCIAL_GRADE12_OLD_GUIDE_FILE_ID", "name": "Grade 12 Social Teacher's Guide (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade12_new": [
            {"file_id": "YOUR_SOCIAL_GRADE12_NEW_GUIDE_FILE_ID", "name": "Grade 12 Social Teacher's Guide (New Curriculum)", "type": "document"},
        ],
        
        # =============================================================================
        # 📝 SHORT NOTES (Premium Resources)
        # =============================================================================
        # Subject-specific short notes for both streams
        
        # Natural Stream Short Notes
        "natural_notes_math": [
            {"file_id": "YOUR_NATURAL_MATH_NOTES_FILE_ID", "name": "Mathematics Short Notes", "type": "document"},
        ],
        "natural_notes_english": [
            {"file_id": "YOUR_NATURAL_ENGLISH_NOTES_FILE_ID", "name": "English Short Notes", "type": "document"},
        ],
        "natural_notes_physics": [
            {"file_id": "YOUR_NATURAL_PHYSICS_NOTES_FILE_ID", "name": "Physics Short Notes", "type": "document"},
        ],
        "natural_notes_biology": [
            {"file_id": "YOUR_NATURAL_BIOLOGY_NOTES_FILE_ID", "name": "Biology Short Notes", "type": "document"},
        ],
        "natural_notes_chemistry": [
            {"file_id": "YOUR_NATURAL_CHEMISTRY_NOTES_FILE_ID", "name": "Chemistry Short Notes", "type": "document"},
        ],
        "natural_notes_aptitude": [
            {"file_id": "YOUR_NATURAL_APTITUDE_NOTES_FILE_ID", "name": "Aptitude Short Notes", "type": "document"},
        ],
        
        # Social Stream Short Notes
        "social_notes_math": [
            {"file_id": "YOUR_SOCIAL_MATH_NOTES_FILE_ID", "name": "Mathematics Short Notes", "type": "document"},
        ],
        "social_notes_english": [
            {"file_id": "YOUR_SOCIAL_ENGLISH_NOTES_FILE_ID", "name": "English Short Notes", "type": "document"},
        ],
        "social_notes_geography": [
            {"file_id": "YOUR_SOCIAL_GEOGRAPHY_NOTES_FILE_ID", "name": "Geography Short Notes", "type": "document"},
        ],
        "social_notes_history": [
            {"file_id": "YOUR_SOCIAL_HISTORY_NOTES_FILE_ID", "name": "History Short Notes", "type": "document"},
        ],
        "social_notes_economics": [
            {"file_id": "YOUR_SOCIAL_ECONOMICS_NOTES_FILE_ID", "name": "Economics Short Notes", "type": "document"},
        ],
        "social_notes_aptitude": [
            {"file_id": "YOUR_SOCIAL_APTITUDE_NOTES_FILE_ID", "name": "Aptitude Short Notes", "type": "document"},
        ],
        
        # =============================================================================
        # 🧮 CHEAT SHEETS (Premium Resources)
        # =============================================================================
        # Subject-specific cheat sheets for both streams
        
        # Natural Stream Cheat Sheets
        "natural_cheats_math": [
            {"file_id": "YOUR_NATURAL_MATH_CHEATS_FILE_ID", "name": "Math Formulas Cheat Sheet", "type": "document"},
        ],
        "natural_cheats_english": [
            {"file_id": "YOUR_NATURAL_ENGLISH_CHEATS_FILE_ID", "name": "English Tips Cheat Sheet", "type": "document"},
        ],
        "natural_cheats_physics": [
            {"file_id": "YOUR_NATURAL_PHYSICS_CHEATS_FILE_ID", "name": "Physics Formulas Cheat Sheet", "type": "document"},
        ],
        "natural_cheats_biology": [
            {"file_id": "YOUR_NATURAL_BIOLOGY_CHEATS_FILE_ID", "name": "Biology Cheats", "type": "document"},
        ],
        "natural_cheats_chemistry": [
            {"file_id": "YOUR_NATURAL_CHEMISTRY_CHEATS_FILE_ID", "name": "Chemistry Cheats", "type": "document"},
        ],
        "natural_cheats_aptitude": [
            {"file_id": "YOUR_NATURAL_APTITUDE_CHEATS_FILE_ID", "name": "Aptitude Tricks", "type": "document"},
        ],
        
        # Social Stream Cheat Sheets
        "social_cheats_math": [
            {"file_id": "YOUR_SOCIAL_MATH_CHEATS_FILE_ID", "name": "Math Formulas Cheat Sheet", "type": "document"},
        ],
        "social_cheats_english": [
            {"file_id": "YOUR_SOCIAL_ENGLISH_CHEATS_FILE_ID", "name": "English Tips Cheat Sheet", "type": "document"},
        ],
        "social_cheats_geography": [
            {"file_id": "YOUR_SOCIAL_GEOGRAPHY_CHEATS_FILE_ID", "name": "Geography Cheats", "type": "document"},
        ],
        "social_cheats_history": [
            {"file_id": "YOUR_SOCIAL_HISTORY_CHEATS_FILE_ID", "name": "History Cheats", "type": "document"},
        ],
        "social_cheats_economics": [
            {"file_id": "YOUR_SOCIAL_ECONOMICS_CHEATS_FILE_ID", "name": "Economics Cheats", "type": "document"},
        ],
        "social_cheats_aptitude": [
            {"file_id": "YOUR_SOCIAL_APTITUDE_CHEATS_FILE_ID", "name": "Aptitude Tricks", "type": "document"},
        ],
        
        # =============================================================================
        # 🧠 QUIZZES (Premium Resources)
        # =============================================================================
        # Grade and subject-specific quizzes for both streams
        
        # Natural Stream Quizzes
        "natural_quiz_math_grade9": [
            {"file_id": "YOUR_NATURAL_MATH_GRADE9_QUIZ_FILE_ID", "name": "Math Quiz Grade 9", "type": "document"},
        ],
        "natural_quiz_math_grade10": [
            {"file_id": "YOUR_NATURAL_MATH_GRADE10_QUIZ_FILE_ID", "name": "Math Quiz Grade 10", "type": "document"},
        ],
        "natural_quiz_math_mixed": [
            {"file_id": "YOUR_NATURAL_MATH_MIXED_QUIZ_FILE_ID", "name": "Math Quiz Mixed", "type": "document"},
        ],
        "natural_quiz_physics_grade9": [
            {"file_id": "YOUR_NATURAL_PHYSICS_GRADE9_QUIZ_FILE_ID", "name": "Physics Quiz Grade 9", "type": "document"},
        ],
        "natural_quiz_chemistry_grade9": [
            {"file_id": "YOUR_NATURAL_CHEMISTRY_GRADE9_QUIZ_FILE_ID", "name": "Chemistry Quiz Grade 9", "type": "document"},
        ],
        
        # Social Stream Quizzes
        "social_quiz_math_grade9": [
            {"file_id": "YOUR_SOCIAL_MATH_GRADE9_QUIZ_FILE_ID", "name": "Math Quiz Grade 9", "type": "document"},
        ],
        "social_quiz_geography_grade9": [
            {"file_id": "YOUR_SOCIAL_GEOGRAPHY_GRADE9_QUIZ_FILE_ID", "name": "Geography Quiz Grade 9", "type": "document"},
        ],
        "social_quiz_history_grade9": [
            {"file_id": "YOUR_SOCIAL_HISTORY_GRADE9_QUIZ_FILE_ID", "name": "History Quiz Grade 9", "type": "document"},
        ],
        
        # =============================================================================
        # 📝 PAST EXAMS (Mixed Free/Premium Resources)
        # =============================================================================
        # Year-specific past exams (2000-2013: Free, 2014-2017: Premium)
        
        # Natural Stream Past Exams (2000-2017)
        "natural_pastexam_2000": [
            {"file_id": "YOUR_NATURAL_2000_EXAM_FILE_ID", "name": "Natural Science Exam 2000", "type": "document"},
        ],
        "natural_pastexam_2001": [
            {"file_id": "YOUR_NATURAL_2001_EXAM_FILE_ID", "name": "Natural Science Exam 2001", "type": "document"},
        ],
        "natural_pastexam_2002": [
            {"file_id": "YOUR_NATURAL_2002_EXAM_FILE_ID", "name": "Natural Science Exam 2002", "type": "document"},
        ],
        "natural_pastexam_2003": [
            {"file_id": "YOUR_NATURAL_2003_EXAM_FILE_ID", "name": "Natural Science Exam 2003", "type": "document"},
        ],
        "natural_pastexam_2004": [
            {"file_id": "YOUR_NATURAL_2004_EXAM_FILE_ID", "name": "Natural Science Exam 2004", "type": "document"},
        ],
        "natural_pastexam_2005": [
            {"file_id": "YOUR_NATURAL_2005_EXAM_FILE_ID", "name": "Natural Science Exam 2005", "type": "document"},
        ],
        "natural_pastexam_2006": [
            {"file_id": "YOUR_NATURAL_2006_EXAM_FILE_ID", "name": "Natural Science Exam 2006", "type": "document"},
        ],
        "natural_pastexam_2007": [
            {"file_id": "YOUR_NATURAL_2007_EXAM_FILE_ID", "name": "Natural Science Exam 2007", "type": "document"},
        ],
        "natural_pastexam_2008": [
            {"file_id": "YOUR_NATURAL_2008_EXAM_FILE_ID", "name": "Natural Science Exam 2008", "type": "document"},
        ],
        "natural_pastexam_2009": [
            {"file_id": "YOUR_NATURAL_2009_EXAM_FILE_ID", "name": "Natural Science Exam 2009", "type": "document"},
        ],
        "natural_pastexam_2010": [
            {"file_id": "YOUR_NATURAL_2010_EXAM_FILE_ID", "name": "Natural Science Exam 2010", "type": "document"},
        ],
        "natural_pastexam_2011": [
            {"file_id": "YOUR_NATURAL_2011_EXAM_FILE_ID", "name": "Natural Science Exam 2011", "type": "document"},
        ],
        "natural_pastexam_2012": [
            {"file_id": "YOUR_NATURAL_2012_EXAM_FILE_ID", "name": "Natural Science Exam 2012", "type": "document"},
        ],
        "natural_pastexam_2013": [
            {"file_id": "YOUR_NATURAL_2013_EXAM_FILE_ID", "name": "Natural Science Exam 2013", "type": "document"},
        ],
        "natural_pastexam_2014": [  # Premium
            {"file_id": "YOUR_NATURAL_2014_EXAM_FILE_ID", "name": "Natural Science Exam 2014", "type": "document"},
        ],
        "natural_pastexam_2015": [  # Premium
            {"file_id": "YOUR_NATURAL_2015_EXAM_FILE_ID", "name": "Natural Science Exam 2015", "type": "document"},
        ],
        "natural_pastexam_2016": [  # Premium
            {"file_id": "YOUR_NATURAL_2016_EXAM_FILE_ID", "name": "Natural Science Exam 2016", "type": "document"},
        ],
        "natural_pastexam_2017": [  # Premium
            {"file_id": "YOUR_NATURAL_2017_EXAM_FILE_ID", "name": "Natural Science Exam 2017", "type": "document"},
        ],
        
        # Social Stream Past Exams (2000-2017)
        "social_pastexam_2000": [
            {"file_id": "BQACAgQAAxkBAAIC6WjKZsGOxyJuZ0P-NEUqkaX0Wae-AAKxGQAC4bZQUvsBXtwNzQABVjYE", "name": "2000 Economics Exam", "type": "document"},
        ],
        "social_pastexam_2001": [
            {"file_id": "YOUR_SOCIAL_2001_EXAM_FILE_ID", "name": "Social Science Exam 2001", "type": "document"},
        ],
        "social_pastexam_2002": [
            {"file_id": "YOUR_SOCIAL_2002_EXAM_FILE_ID", "name": "Social Science Exam 2002", "type": "document"},
        ],
        "social_pastexam_2003": [
            {"file_id": "YOUR_SOCIAL_2003_EXAM_FILE_ID", "name": "Social Science Exam 2003", "type": "document"},
        ],
        "social_pastexam_2004": [
            {"file_id": "YOUR_SOCIAL_2004_EXAM_FILE_ID", "name": "Social Science Exam 2004", "type": "document"},
        ],
        "social_pastexam_2005": [
            {"file_id": "YOUR_SOCIAL_2005_EXAM_FILE_ID", "name": "Social Science Exam 2005", "type": "document"},
        ],
        "social_pastexam_2006": [
            {"file_id": "YOUR_SOCIAL_2006_EXAM_FILE_ID", "name": "Social Science Exam 2006", "type": "document"},
        ],
        "social_pastexam_2007": [
            {"file_id": "YOUR_SOCIAL_2007_EXAM_FILE_ID", "name": "Social Science Exam 2007", "type": "document"},
        ],
        "social_pastexam_2008": [
            {"file_id": "YOUR_SOCIAL_2008_EXAM_FILE_ID", "name": "Social Science Exam 2008", "type": "document"},
        ],
        "social_pastexam_2009": [
            {"file_id": "YOUR_SOCIAL_2009_EXAM_FILE_ID", "name": "Social Science Exam 2009", "type": "document"},
        ],
        "social_pastexam_2010": [
            {"file_id": "YOUR_SOCIAL_2010_EXAM_FILE_ID", "name": "Social Science Exam 2010", "type": "document"},
        ],
        "social_pastexam_2011": [
            {"file_id": "YOUR_SOCIAL_2011_EXAM_FILE_ID", "name": "Social Science Exam 2011", "type": "document"},
        ],
        "social_pastexam_2012": [
            {"file_id": "YOUR_SOCIAL_2012_EXAM_FILE_ID", "name": "Social Science Exam 2012", "type": "document"},
        ],
        "social_pastexam_2013": [
            {"file_id": "YOUR_SOCIAL_2013_EXAM_FILE_ID", "name": "Social Science Exam 2013", "type": "document"},
        ],
        "social_pastexam_2014": [  # Premium
            {"file_id": "YOUR_SOCIAL_2014_EXAM_FILE_ID", "name": "Social Science Exam 2014", "type": "document"},
        ],
        "social_pastexam_2015": [  # Premium
            {"file_id": "YOUR_SOCIAL_2015_EXAM_FILE_ID", "name": "Social Science Exam 2015", "type": "document"},
        ],
        "social_pastexam_2016": [  # Premium
            {"file_id": "YOUR_SOCIAL_2016_EXAM_FILE_ID", "name": "Social Science Exam 2016", "type": "document"},
        ],
        "social_pastexam_2017": [  # Premium
            {"file_id": "YOUR_SOCIAL_2017_EXAM_FILE_ID", "name": "Social Science Exam 2017", "type": "document"},
        ],
        
        # =============================================================================
        # 💡 EXAM TIPS (Premium Resources)
        # =============================================================================
        # Stream-specific exam tips and strategies
        
        "natural_examtips": [
            {"file_id": "YOUR_NATURAL_EXAM_TIPS_FILE_ID", "name": "Natural Science Exam Tips", "type": "document"},
        ],
        "social_examtips": [
            {"file_id": "YOUR_SOCIAL_EXAM_TIPS_FILE_ID", "name": "Social Science Exam Tips", "type": "document"},
        ],
        
        # =============================================================================
        # 📖 STUDY TIPS (Premium Resources)
        # =============================================================================
        # Stream-specific study tips and techniques
        
        "natural_studytips": [
            {"file_id": "YOUR_NATURAL_STUDY_TIPS_FILE_ID", "name": "Natural Science Study Tips", "type": "document"},
        ],
        "social_studytips": [
            {"file_id": "YOUR_SOCIAL_STUDY_TIPS_FILE_ID", "name": "Social Science Study Tips", "type": "document"},
        ],
        
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