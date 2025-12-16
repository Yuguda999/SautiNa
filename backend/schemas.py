"""
SautiNa API Schemas
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from config import SupportedLanguage, ChatMode


class TextRequest(BaseModel):
    """Text input request for chat (useful for testing)"""
    text: str = Field(..., description="User message in any supported language")
    language: Optional[SupportedLanguage] = Field(
        default=None,
        description="Language code (ha, yo, ig, pcm, en). Auto-detected if not provided."
    )
    mode: ChatMode = Field(
        default=ChatMode.CHAT,
        description="Chat mode: 'chat' for normal conversation, 'learn' for interactive teacher mode"
    )


class TextResponse(BaseModel):
    """Text response from the assistant"""
    text: str = Field(..., description="Assistant response text")
    detected_language: SupportedLanguage = Field(..., description="Language used for response")
    audio_url: Optional[str] = Field(None, description="URL to audio response file")


class VoiceResponse(BaseModel):
    """Voice response with audio data"""
    transcribed_text: str = Field(..., description="What the user said (transcribed)")
    response_text: str = Field(..., description="Assistant's text response")
    detected_language: SupportedLanguage = Field(..., description="Detected/used language")
    audio_url: Optional[str] = Field(None, description="URL to audio response file")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    app_name: str
    version: str
    natlas_endpoint: str


class LanguagesResponse(BaseModel):
    """Supported languages response"""
    languages: list[dict] = Field(..., description="List of supported languages")


class TranslateRequest(BaseModel):
    """Translation request between supported languages"""
    text: str = Field(..., description="Text to translate")
    source_language: SupportedLanguage = Field(..., description="Source language code (ha, yo, ig, pcm, en)")
    target_language: SupportedLanguage = Field(..., description="Target language code (ha, yo, ig, pcm, en)")


class TranslateResponse(BaseModel):
    """Translation response"""
    original_text: str = Field(..., description="Original text")
    translated_text: str = Field(..., description="Translated text")
    source_language: SupportedLanguage = Field(..., description="Source language")
    target_language: SupportedLanguage = Field(..., description="Target language")
