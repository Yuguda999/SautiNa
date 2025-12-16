"""
Intent Classification Service
Uses N-ATLaS to intelligently classify user intent for smart routing.
"""
from enum import Enum
from openai import OpenAI
import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)


class Intent(str, Enum):
    """Possible user intents"""
    SEARCH = "search"       # Needs real-time data (weather, prices, news)
    TRANSLATE = "translate" # Translation request
    LEARN = "learn"         # Educational/learning request
    CHAT = "chat"           # General conversation


INTENT_CLASSIFICATION_PROMPT = """You are an intent classifier for a Nigerian AI assistant. Analyze the user's message and classify it into exactly ONE of these intents.
IMPORTANT: You must handle input in English, Nigerian Pidgin, Hausa, Yoruba, and Igbo.

SEARCH - User needs current/real-time information:
  - Weather (e.g., "weather", "oju ojo", "yanayi", "ihu igwe")
  - Prices (e.g., "price", "owo", "nawa ne", "ego ole")
  - News/Events (e.g., "news", "iroyin", "labarai", "ozi")
  - "Today", "now", "current" queries

TRANSLATE - User wants to translate text:
  - Explicitly asks to translate
  - "How do you say X in Y"
  - "Tumọ", "Fassara", "Kowaa"

LEARN - User wants to learn or be taught:
  - "Teach me", "Explain", "Kọ mi", "Koya min"
  - Educational content (health, farming, tech)
  - "How to", "Yadda ake", "Bawo ni a se"

CHAT - General conversation:
  - Greetings ("Bawo", "Sannu", "Kedu", "How far")
  - Small talk, personal questions
  - Jokes, stories

Respond with ONLY the intent word in lowercase: search, translate, learn, or chat"""


class IntentService:
    """Service for classifying user intent using N-ATLaS"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.natlas_api_url,
            api_key=settings.natlas_api_key,
        )
        self.model = settings.natlas_model_name
    
    async def classify(self, user_message: str) -> Intent:
        """
        Classify the intent of a user message.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Intent enum value
        """
        try:
            logger.info(f"Classifying intent for: {user_message[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=10,  # Only need one word
                temperature=0.1,  # Low temperature for consistent classification
            )
            
            intent_text = response.choices[0].message.content.strip().lower()
            logger.info(f"Classified intent: {intent_text}")
            
            # Map response to Intent enum
            intent_map = {
                "search": Intent.SEARCH,
                "translate": Intent.TRANSLATE,
                "learn": Intent.LEARN,
                "chat": Intent.CHAT,
            }
            
            intent = intent_map.get(intent_text, Intent.CHAT)
            return intent
            
        except Exception as e:
            logger.error(f"Intent classification error: {str(e)}")
            # Default to CHAT on error
            return Intent.CHAT
    
    def classify_quick(self, user_message: str) -> Intent:
        """
        Quick heuristic-based classification as fallback.
        Uses pattern matching for obvious cases to save API calls.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Intent enum value or None if unsure
        """
        message_lower = user_message.lower()
        
        # Clear translation indicators
        translate_patterns = [
            "translate", "translation", "how do you say",
            "in hausa", "in yoruba", "in igbo", "in pidgin", "in english",
            "to hausa", "to yoruba", "to igbo", "to pidgin", "to english",
            "tumọ", "fassara", "kowaa", # Local translation keywords
        ]
        if any(pattern in message_lower for pattern in translate_patterns):
            return Intent.TRANSLATE
        
        # Clear search indicators (real-time data)
        search_patterns = [
            "weather", "price", "market price", "news", "today",
            "current", "now", "latest", "how much is", "cost of",
            "oju ojo", "iroyin", "owo", # Yoruba
            "yanayi", "labarai", "nawa ne", # Hausa
            "ihu igwe", "ozi", "ego ole", # Igbo
        ]
        if any(pattern in message_lower for pattern in search_patterns):
            return Intent.SEARCH
        
        # Clear learning indicators
        learn_patterns = [
            "teach me", "explain", "learn about", "tell me about",
            "what is", "how do i", "how to", "guide me", "help me understand",
            "kọ mi", "koya min", "kuziere m", # Local learning keywords
        ]
        if any(pattern in message_lower for pattern in learn_patterns):
            return Intent.LEARN
        
        # If no clear pattern, return None to trigger LLM classification
        return None


# Singleton instance
intent_service = IntentService()
