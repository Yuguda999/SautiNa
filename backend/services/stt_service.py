"""
Speech-to-Text Service
Uses OpenAI Whisper for transcribing audio in Nigerian languages.
"""
import whisper
import os
import tempfile
import logging
from typing import Tuple, Optional

from config import settings, SupportedLanguage

logger = logging.getLogger(__name__)


class STTService:
    """Service for speech-to-text using Whisper"""
    
    def __init__(self):
        self.model = None
        self._model_name = settings.whisper_model
    
    def _load_model(self):
        """Lazy load Whisper model"""
        if self.model is None:
            logger.info(f"Loading Whisper model: {self._model_name}")
            self.model = whisper.load_model(self._model_name)
            logger.info("Whisper model loaded successfully")
    
    def _detect_language(self, whisper_lang: str) -> SupportedLanguage:
        """
        Map Whisper detected language to SupportedLanguage.
        Whisper uses ISO 639-1 codes.
        """
        lang_map = {
            "ha": SupportedLanguage.HAUSA,
            "yo": SupportedLanguage.YORUBA,
            "ig": SupportedLanguage.IGBO,
            "en": SupportedLanguage.ENGLISH,
            # Whisper doesn't directly detect Pidgin, so we default to English
        }
        return lang_map.get(whisper_lang, SupportedLanguage.ENGLISH)
    
    async def transcribe(
        self,
        audio_data: bytes,
        filename: str = "audio.wav"
    ) -> Tuple[str, SupportedLanguage]:
        """
        Transcribe audio to text.
        
        Args:
            audio_data: Raw audio bytes
            filename: Original filename (for format detection)
            
        Returns:
            Tuple of (transcribed text, detected language)
        """
        self._load_model()
        
        # Save audio to temp file
        suffix = os.path.splitext(filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name
        
        try:
            logger.info(f"Transcribing audio file: {tmp_path}")
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                tmp_path,
                task="transcribe",
                # Don't specify language - let Whisper auto-detect
            )
            
            text = result["text"].strip()
            detected_lang = result.get("language", "en")
            language = self._detect_language(detected_lang)
            
            logger.info(f"Transcribed: '{text[:100]}...' (detected: {detected_lang})")
            
            return text, language
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    async def transcribe_file(
        self,
        file_path: str
    ) -> Tuple[str, SupportedLanguage]:
        """
        Transcribe audio from file path.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (transcribed text, detected language)
        """
        self._load_model()
        
        try:
            logger.info(f"Transcribing audio file: {file_path}")
            
            result = self.model.transcribe(file_path, task="transcribe")
            
            text = result["text"].strip()
            detected_lang = result.get("language", "en")
            language = self._detect_language(detected_lang)
            
            logger.info(f"Transcribed: '{text[:100]}...' (detected: {detected_lang})")
            
            return text, language
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise


# Singleton instance
stt_service = STTService()
