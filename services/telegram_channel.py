# services/telegram_channel.py

import logging
from typing import List, Dict, Optional
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from config import Config

logger = logging.getLogger(__name__)

class TelegramChannelService:
    """
    Service to handle content retrieval from a single Telegram channel
    using hashtag-based organization.
    """
    
    def __init__(self, channel_username: str = None):
        self.channel_username = channel_username or Config.CONTENT_CHANNEL_USERNAME
        self.channel_id = Config.CONTENT_CHANNEL_ID
    
    async def get_content(self, 
                        context: ContextTypes.DEFAULT_TYPE, 
                        stream: str, 
                        resource_type: str, 
                        subject: str = None, 
                        grade: str = None, 
                        year: str = None, 
                        is_premium: bool = False,
                        user_id: int = None) -> List[Dict]:
        """
        Retrieve content using direct file_id mapping.
        
        Args:
            context: Telegram context for API calls
            stream: 'natural' or 'social'
            resource_type: 'textbook', 'notes', 'quiz', 'pastexam', 'examtips', 'studytips', 'cheats'
            subject: Subject name (optional)
            grade: Grade level (optional)
            year: Year for past exams (optional)
            is_premium: Whether this is premium content
            user_id: User ID to forward files to
            
        Returns:
            List of forwarded content or file info
        """
        try:
            # Build content key for file_id mapping
            content_key = self._build_content_key(stream, resource_type, subject, grade, year)
            logger.info(f"Built content key: {content_key} from stream={stream}, resource_type={resource_type}, grade={grade}")
            
            # Get file_ids from mapping
            file_ids = self._get_file_ids_mapping(content_key)
            logger.info(f"Found {len(file_ids)} files for key: {content_key}")
            
            if not file_ids:
                logger.info(f"No content found for key: {content_key}")
                return []
            
            # Send files directly to user if user_id provided
            if user_id and context:
                sent_files = []
                for file_info in file_ids:
                    try:
                        file_id = file_info['file_id']
                        file_name = file_info.get('name', 'Untitled')
                        file_type = file_info.get('type', 'document')
                        
                        # Send file directly to user with content protection for premium content
                        if file_type == 'document':
                            sent_msg = await context.bot.send_document(
                                chat_id=user_id,
                                document=file_id,
                                caption=file_name,
                                protect_content=is_premium
                            )
                        elif file_type == 'photo':
                            sent_msg = await context.bot.send_photo(
                                chat_id=user_id,
                                photo=file_id,
                                caption=file_name,
                                protect_content=is_premium
                            )
                        else:
                            # Default to document
                            sent_msg = await context.bot.send_document(
                                chat_id=user_id,
                                document=file_id,
                                caption=file_name,
                                protect_content=is_premium
                            )
                        
                        sent_files.append({
                            'file_id': file_id,
                            'file_name': file_name,
                            'sent': True,
                            'sent_message_id': sent_msg.message_id,
                            'success': True
                        })
                        logger.info(f"Sent file {file_name} to user {user_id}")
                        
                    except Exception as e:
                        logger.error(f"Failed to send file {file_name} to user {user_id}: {e}")
                        sent_files.append({
                            'file_id': file_id,
                            'file_name': file_name,
                            'sent': False,
                            'success': False,
                            'error': str(e)
                        })
                
                return sent_files
            
            # If no user_id, return file info for display purposes
            content_list = []
            for file_info in file_ids:
                content_item = {
                    'file_id': file_info['file_id'],
                    'file_name': file_info.get('name', 'Untitled'),
                    'file_type': file_info.get('type', 'document'),
                    'is_premium': is_premium
                }
                content_list.append(content_item)
            
            logger.info(f"Retrieved {len(content_list)} items for key: {content_key}")
            return content_list
            
        except Exception as e:
            logger.error(f"Error retrieving content: {e}")
            return []
    
    def _build_content_key(self, stream: str, resource_type: str, 
                          subject: str = None, grade: str = None, year: str = None) -> str:
        """
        Build a content key for file_id mapping.
        
        Args:
            stream: 'natural' or 'social'
            resource_type: 'textbook', 'notes', 'quiz', etc.
            subject: Subject name (optional)
            grade: Grade level (optional) 
            year: Year for past exams (optional)
            
        Returns:
            Content key string for mapping lookup
        """
        key_parts = [stream, resource_type]
        
        if subject:
            key_parts.append(subject.lower())
        if grade:
            if "_" in grade:  # Handle curriculum suffix like "9_old" or "9_new"
                grade_parts = grade.split("_")
                key_parts.append(f"grade{grade_parts[0]}")
                if len(grade_parts) > 1:
                    key_parts.append(grade_parts[1])  # Add curriculum type (old/new)
            else:
                key_parts.append(f"grade{grade}" if grade != "mixed" else "mixed")
        if year:
            key_parts.append(str(year))
            
        return "_".join(key_parts)
    
    def _get_file_ids_mapping(self, content_key: str) -> List[Dict]:
        """
        Get file_ids from Config.FILE_IDS based on content key.
        
        Args:
            content_key: Content key built from stream, resource_type, etc.
            
        Returns:
            List of file info dictionaries from config
        """
        return Config.FILE_IDS.get(content_key, [])
    
    async def get_textbooks(self, context: ContextTypes.DEFAULT_TYPE, 
                           stream: str, grade: str, user_id: int = None) -> List[Dict]:
        """Get textbooks for a specific stream and grade."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="textbook",
            grade=grade,
            is_premium=False,
            user_id=user_id
        )
    
    async def get_teachers_guide(self, context: ContextTypes.DEFAULT_TYPE, 
                                stream: str, grade: str, user_id: int = None) -> List[Dict]:
        """Get teacher's guides for a specific stream and grade."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="guide",
            grade=grade,
            is_premium=False,
            user_id=user_id
        )
    
    async def get_notes(self, context: ContextTypes.DEFAULT_TYPE, 
                       stream: str, subject: str, user_id: int = None) -> List[Dict]:
        """Get notes for a specific stream and subject (Premium)."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="notes",
            subject=subject,
            is_premium=True,
            user_id=user_id
        )
    
    async def get_cheat_sheets(self, context: ContextTypes.DEFAULT_TYPE, 
                              stream: str, subject: str, user_id: int = None) -> List[Dict]:
        """Get cheat sheets for a specific stream and subject (Premium)."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="cheats",
            subject=subject,
            is_premium=True,
            user_id=user_id
        )
    
    async def get_quizzes(self, context: ContextTypes.DEFAULT_TYPE, 
                         stream: str, subject: str, grade: str, user_id: int = None) -> List[Dict]:
        """Get quizzes for a specific stream, subject, and grade (Premium)."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="quiz",
            subject=subject,
            grade=grade,
            is_premium=True,
            user_id=user_id
        )
    
    async def get_past_exams_by_year(self, context: ContextTypes.DEFAULT_TYPE, 
                                    stream: str, year: str, user_id: int = None) -> List[Dict]:
        """Get past exams for a specific year."""
        # Years 2002-2017 are premium, only 2000-2001 are free
        year_int = int(year) if isinstance(year, str) else year
        is_premium = year_int >= 2002
        
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="pastexam",
            year=year,
            is_premium=is_premium,
            user_id=user_id
        )
    
    async def get_past_exams_by_topic(self, context: ContextTypes.DEFAULT_TYPE, 
                                     stream: str, subject: str, user_id: int = None) -> List[Dict]:
        """Get past exams organized by topic/subject."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="pastexam",
            subject=subject,
            is_premium=False,
            user_id=user_id
        )
    
    async def get_exam_tips(self, context: ContextTypes.DEFAULT_TYPE, 
                           stream: str, user_id: int = None) -> List[Dict]:
        """Get exam tips for a specific stream (Premium)."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="examtips",
            is_premium=True,
            user_id=user_id
        )
    
    async def get_study_tips(self, context: ContextTypes.DEFAULT_TYPE, 
                            stream: str, user_id: int = None) -> List[Dict]:
        """Get study tips for a specific stream (Premium)."""
        return await self.get_content(
            context=context,
            stream=stream,
            resource_type="studytips",
            is_premium=True,
            user_id=user_id
        )
