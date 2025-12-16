"""
Text-to-Speech Service
Uses YarnGPT API for converting text to natural-sounding Nigerian speech.
"""
import requests
import os
import uuid
import logging
from typing import Optional

from config import settings, SupportedLanguage, LANGUAGE_VOICE_MAP

logger = logging.getLogger(__name__)


class TTSService:
    """Service for text-to-speech using YarnGPT API"""
    
    def __init__(self):
        self.output_dir = settings.temp_dir
        self.api_url = settings.yarngpt_api_url
        self.api_key = settings.yarngpt_api_key
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_voice(self, language: SupportedLanguage) -> str:
        """Get the appropriate YarnGPT voice for the language"""
        return LANGUAGE_VOICE_MAP.get(language, LANGUAGE_VOICE_MAP[SupportedLanguage.ENGLISH])
    
    async def synthesize(
        self,
        text: str,
        language: SupportedLanguage = SupportedLanguage.ENGLISH,
        filename: Optional[str] = None
    ) -> str:
        """
        Convert text to speech using YarnGPT API.
        
        Args:
            text: Text to convert to speech (max 2000 characters)
            language: Language for voice selection
            filename: Optional output filename (without extension)
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Generate unique filename if not provided
            if not filename:
                filename = f"response_{uuid.uuid4().hex[:8]}"
            
            output_path = os.path.join(self.output_dir, f"{filename}.mp3")
            voice = self._get_voice(language)
            
            logger.info(f"Synthesizing speech with YarnGPT voice: {voice}")
            logger.info(f"Text: {text[:100]}...")
            
            # Prepare request to YarnGPT API
            if not self.api_key:
                raise ValueError("YarnGPT API key is not set. Please configure YARNGPT_API_KEY.")
            
            auth_header = self.api_key if self.api_key.startswith("Bearer ") else f"Bearer {self.api_key}"
            
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text[:2000],  # YarnGPT max is 2000 characters
                "voice": voice,
                "response_format": "mp3"
            }
            
            # Make request to YarnGPT API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code != 200:
                error_msg = f"YarnGPT API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data}"
                except:
                    pass
                raise Exception(error_msg)
            
            # Save audio response to file
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Audio saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            raise
    
    async def get_audio_url(self, file_path: str) -> str:
        """
        Get the URL for an audio file.
        
        Args:
            file_path: Full path to audio file
            
        Returns:
            URL path for accessing the audio
        """
        filename = os.path.basename(file_path)
        return f"/audio/{filename}"


# Singleton instance
tts_service = TTSService()
