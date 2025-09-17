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
    # 📖 SUBJECTS: 
    #     SOCIAL: amharic, english, civics, geography, history, mathematics, economics, general_business
    #     NATURAL: amharic, english, civics, mathematics, physics, chemistry, biology, agriculture, it
    # 🎓 GRADES: grade9, grade10, grade11, grade12, mixed
    # 📅 YEARS: 2000-2017 (for past exams)
    # 📝 FILE NAMING: G9=Grade9, STB=Textbook, TGG=Teacher's Guide, OLD=Old Curriculum, NEW=New Curriculum
    # =============================================================================
    
    FILE_IDS = {
        # =============================================================================
        # 📚 TEXTBOOKS (Free Resources)
        # =============================================================================
        # Grade-specific textbooks for both Natural and Social streams
        
        # Natural Stream Textbooks - Old Curriculum
        "natural_textbook_grade9_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMxaMq6FPhMHdlGN2_B3NDTKz1JjEgAAlcZAALhtlhSPzyJU_cXm8c2BA", "name": "Grade 9 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM1aMq6FFGfTRI1VMeWEtRvX59huWsAAlsZAALhtlhSJeV865K1L-k2BA", "name": "Grade 9 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM0aMq6FJEejA-E5i2YuzK6qux0dmYAAloZAALhtlhSTTwjNOxl12c2BA", "name": "Grade 9 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM5aMq6FPCGnSNaQYoJMhG44D0TX3QAAmMZAALhtlhSJHC7v7oiRFM2BA", "name": "Grade 9 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM6aMq6FCDSrhw5uW_rkk5Wnitm7uAAAmQZAALhtlhSUgoSjm2D1YU2BA", "name": "Grade 9 Physics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMzaMq6FCp3SQn8blYGIAUO19_KFNYAAlkZAALhtlhSEb3cCJdJzRE2BA", "name": "Grade 9 Chemistry Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMyaMq6FPEWMb-8GJmz37-h5UwEZysAAlgZAALhtlhSmaa2COiJZFA2BA", "name": "Grade 9 Biology Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM4aMq6FGxunZXdfp7UTamIyghT48gAAl4ZAALhtlhSC2vaLYN5nfg2BA", "name": "Grade 9 IT Textbook (Old Curriculum)", "type": "document"},
        ],
        # Natural Stream Textbooks - New Curriculum
        "natural_textbook_grade9_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANhaMrI3EamtdGzkgeJ8BrZq0sFy00AAsIZAALhtlhSZ2Ff6whdrKw2BA", "name": "Grade 9 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANfaMrI3H5DCTIxYDdDl4cDms_Pe00AArwZAALhtlhS8ppSjDK-qEQ2BA", "name": "Grade 9 Citizenship Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANmaMrI3Dv6ZlpbLBr0Ctj3N819MlEAAsgZAALhtlhS2lAbRwdrz9A2BA", "name": "Grade 9 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANeaMrI3HKrraSpW3AvEzeiCg9mav4AArkZAALhtlhSI-41gt-VUJY2BA", "name": "Grade 9 Chemistry Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANdaMrI3PjSwtMCws9U8PpLhQVJeqoAArgZAALhtlhS8PMAAY_pJJaJNgQ", "name": "Grade 9 Biology Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANlaMrI3CDZHWO6hJV9KHBbd_7CbQ4AAsYZAALhtlhSN24ylcr29KI2BA", "name": "Grade 9 IT Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANkaMrI3HIm2ItYvSBrTiXZhBJrZywAAsUZAALhtlhSXURUO-z_3QY2BA", "name": "Grade 9 HPE Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade10_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM9aMq7rsCQ1AOjybW3lIoSxKpybYgAAmcZAALhtlhS-_g_YssiUNo2BA", "name": "Grade 10 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANBaMq7rmgxYAhEeC4knI0TOkWmP6AAAmwZAALhtlhSkFRrbWyvQf42BA", "name": "Grade 10 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANAaMq7roQOiZFIz-Fn2nRawFt9pxYAAmsZAALhtlhSPCEaKcuN1Uw2BA", "name": "Grade 10 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANFaMq7ru7ZfUyagxkTLS_GUQ8RtCsAAnwZAALhtlhSpwmT8GuaNIU2BA", "name": "Grade 10 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANGaMq7rjjR_z_HSB5AM-Rl4TPXjL8AAn4ZAALhtlhSgEYLYd37jus2BA", "name": "Grade 10 Physics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM_aMq7rpBKnhdvkdjmsB5bvBbN4roAAmoZAALhtlhSj-TxiR1SBZ82BA", "name": "Grade 10 Chemistry Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM-aMq7rvCfo4nIvv7nTrbS75gl7I4AAmgZAALhtlhSmNA7f2Vg7kM2BA", "name": "Grade 10 Biology Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANEaMq7rnSJYM_6WLn_647tC1nnVwQAAnkZAALhtlhSuZqDgUhfwgE2BA", "name": "Grade 10 IT Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade10_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANpaMrJaptfb6PtXaDtSmjjEJ9rHDMAAswZAALhtlhSWSZK5GMIpT82BA", "name": "Grade 10 Citizenship Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANvaMrJaljt9-9LTFz3uJAvW5GQFvQAAtUZAALhtlhSldmkxsKRxoQ2BA", "name": "Grade 10 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANwaMrJatKTrAhqG8vCrJm4j-oWc0sAAtYZAALhtlhSvyR_gn_vdRw2BA", "name": "Grade 10 Physics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANoaMrJai0KNBBw6UE3VpbYwAru46UAAsoZAALhtlhSOBY3NgyPbiY2BA", "name": "Grade 10 Chemistry Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANnaMrJasxZmAhyRU1ywMxQYUyCez0AAskZAALhtlhSOdeTDqh7nb02BA", "name": "Grade 10 Biology Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANuaMrJaguVKjtOHeKx4dzwIneh97IAAtIZAALhtlhSRydB8Bc6cLg2BA", "name": "Grade 10 IT Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANtaMrJaobAC972S5a39oaDhOVFN5QAAtEZAALhtlhSCz1NXr-LXoE2BA", "name": "Grade 10 HPE Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade11_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANHaMq-t7rwRD88_AuXbPyr1Kdb4acAAn8ZAALhtlhSAwZVti7ddh02BA", "name": "Grade 11 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANMaMq-txnb-NK_Ft5Jg2zmBbkpjUEAAosZAALhtlhSCDLxWiYC1Fc2BA", "name": "Grade 11 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANKaMq-tzLfFzn76CrHVgNhaEhA-3gAAoUZAALhtlhSIHeBRt0mino2BA", "name": "Grade 11 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANQaMq-t9-Ggt-sX193hLOOMttRPPkAApMZAALhtlhSpjadicWaxoU2BA", "name": "Grade 11 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANRaMq_L_YUmH95M_rNMIRTnH6gRcIAApkZAALhtlhSr_5j9D13Rno2BA", "name": "Grade 11 Physics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANJaMq-t0aHrdrmp3sYCmkmlgTIGlgAAoQZAALhtlhS6cyBWkngBRQ2BA", "name": "Grade 11 Chemistry Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANIaMq-t1bld1P4QKT7zoeq3jI4TYkAAoMZAALhtlhSF2adOOtoIYU2BA", "name": "Grade 11 Biology Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade11_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN1aMrLawoWvO0yYOg7bcZOMiE-mgEAAvQZAALhtlhSNgIxFbdJQK02BA", "name": "Grade 11 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN5aMrLa7uDwcV4o3G5MpC90WAE9VMAAgwaAALhtlhSN7vMYKAopeE2BA", "name": "Grade 11 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN6aMrLa3h8-XAhDR5AvpMpMoZEoewAAg8aAALhtlhSXMuhuPO9H7w2BA", "name": "Grade 11 Physics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANzaMrLa4FIMASwS-f3g5GEiGjIAk8AAuEZAALhtlhSxFwodutOEsU2BA", "name": "Grade 11 Chemistry Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANyaMrLa0tFkWCDE0PFYikaHOCfxFoAAt4ZAALhtlhSpWwJax104Bo2BA", "name": "Grade 11 Biology Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANxaMrLa1x0Ti2tEFOuXrEOqUII-q8AAtoZAALhtlhS19q1ShuI_kQ2BA", "name": "Grade 11 Agriculture Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN4aMrLa0wTDOuvJsOjoJtRb-rORPAAAvkZAALhtlhSIEq5OaQ7Edk2BA", "name": "Grade 11 IT Textbook (New Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade12_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANSaMrCniYuxIjRvZDH_MAPYvV27-wAApoZAALhtlhS0_Usx2bavkA2BA", "name": "Grade 12 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANWaMrCni6RkhL8wAuLApGWaM95jXkAAqAZAALhtlhSzlAuTdE69LY2BA", "name": "Grade 12 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANaaMrCnj69M06gyPHmFkZALR1-EZEAAqcZAALhtlhS-PWFfhUTbhY2BA", "name": "Grade 12 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANbaMrCnvpV02P8iPjD0zY7MCK3GhMAAqsZAALhtlhS9FBMt0x8RdY2BA", "name": "Grade 12 Physics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANUaMrCnnlQ_lCGAWO6t_kGgONik5wAApwZAALhtlhSgdinuZd4haE2BA", "name": "Grade 12 Chemistry Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANTaMrCnmOG0hS4yGKccvAWBCMKgQMAApsZAALhtlhS59bwx0v-FsY2BA", "name": "Grade 12 Biology Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANZaMrCnoq2EdULFtUxnebCwe5JWQoAAqMZAALhtlhSAS6I_-E8yUo2BA", "name": "Grade 12 IT Textbook (Old Curriculum)", "type": "document"},
        ],
        "natural_textbook_grade12_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOAaMrNZtHvCkMCj5H7wNVdDK0aORIAAjUaAALhtlhSCxFgWqCb9ZY2BA", "name": "Grade 12 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOEaMrNZrTTNXtqiWlg0b3dSkKTcUcAAj4aAALhtlhSBP-qri2kVz82BA", "name": "Grade 12 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOFaMrNZnbe6P08VkgllQYvQ0ONyn4AAj8aAALhtlhSIfujbvX1E4I2BA", "name": "Grade 12 Physics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN-aMrNZp_hEQnaaIMjOiWo-u-iHLkAAjIaAALhtlhSsrPe8MhJQgk2BA", "name": "Grade 12 Chemistry Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN9aMrNZuTXnCR9mRltSBo2ZrzhCicAAi8aAALhtlhSESfy3asHwSQ2BA", "name": "Grade 12 Biology Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAODaMrNZoAxThQmNE2q2ktZ2Sym26wAAjoaAALhtlhS4GdUmuymh3Y2BA", "name": "Grade 12 IT Textbook (New Curriculum)", "type": "document"},
        ],
        
        # Social Stream Textbooks
        "social_textbook_grade9_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAMxaMq6FPhMHdlGN2_B3NDTKz1JjEgAAlcZAALhtlhSPzyJU_cXm8c2BA", "name": "Grade 9 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM1aMq6FFGfTRI1VMeWEtRvX59huWsAAlsZAALhtlhSJeV865K1L-k2BA", "name": "Grade 9 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM0aMq6FJEejA-E5i2YuzK6qux0dmYAAloZAALhtlhSTTwjNOxl12c2BA", "name": "Grade 9 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM2aMq6FCqj4R2UeQjPiov3PkzA8XMAAlwZAALhtlhSPuvBZWIGd742BA", "name": "Grade 9 Geography Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM3aMq6FDF01cYDHQUjZhGe6nUnY1wAAl0ZAALhtlhS7Gu5tVKFS2s2BA", "name": "Grade 9 History Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM5aMq6FPCGnSNaQYoJMhG44D0TX3QAAmMZAALhtlhSJHC7v7oiRFM2BA", "name": "Grade 9 Mathematics Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade9_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANhaMrI3EamtdGzkgeJ8BrZq0sFy00AAsIZAALhtlhSZ2Ff6whdrKw2BA", "name": "Grade 9 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANfaMrI3H5DCTIxYDdDl4cDms_Pe00AArwZAALhtlhS8ppSjDK-qEQ2BA", "name": "Grade 9 Citizenship Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANiaMrI3AEBFqSG_VdFOtUZrIHL2UEAAsMZAALhtlhS7odgujTwrlc2BA", "name": "Grade 9 Geography Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANjaMrI3I19XQ-7cAABfBUUVm-wR6DdAALEGQAC4bZYUoIlIW9nDWk2NgQ", "name": "Grade 9 History Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANmaMrI3Dv6ZlpbLBr0Ctj3N819MlEAAsgZAALhtlhS2lAbRwdrz9A2BA", "name": "Grade 9 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANgaMrI3MuOLSfHsKS4GOW7ddTEH3IAAr0ZAALhtlhStS4QIQUF4lI2BA", "name": "Grade 9 Economics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANkaMrI3HIm2ItYvSBrTiXZhBJrZywAAsUZAALhtlhSXURUO-z_3QY2BA", "name": "Grade 9 HPE Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade10_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAM9aMq7rsCQ1AOjybW3lIoSxKpybYgAAmcZAALhtlhS-_g_YssiUNo2BA", "name": "Grade 10 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANBaMq7rmgxYAhEeC4knI0TOkWmP6AAAmwZAALhtlhSkFRrbWyvQf42BA", "name": "Grade 10 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANAaMq7roQOiZFIz-Fn2nRawFt9pxYAAmsZAALhtlhSPCEaKcuN1Uw2BA", "name": "Grade 10 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANCaMq7rt97TJ3IZoLau5sgSURMDPIAAnMZAALhtlhSYgLg9dxRHS42BA", "name": "Grade 10 Geography Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANDaMq7rlflVlWhXp3jPi3YwHeE6coAAnUZAALhtlhSTNaGMWBYlho2BA", "name": "Grade 10 History Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANFaMq7ru7ZfUyagxkTLS_GUQ8RtCsAAnwZAALhtlhSpwmT8GuaNIU2BA", "name": "Grade 10 Mathematics Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade10_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANpaMrJaptfb6PtXaDtSmjjEJ9rHDMAAswZAALhtlhSWSZK5GMIpT82BA", "name": "Grade 10 Citizenship Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANraMrJani3zFCxl-01x2DCz9qxHGUAAs8ZAALhtlhSF0FGnf1xrxI2BA", "name": "Grade 10 Geography Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANsaMrJavNfbJMO5BVkrBO5oqFC5IAAAtAZAALhtlhSL7HpLPjb99M2BA", "name": "Grade 10 History Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANvaMrJaljt9-9LTFz3uJAvW5GQFvQAAtUZAALhtlhSldmkxsKRxoQ2BA", "name": "Grade 10 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANqaMrJal1j3foWgeRCdt8WZs0COPsAAs0ZAALhtlhS-k_vDrOAQ5w2BA", "name": "Grade 10 Economics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANtaMrJaobAC972S5a39oaDhOVFN5QAAtEZAALhtlhSCz1NXr-LXoE2BA", "name": "Grade 10 HPE Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade11_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANHaMq-t7rwRD88_AuXbPyr1Kdb4acAAn8ZAALhtlhSAwZVti7ddh02BA", "name": "Grade 11 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANMaMq-txnb-NK_Ft5Jg2zmBbkpjUEAAosZAALhtlhSCDLxWiYC1Fc2BA", "name": "Grade 11 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANKaMq-tzLfFzn76CrHVgNhaEhA-3gAAoUZAALhtlhSIHeBRt0mino2BA", "name": "Grade 11 Civics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANOaMq-t2RfPRC8BCNoHxMC-t1H_RoAAo8ZAALhtlhS61K4QxV31RQ2BA", "name": "Grade 11 Geography Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANPaMq-txfuEitTpWlTvXlfNycpnJwAApAZAALhtlhSF3P9HvQ7smI2BA", "name": "Grade 11 History Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANQaMq-t9-Ggt-sX193hLOOMttRPPkAApMZAALhtlhSpjadicWaxoU2BA", "name": "Grade 11 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANLaMq-t2PJVrdb_8HxQqlTgo-COO4AAoYZAALhtlhSm6wNOzvqHso2BA", "name": "Grade 11 Economics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANNaMq-ty7_g3wSAjnRjGbjsasL4bwAAowZAALhtlhS6a7SL2mdQTM2BA", "name": "Grade 11 General Business Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade11_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN1aMrLawoWvO0yYOg7bcZOMiE-mgEAAvQZAALhtlhSNgIxFbdJQK02BA", "name": "Grade 11 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN2aMrLayKjnlVx0gnfLefoEwAB6A-TAAL2GQAC4bZYUglGwYya9sbENgQ", "name": "Grade 11 Geography Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN3aMrLa1pIzxQtR7TbMW5jmm08GBcAAvgZAALhtlhStq9YLwW7zEI2BA", "name": "Grade 11 History Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN5aMrLa7uDwcV4o3G5MpC90WAE9VMAAgwaAALhtlhSN7vMYKAopeE2BA", "name": "Grade 11 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN0aMrLa8NuLiSxx5WzMc2ke42lh2QAAuQZAALhtlhSR3XEZ2IWa8w2BA", "name": "Grade 11 Economics Textbook (New Curriculum)", "type": "document"},
        ],
        "social_textbook_grade12_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAANSaMrCniYuxIjRvZDH_MAPYvV27-wAApoZAALhtlhS0_Usx2bavkA2BA", "name": "Grade 12 Amharic Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANWaMrCni6RkhL8wAuLApGWaM95jXkAAqAZAALhtlhSzlAuTdE69LY2BA", "name": "Grade 12 English Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANYaMrCnn_1S-9sbPgriLqYwTEmzUsAAqIZAALhtlhSifVsfhA5MAM2BA", "name": "Grade 12 Geography Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANaaMrCnj69M06gyPHmFkZALR1-EZEAAqcZAALhtlhS-PWFfhUTbhY2BA", "name": "Grade 12 Mathematics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANVaMrCnla4d2TyCom6FDa9IhOyjOMAAp8ZAALhtlhSIzUaMmJBzx82BA", "name": "Grade 12 Economics Textbook (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAANXaMrCnvP9ssB-l8pe8pr32g_WvJUAAqEZAALhtlhSJ59CUDqWaa82BA", "name": "Grade 12 General Business Textbook (Old Curriculum)", "type": "document"},
        ],
        "social_textbook_grade12_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOAaMrNZtHvCkMCj5H7wNVdDK0aORIAAjUaAALhtlhSCxFgWqCb9ZY2BA", "name": "Grade 12 English Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOBaMrNZuvsqctoi_OXBRq09iknucAAAjcaAALhtlhSgNIXHUq_R-02BA", "name": "Grade 12 Geography Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOCaMrNZhBV3MgMfZ2IHWbFBlsh8jkAAjkaAALhtlhS5-mYVjf1iYs2BA", "name": "Grade 12 History Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOEaMrNZrTTNXtqiWlg0b3dSkKTcUcAAj4aAALhtlhSBP-qri2kVz82BA", "name": "Grade 12 Mathematics Textbook (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAN_aMrNZu5uQx5PfdhvUoOorqTMl_EAAjMaAALhtlhSFZNnXvkEmFY2BA", "name": "Grade 12 Economics Textbook (New Curriculum)", "type": "document"},
        ],
        
        # =============================================================================
        # 📖 TEACHER'S GUIDES (Free Resources)
        # =============================================================================
        # Grade-specific teacher's guides for both streams
        
        # Natural Stream Teacher's Guides - Old Curriculum
        "natural_guide_grade9_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOLaMrQp4wX-kl31H6k0XxWkNEPjgQAAlMaAALhtlhSzb8cghmCFrE2BA", "name": "English Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOKaMrQp5W6AYtwYd645XZy05CepasAAlIaAALhtlhS7nlgWx6Jn-o2BA", "name": "Civics Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAONaMrQp4hAT1NQeIuDPick0s7vcQ4AAlUaAALhtlhSXzVE9H9zv3M2BA", "name": "Mathematics Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOJaMrQpwllgrcV52gF6X06yDEQM3kAAlEaAALhtlhSAyOD09mtySE2BA", "name": "Chemistry Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOIaMrQp9jK4XTx2Ne05H1iGiKNiwwAAlAaAALhtlhScSBIeFQGNFQ2BA", "name": "Biology Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
        ],
        # Natural Stream Teacher's Guides - New Curriculum
        "natural_guide_grade9_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOnaMrSB5v-B6EI4HL1tJyTU0OCyXsAAnAaAALhtlhSsdWMnnp9nvw2BA", "name": "Mathematics Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOoaMrSB3bZmYKLUGRYEXpqxmZEYdQAAnEaAALhtlhSLbnJdzKIlOM2BA", "name": "Physics Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOiaMrSB2FXEUDjXzcAAdxrTpB07RRhAAJqGgAC4bZYUtB9Nb0FUkCENgQ", "name": "Biology Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOmaMrSB19uCJuSLt7LZESEdmPn7E4AAm8aAALhtlhSCP2JUetVDLI2BA", "name": "IT Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOlaMrSB5uUXaqy5ZyaFAlrCjmNyhEAAm0aAALhtlhSAAHR5JPXV8uQNgQ", "name": "HPE Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOpaMrSB4HZ2vSfSWAp5iDWi0bEmPEAAnIaAALhtlhS7hGCh4H5Lho2BA", "name": "PVA Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade10_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAORaMrRXse2SQVpc1CYzKUXGQABh-ojAAJZGgAC4bZYUv9Tqixv4VsMNgQ", "name": "English Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOQaMrRXsEhl81iT2e8eQVoTVZXPisAAlgaAALhtlhSuX2Mk-SWmmE2BA", "name": "Civics Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOTaMrRXgva55h5dLRKflVJVNQPdbgAAlsaAALhtlhSucu6PiwJNt42BA", "name": "Mathematics Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOUaMrRXspi3D1EheiDX0jhNguc-DMAAlwaAALhtlhSWt1yaS4Rq382BA", "name": "Physics Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOPaMrRXtD-w-hMlSvxIncKEiJXrPUAAlcaAALhtlhSRsiMfqcE5p42BA", "name": "Chemistry Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOOaMrRXsVH1YcgEUl-RUxuGS9_tiQAAlYaAALhtlhSjP4Xhp6Db1k2BA", "name": "Biology Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOVaMrRXs20YKemLPZzLbH-KpXduJcAAl0aAALhtlhS0QErLnzxU402BA", "name": "IT Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade10_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOtaMrSWBL2kuUAAdF_OkGvxtFBGw8FAAJ2GgAC4bZYUlkfN2Ruc7IQNgQ", "name": "English Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOraMrSWC0ejIRpjPXtUIhVmzQUMhkAAnQaAALhtlhSwXTu_qwh0Uc2BA", "name": "Citizenship Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOyaMrSWAlX9WruhqLAe2QAAcNLY1p9AAJ7GgAC4bZYUhlV1503KdGhNgQ", "name": "Mathematics Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOzaMrSWI3mhkSYFGRRJF99lPsl9RkAAnwaAALhtlhSTN1BISiq80A2BA", "name": "Physics Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOqaMrSWOIdXGeK9H2vL2trgvcYSeMAAnMaAALhtlhSB_KlUOT898g2BA", "name": "Chemistry Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOxaMrSWM6Kfs_6mraweRDRkgEeiycAAnoaAALhtlhS-Q9IZznC8-Y2BA", "name": "IT Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOwaMrSWFcYc23jLMuEjHYyRtJGhj0AAnkaAALhtlhSMhR-yN8gx_M2BA", "name": "HPE Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade11_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOZaMrRrRvopwNtorJh0MzTjYAZhmIAAmAaAALhtlhSgYXqdNIiG2Y2BA", "name": "English Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAObaMrRrUk2nyUzYnelwTSghbiIKAUAAmIaAALhtlhSFpGIucnUm5M2BA", "name": "Mathematics Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOcaMrRrb_4FoL55Nmty59aSYEtiiQAAmMaAALhtlhSu5n4ezJG9WA2BA", "name": "Physics Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOXaMrRrT8cNsV1YqHBE4DokXvQNqEAAl4aAALhtlhS47T5IJGnTA82BA", "name": "Chemistry Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade11_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO3aMrTKsOlqc8qzf3SStpMxVDLp9QAAoEaAALhtlhSJKueWx9WOh82BA", "name": "English Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO7aMrTKnp5J1yGdu3YOHmI9xZMoUcAAosaAALhtlhSmM8x9Qi-X_U2BA", "name": "Mathematics Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO8aMrTKiN2VE6CfKEnFyEI1Y0IJucAAowaAALhtlhSNikvncemyk02BA", "name": "Physics Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO1aMrTKjGWRORr_uTUyigzIda8U-cAAn8aAALhtlhSmww47jZfyeA2BA", "name": "Chemistry Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO0aMrTKr7Xo3vUrE43vuXKCZHWA-wAAn0aAALhtlhSSSGaKiyicZQ2BA", "name": "Agriculture Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO6aMrTKs89pm-Aq0cmVEM7fc_YCOMAAoUaAALhtlhSyOF4f6O6czQ2BA", "name": "IT Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
        ],
        "natural_guide_grade12_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOhaMrR3tWi_oQfXntWxCgMpsrWUhEAAmkaAALhtlhSB57clCk19C82BA", "name": "Physics Teacher's Guide Grade 12 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOdaMrR3jSE2UNhAt_vhCAjjTTVCTIAAmQaAALhtlhS70psGunBNy82BA", "name": "Chemistry Teacher's Guide Grade 12 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOgaMrR3tuHH6o5tEOHmzVy9iMfKg0AAmcaAALhtlhS3wdZIySG8uI2BA", "name": "IT Teacher's Guide Grade 12 (Old Curriculum)", "type": "document"},
        ],
        "natural_guide_grade12_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPAaMrTtGC456MmsthLAqUJZ5uLRloAApMaAALhtlhSv3v4aLDTTHg2BA", "name": "English Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPCaMrTtMbgi-6TxV-zefJGLbNXnDgAApgaAALhtlhSDJeVAyNGT2c2BA", "name": "Mathematics Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPDaMrTtJHK7RrUVX72P0j1KdJwx4QAApkaAALhtlhS4PptVcp7Nec2BA", "name": "Physics Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO_aMrTtGPxHNR9J6qKHofmTq9ZyR4AApIaAALhtlhSk85L2fOX0Y42BA", "name": "Chemistry Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO-aMrTtMPWvmhqxV9fcW2A8fT7wd4AApEaAALhtlhS7jMdMcfwE8M2BA", "name": "Biology Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO9aMrTtL7fCTa3o2oQLO8JPCrXIVAAAo4aAALhtlhSpMibkqjwuRc2BA", "name": "Agriculture Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPBaMrTtPVMlo-OSYyrDpK0Kd9TJkMAApQaAALhtlhSvneeDsem74g2BA", "name": "IT Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
        ],
        
        # Social Stream Teacher's Guides
        "social_guide_grade9_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOLaMrQp4wX-kl31H6k0XxWkNEPjgQAAlMaAALhtlhSzb8cghmCFrE2BA", "name": "English Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOKaMrQp5W6AYtwYd645XZy05CepasAAlIaAALhtlhS7nlgWx6Jn-o2BA", "name": "Civics Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOMaMrQpxf6SW8tsDxaSDjBKlK5agwAAlQaAALhtlhSbZFyWXT6UCQ2BA", "name": "Geography Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAONaMrQp4hAT1NQeIuDPick0s7vcQ4AAlUaAALhtlhSXzVE9H9zv3M2BA", "name": "Mathematics Teacher's Guide Grade 9 (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade9_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOjaMrSB8MzCdgMHvAmZroCLnnuSV0AAmsaAALhtlhSdLlBdkO0Xz42BA", "name": "Geography Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOkaMrSB1zL4mGiak6jNovzltSMAQYAAmwaAALhtlhSRmEQ3YxWofE2BA", "name": "History Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOnaMrSB5v-B6EI4HL1tJyTU0OCyXsAAnAaAALhtlhSsdWMnnp9nvw2BA", "name": "Mathematics Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOlaMrSB5uUXaqy5ZyaFAlrCjmNyhEAAm0aAALhtlhSAAHR5JPXV8uQNgQ", "name": "HPE Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOpaMrSB4HZ2vSfSWAp5iDWi0bEmPEAAnIaAALhtlhS7hGCh4H5Lho2BA", "name": "PVA Teacher's Guide Grade 9 (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade10_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAORaMrRXse2SQVpc1CYzKUXGQABh-ojAAJZGgAC4bZYUv9Tqixv4VsMNgQ", "name": "English Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOQaMrRXsEhl81iT2e8eQVoTVZXPisAAlgaAALhtlhSuX2Mk-SWmmE2BA", "name": "Civics Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOSaMrRXr5ddE1rS2Fn9uAo4RB7ISEAAloaAALhtlhS2tZgRCFtyAc2BA", "name": "Geography Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOTaMrRXgva55h5dLRKflVJVNQPdbgAAlsaAALhtlhSucu6PiwJNt42BA", "name": "Mathematics Teacher's Guide Grade 10 (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade10_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOtaMrSWBL2kuUAAdF_OkGvxtFBGw8FAAJ2GgAC4bZYUlkfN2Ruc7IQNgQ", "name": "English Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOraMrSWC0ejIRpjPXtUIhVmzQUMhkAAnQaAALhtlhSwXTu_qwh0Uc2BA", "name": "Citizenship Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOuaMrSWIZR_e1XAkyG4EAG_KnpOR4AAncaAALhtlhSQO3k-VwjwjI2BA", "name": "Geography Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOvaMrSWIpqNKrNU-28JNMfiM8mghEAAngaAALhtlhSagPPeKrwGd82BA", "name": "History Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOyaMrSWAlX9WruhqLAe2QAAcNLY1p9AAJ7GgAC4bZYUhlV1503KdGhNgQ", "name": "Mathematics Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOsaMrSWEPMyl_blciRBeZ9CG8eLigAAnUaAALhtlhSNRAs5CH3Elw2BA", "name": "Economics Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOwaMrSWFcYc23jLMuEjHYyRtJGhj0AAnkaAALhtlhSMhR-yN8gx_M2BA", "name": "HPE Teacher's Guide Grade 10 (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade11_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOZaMrRrRvopwNtorJh0MzTjYAZhmIAAmAaAALhtlhSgYXqdNIiG2Y2BA", "name": "English Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOaaMrRrag5JzxVOdLpkbXcr3AIq_cAAmEaAALhtlhSPxpu0zsYHNI2BA", "name": "Geography Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAObaMrRrUk2nyUzYnelwTSghbiIKAUAAmIaAALhtlhSFpGIucnUm5M2BA", "name": "Mathematics Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOYaMrRrQkZQEGjQWghz4u0Xrqbe10AAl8aAALhtlhSTeQVmI7r1zc2BA", "name": "Economics Teacher's Guide Grade 11 (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade11_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO3aMrTKsOlqc8qzf3SStpMxVDLp9QAAoEaAALhtlhSJKueWx9WOh82BA", "name": "English Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO4aMrTKlZEeAvi41xE9kVBwha58Q4AAoIaAALhtlhScSAv3pVyrKc2BA", "name": "Geography Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO5aMrTKsIHoDHnPU34nRzH0Up6qZkAAoQaAALhtlhS6sZhLJSiy842BA", "name": "History Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO7aMrTKnp5J1yGdu3YOHmI9xZMoUcAAosaAALhtlhSmM8x9Qi-X_U2BA", "name": "Mathematics Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAO2aMrTKtL9YdKyJn7W-1vTvITDxjUAAoAaAALhtlhSdHS15ZzezBA2BA", "name": "Economics Teacher's Guide Grade 11 (New Curriculum)", "type": "document"},
        ],
        "social_guide_grade12_old": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOfaMrR3iUr938mmDYRu04c1q7BS5gAAmYaAALhtlhShJ8flJqVkvw2BA", "name": "Geography Teacher's Guide Grade 12 (Old Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAOeaMrR3g7naWEeoVBncFfrkILsvYcAAmUaAALhtlhSzsrhnyEKeho2BA", "name": "Economics Teacher's Guide Grade 12 (Old Curriculum)", "type": "document"},
        ],
        "social_guide_grade12_new": [
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPAaMrTtGC456MmsthLAqUJZ5uLRloAApMaAALhtlhSv3v4aLDTTHg2BA", "name": "English Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPCaMrTtMbgi-6TxV-zefJGLbNXnDgAApgaAALhtlhSDJeVAyNGT2c2BA", "name": "Mathematics Teacher's Guide Grade 12 (New Curriculum)", "type": "document"},
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
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPHaMraYeDxW3MuZhUrJMO3r5EgIowAAqkaAALhtlhSozYWVQE-J1k2BA", "name": "2002 English Exam", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPIaMraYf2AjQABzqQIrwTrPq48owHCAAKqGgAC4bZYUrKTz-A2x39UNgQ", "name": "2002 Geography Exam", "type": "document"},
            {"file_id": "BQACAgQAAyEFAASkzI5MAAPJaMraYT8tj9fHr7UuRlPfjKt3HzQAAqsaAALhtlhSo3XaBEFMpDo2BA", "name": "2002 History Exam", "type": "document"},
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