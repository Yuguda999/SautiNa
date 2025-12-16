import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables BEFORE importing config
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.tts_service import tts_service
from config import SupportedLanguage

async def test_yarngpt():
    print("Testing YarnGPT TTS...")
    
    text = "Hello, this is a test of the YarnGPT text to speech service."
    print(f"Text: {text}")
    
    try:
        # Test with English
        print("Synthesizing (English)...")
        output_path = await tts_service.synthesize(text, SupportedLanguage.ENGLISH)
        print(f"✅ Success! Audio saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Ensure output dir exists (usually handled by service init, but good to be safe)
    os.makedirs("temp", exist_ok=True)
    
    asyncio.run(test_yarngpt())
