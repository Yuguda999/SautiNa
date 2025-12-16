"""
Voice Pipeline Service
Orchestrates the full voice-to-voice pipeline: STT → LLM → TTS
"""
import logging
from typing import Optional, Tuple

from config import SupportedLanguage, ChatMode
from services.stt_service import stt_service
from services.llm_service import llm_service
from services.tts_service import tts_service
from schemas import VoiceResponse

logger = logging.getLogger(__name__)


class PipelineService:
    """Main orchestration service for voice processing"""
    
    async def process_voice(
        self,
        audio_data: bytes,
        filename: str = "audio.wav",
        preferred_language: Optional[SupportedLanguage] = None,
        mode: ChatMode = ChatMode.CHAT
    ) -> VoiceResponse:
        """
        Process a voice message through the full pipeline.
        
        Pipeline: Audio → STT → LLM → TTS → Audio
        
        Args:
            audio_data: Raw audio bytes from user
            filename: Original filename
            preferred_language: Optional language override
            mode: Chat mode (chat or learn)
            
        Returns:
            VoiceResponse with transcription, response, and audio URL
        """
        logger.info(f"🎤 Starting voice pipeline (mode: {mode.value})...")
        
        # Step 1: Speech-to-Text
        logger.info("Step 1: Transcribing audio...")
        transcribed_text, detected_language = await stt_service.transcribe(
            audio_data, filename
        )
        
        # Use preferred language if provided, otherwise use detected
        language = preferred_language or detected_language
        logger.info(f"Using language: {language.value}")
        
        # Step 2: Generate LLM response
        logger.info("Step 2: Generating AI response...")
        response_text, intent = await llm_service.generate_response(
            transcribed_text, language, mode=mode
        )
        logger.info(f"Intent detected: {intent.value}")
        
        # Step 3: Text-to-Speech
        logger.info("Step 3: Synthesizing speech...")
        audio_url = None
        try:
            audio_path = await tts_service.synthesize(response_text, language)
            audio_url = await tts_service.get_audio_url(audio_path)
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            # Continue without audio, don't crash the pipeline
        
        logger.info("✅ Voice pipeline complete!")
        
        return VoiceResponse(
            transcribed_text=transcribed_text,
            response_text=response_text,
            detected_language=language,
            audio_url=audio_url
        )
    
    async def process_text(
        self,
        text: str,
        language: Optional[SupportedLanguage] = None,
        mode: ChatMode = ChatMode.CHAT
    ) -> Tuple[str, SupportedLanguage, Optional[str]]:
        """
        Process a text message (useful for testing without audio).
        
        Args:
            text: User's text message
            language: Language for response
            mode: Chat mode (chat or learn for teacher mode)
            
        Returns:
            Tuple of (response_text, language, audio_url)
        """
        # Default to English if not specified
        lang = language or SupportedLanguage.ENGLISH
        
        logger.info(f"Processing text in {mode.value} mode")
        
        # Generate response with mode
        response_text, intent = await llm_service.generate_response(text, lang, mode=mode)
        logger.info(f"Intent detected: {intent.value}")
        
        # Optionally generate audio
        audio_url = None
        try:
            audio_path = await tts_service.synthesize(response_text, lang)
            audio_url = await tts_service.get_audio_url(audio_path)
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
        
        return response_text, lang, audio_url


# Singleton instance
pipeline_service = PipelineService()
