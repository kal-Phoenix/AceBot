# services/gemini_ai.py

import google.generativeai as genai
from config import Config
import logging

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def chat_with_gemini(self, user_id: int, user_message: str, chat_history: list = None):
        try:
            # Prompt: Encourage emojis, strictly forbid Markdown/bold/italics.
            modified_message = (
                f"{user_message}\n\n"
                f"Please provide a helpful and clear response. "
                f"You can use relevant emojis to make the response more engaging. "
                f"However, do NOT use any Markdown, bolding (**), italics (*), or any other text formatting. "
                f"Keep the response in plain text."
            )

            # Note: For persistent chat history, you would pass 'chat_history' to generate_content_async
            # For now, we are sending each message as a new request.
            response = await self.model.generate_content_async(modified_message)

            return response.text, [] # Return an empty list for chat history if not being used
        except Exception as e:
            logger.error(f"Error communicating with Gemini AI for user {user_id}: {e}")
            return "🤖 Sorry, I'm having trouble connecting to the AI right now. Please try again later.", []