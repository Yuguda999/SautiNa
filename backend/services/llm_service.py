"""
N-ATLaS LLM Service
Integrates with the deployed N-ATLaS model on Modal for multilingual responses.
"""
from openai import OpenAI
from typing import Optional, Tuple
import logging

from config import settings, SupportedLanguage, SYSTEM_PROMPTS, TEACHER_PROMPTS, ChatMode
from services.search_service import search_service
from services.intent_service import intent_service, Intent

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with N-ATLaS LLM"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.natlas_api_url,
            api_key=settings.natlas_api_key,
        )
        self.model = settings.natlas_model_name
    
    async def generate_response(
        self,
        user_message: str,
        language: SupportedLanguage = SupportedLanguage.ENGLISH,
        conversation_history: Optional[list] = None,
        mode: ChatMode = ChatMode.CHAT
    ) -> Tuple[str, Intent]:
        """
        Generate a response from N-ATLaS LLM.
        
        Args:
            user_message: The user's message/question
            language: Target language for response
            conversation_history: Optional previous messages for context
            mode: Chat mode - CHAT for normal, LEARN for teacher mode
            
        Returns:
            Tuple of (AI-generated response text, detected intent)
        """
        try:
            # In learn mode, always use LEARN intent (no search needed)
            if mode == ChatMode.LEARN:
                intent = Intent.LEARN
            else:
                # Use intent classification for chat mode
                intent = intent_service.classify_quick(user_message)
                if intent is None:
                    intent = await intent_service.classify(user_message)
            
            logger.info(f"Mode: {mode.value}, Detected intent: {intent.value}")
            
            # Perform search if intent requires real-time data (only in chat mode)
            search_context = ""
            if mode == ChatMode.CHAT and intent == Intent.SEARCH:
                search_results = search_service.search(user_message)
                if search_results:
                    search_context = f"\n\nCONTEXT FROM WEB SEARCH:\n{search_results}\nUse this information to answer the user's question if relevant."

            # Select system prompt based on mode
            if mode == ChatMode.LEARN:
                system_prompt = TEACHER_PROMPTS.get(language, TEACHER_PROMPTS[SupportedLanguage.ENGLISH])
            else:
                system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS[SupportedLanguage.ENGLISH])
            
            # STRICTLY enforce language
            enforcement_instruction = f"\n\nIMPORTANT: You MUST respond in {language.name} ({language.value}). Do not switch languages unless explicitly asked."
            
            messages = [
                {"role": "system", "content": system_prompt + enforcement_instruction + search_context}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Sending to N-ATLaS ({mode.value} mode): {user_message[:100]}...")
            
            # Call N-ATLaS API (synchronous but wrapped for async)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            
            assistant_message = response.choices[0].message.content
            logger.info(f"N-ATLaS response: {assistant_message[:100]}...")
            
            return assistant_message, intent
            
        except Exception as e:
            logger.error(f"N-ATLaS API error: {str(e)}")
            # Fallback response
            fallback_messages = {
                SupportedLanguage.HAUSA: "Yi haƙuri, matsala ta faru. Da fatan za a sake gwadawa.",
                SupportedLanguage.YORUBA: "E jọ̀wọ́, ìṣòro kan wáyé. Ẹ gbìyànjú lẹ́ẹ̀kan síi.",
                SupportedLanguage.IGBO: "Biko, nsogbu mere. Gbalịa ọzọ.",
                SupportedLanguage.PIDGIN: "Abeg, problem happen. Try again abeg.",
                SupportedLanguage.ENGLISH: "Sorry, an error occurred. Please try again.",
            }
            return fallback_messages.get(language, fallback_messages[SupportedLanguage.ENGLISH]), Intent.CHAT

    async def translate(
        self,
        text: str,
        source_language: SupportedLanguage,
        target_language: SupportedLanguage
    ) -> str:
        """
        Translate text between supported languages using N-ATLaS.
        
        Args:
            text: Text to translate
            source_language: Source language of the text
            target_language: Target language for translation
            
        Returns:
            Translated text
        """
        try:
            # Language name mapping for clearer prompts
            language_names = {
                SupportedLanguage.HAUSA: "Hausa",
                SupportedLanguage.YORUBA: "Yoruba",
                SupportedLanguage.IGBO: "Igbo",
                SupportedLanguage.PIDGIN: "Nigerian Pidgin",
                SupportedLanguage.ENGLISH: "English",
            }
            
            source_name = language_names.get(source_language, "the source language")
            target_name = language_names.get(target_language, "the target language")
            
            # Build translation prompt
            system_prompt = f"""You are a professional translator specializing in Nigerian languages.
Your task is to translate text accurately from {source_name} to {target_name}.
Preserve the meaning, tone, and cultural context of the original text.
Only output the translated text, nothing else. Do not add explanations or notes."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate this from {source_name} to {target_name}:\n\n{text}"}
            ]
            
            logger.info(f"Translating from {source_name} to {target_name}: {text[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.3,  # Lower temperature for more accurate translation
            )
            
            translated_text = response.choices[0].message.content.strip()
            logger.info(f"Translation result: {translated_text[:50]}...")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise Exception(f"Translation failed: {str(e)}")


# Singleton instance
llm_service = LLMService()
