import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Channel Configuration
class ChannelConfig:
    # Textbooks & Guides Channels
    OLD_TEXTBOOKS_CHANNEL_ID = os.getenv("OLD_TEXTBOOKS_CHANNEL_ID", "-1001234567891")
    OLD_GUIDES_CHANNEL_ID = os.getenv("OLD_GUIDES_CHANNEL_ID", "-1001234567892")
    NEW_TEXTBOOKS_CHANNEL_ID = os.getenv("NEW_TEXTBOOKS_CHANNEL_ID", "-1001234567893")
    NEW_GUIDES_CHANNEL_ID = os.getenv("NEW_GUIDES_CHANNEL_ID", "-1001234567894")
    
    # Notes Channels
    NOTES_NATURAL_CHANNEL_ID = os.getenv("NOTES_NATURAL_CHANNEL_ID", "-1001234567895")
    NOTES_SOCIAL_CHANNEL_ID = os.getenv("NOTES_SOCIAL_CHANNEL_ID", "-1001234567896")
    
    # Quizzes Channels
    QUIZZES_NATURAL_CHANNEL_ID = os.getenv("QUIZZES_NATURAL_CHANNEL_ID", "-1001234567897")
    QUIZZES_SOCIAL_CHANNEL_ID = os.getenv("QUIZZES_SOCIAL_CHANNEL_ID", "-1001234567898")
    
    # Past Exams Channels
    EXAMS_YEARLY_CHANNEL_ID = os.getenv("EXAMS_YEARLY_CHANNEL_ID", "-1001234567899")
    EXAMS_TOPICS_CHANNEL_ID = os.getenv("EXAMS_TOPICS_CHANNEL_ID", "-1001234567900")
    
    # Tips Channels
    EXAM_TIPS_CHANNEL_ID = os.getenv("EXAM_TIPS_CHANNEL_ID", "-1001234567901")
    STUDY_TIPS_CHANNEL_ID = os.getenv("STUDY_TIPS_CHANNEL_ID", "-1001234567902")
    
    # Channel Mappings
    CHANNELS = {
        # Textbooks & Guides
        'old_textbooks': {'id': OLD_TEXTBOOKS_CHANNEL_ID},
        'old_guides': {'id': OLD_GUIDES_CHANNEL_ID},
        'new_textbooks': {'id': NEW_TEXTBOOKS_CHANNEL_ID},
        'new_guides': {'id': NEW_GUIDES_CHANNEL_ID},
        
        # Notes
        'notes_natural': {'id': NOTES_NATURAL_CHANNEL_ID},
        'notes_social': {'id': NOTES_SOCIAL_CHANNEL_ID},
        
        # Quizzes
        'quizzes_natural': {'id': QUIZZES_NATURAL_CHANNEL_ID},
        'quizzes_social': {'id': QUIZZES_SOCIAL_CHANNEL_ID},
        
        # Past Exams
        'exams_yearly': {'id': EXAMS_YEARLY_CHANNEL_ID},
        'exams_topics': {'id': EXAMS_TOPICS_CHANNEL_ID},
        
        # Tips
        'exam_tips': {'id': EXAM_TIPS_CHANNEL_ID},
        'study_tips': {'id': STUDY_TIPS_CHANNEL_ID}
    }
    
    @classmethod
    def get_channel_id(cls, channel_type):
        """Helper method to get channel ID by type"""
        channel = cls.CHANNELS.get(channel_type, {})
        return channel.get('id') if channel else None
