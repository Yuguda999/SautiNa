"""
SautiNa API Routes
Endpoints for voice and text processing.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import Optional
import logging

from config import settings, SupportedLanguage
from schemas import (
    TextRequest,
    TextResponse,
    VoiceResponse,
    HealthResponse,
    LanguagesResponse,
    TranslateRequest,
    TranslateResponse
)
from services.pipeline_service import pipeline_service
from services.llm_service import llm_service
from services.tts_service import tts_service


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        natlas_endpoint=settings.natlas_api_url
    )


@router.get("/languages", response_model=LanguagesResponse)
async def get_languages():
    """Get list of supported languages"""
    languages = [
        {"code": "ha", "name": "Hausa", "native": "Hausa"},
        {"code": "yo", "name": "Yoruba", "native": "Yorùbá"},
        {"code": "ig", "name": "Igbo", "native": "Igbo"},
        {"code": "pcm", "name": "Nigerian Pidgin", "native": "Pidgin"},
        {"code": "en", "name": "English", "native": "English"},
    ]
    return LanguagesResponse(languages=languages)


@router.post("/text", response_model=TextResponse)
async def process_text(request: TextRequest):
    """
    Process a text message and get an AI response.
    
    Supports two modes:
    - 'chat': Normal conversation mode (default)
    - 'learn': Teacher mode - AI asks questions and teaches interactively
    """
    try:
        logger.info(f"Text request ({request.mode.value} mode): {request.text[:100]}...")
        
        # Use provided language or default
        language = request.language or SupportedLanguage.ENGLISH
        
        # Process through pipeline (LLM + TTS) with mode
        response_text, response_lang, audio_url = await pipeline_service.process_text(
            request.text, language, mode=request.mode
        )
        
        return TextResponse(
            text=response_text,
            detected_language=response_lang,
            audio_url=audio_url
        )
        
    except Exception as e:
        logger.error(f"Text processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice", response_model=VoiceResponse)
async def process_voice(
    audio: UploadFile = File(..., description="Audio file (wav, mp3, ogg, webm)"),
    language: Optional[str] = Form(None, description="Language code (ha, yo, ig, pcm, en)")
):
    """
    Process a voice message through the full pipeline.
    
    1. Transcribes audio to text (STT)
    2. Generates AI response (LLM)
    3. Converts response to speech (TTS)
    
    Returns transcription, response text, and URL to audio response.
    """
    try:
        logger.info(f"Voice request: {audio.filename}")
        
        # Read audio data
        audio_data = await audio.read()
        
        # Parse language if provided
        preferred_language = None
        if language:
            try:
                preferred_language = SupportedLanguage(language)
            except ValueError:
                logger.warning(f"Invalid language code: {language}, using auto-detect")
        
        # Process through full pipeline
        result = await pipeline_service.process_voice(
            audio_data=audio_data,
            filename=audio.filename or "audio.wav",
            preferred_language=preferred_language
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Voice processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text-to-speech")
async def text_to_speech(
    text: str = Form(..., description="Text to convert to speech"),
    language: str = Form("en", description="Language code")
):
    """
    Convert text to speech and return audio file.
    """
    try:
        # Parse language
        try:
            lang = SupportedLanguage(language)
        except ValueError:
            lang = SupportedLanguage.ENGLISH
        
        # Generate audio
        audio_path = await tts_service.synthesize(text, lang)
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="response.mp3"
        )
        
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text between supported Nigerian languages.
    
    Supports translation between Hausa, Yoruba, Igbo, Nigerian Pidgin, and English.
    Uses the N-ATLaS multilingual model for culturally-aware translation.
    """
    try:
        logger.info(f"Translation request: {request.source_language.value} -> {request.target_language.value}")
        
        # Perform translation
        translated_text = await llm_service.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language
        )
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
