# services/gemini_ai.py

import google.generativeai as genai
from config import Config
import logging
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self._conversation_history = {}  # Store history per user_id

    async def chat_with_gemini(self, user_id: int, user_message: str, context: ContextTypes.DEFAULT_TYPE = None):
        try:
            # Initialize or retrieve conversation history for the user
            if user_id not in self._conversation_history:
                self._conversation_history[user_id] = []

            # Limit history to the last 3 exchanges to manage context and token usage
            history = self._conversation_history[user_id][-6:]  # Max 3 question-answer pairs

            # Construct the prompt with context and instructions
            system_prompt = (
                "🌟 You are an expert tutor for the Ethiopian University Entrance Examination (UEE). "
                "Your mission is to help students excel! 🎓 "
                "You were developed by Kaleab Dereje and Phoenix Team from Addis Ababa University (AAU). 🇪🇹 "
                "Provide answers related to UEE subjects. "
                "Keep your responses concise, ideally a few sentences per point. "
                "You MAY use bullet points (•) for main explanations or lists. "
                "DO NOT use any other Markdown formatting whatsoever (no asterisks for bolding, no italics, no hashtags). "
                "Instead, use relevant emojis generously throughout your response to make it engaging and easy to read. "
                "If it's a problem, give the solution directly or a very brief step-by-step. 📝 "
                "If it's a concept, explain it using clear, short bullet points. 💡 "
                "Always provide answers relevant to the Ethiopian curriculum where applicable. "
                "Here is the student's question: "
            )

            # Build the conversation context
            conversation_context = "\n".join(history) if history else ""
            if conversation_context:
                conversation_context += "\n"

            # Full prompt including history and user message
            full_prompt = (
                f"{system_prompt}\n\n"
                f"Conversation history (if any):\n{conversation_context}"
                f"User question: {user_message}\n"
                f"Respond now."
            )

            # Generate response
            response = await self.model.generate_content_async(full_prompt)

            # Update history with user message and response
            self._conversation_history[user_id].append(f"User: {user_message}")
            self._conversation_history[user_id].append(f"Assistant: {response.text}")

            return response.text
        except Exception as e:
            logger.error(f"Error communicating with Gemini AI for user {user_id}: {e}")
            return "🤖 Sorry, I'm having trouble connecting to the AI right now. Please try again later."