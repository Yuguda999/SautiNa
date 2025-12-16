import asyncio
import websockets
import json
import os
import sys
from dotenv import load_dotenv

# Load .env from backend directory
backend_dir = os.path.join(os.getcwd(), "backend")
load_dotenv(os.path.join(backend_dir, ".env"))

# Add backend to path
sys.path.append(backend_dir)

from services.tts_service import tts_service
from config import SupportedLanguage

async def verify_stt():
    print("1. Generating test audio...")
    test_text = "Hello world, this is a test of the real-time transcription system."
    audio_path = await tts_service.synthesize(test_text, SupportedLanguage.ENGLISH)
    print(f"   Audio generated at: {audio_path}")

    print("\n2. Connecting to WebSocket...")
    uri = "ws://localhost:8000/api/ws/transcribe"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("   Connected!")
            
            # Read audio file
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            
            # Send in chunks
            chunk_size = 4096
            total_sent = 0
            print(f"\n3. Sending audio ({len(audio_data)} bytes)...")
            
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i+chunk_size]
                await websocket.send(chunk)
                total_sent += len(chunk)
                # Simulate real-time (wait a bit)
                await asyncio.sleep(0.1)
            
            print(f"   Sent {total_sent} bytes.")
            
            # Wait for responses until we get the full text or timeout
            print("\n4. Waiting for transcription...")
            start_time = asyncio.get_event_loop().time()
            full_transcription = ""
            
            while asyncio.get_event_loop().time() - start_time < 15.0:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    text = data.get("text", "")
                    print(f"   Received update: {text}")
                    
                    if len(text) > len(full_transcription):
                        full_transcription = text
                    
                    if "test of the real" in full_transcription.lower():
                        print(f"\n   Original: {test_text}")
                        print(f"   Final Transcribed: {full_transcription}")
                        print("\n✅ Verification SUCCESS: Transcription contains expected keywords.")
                        return
                        
                except asyncio.TimeoutError:
                    # No new message for 1 second, continue waiting if total time < 15s
                    continue
                except Exception as e:
                    print(f"   Error receiving: {e}")
                    break
            
            print(f"\n   Original: {test_text}")
            print(f"   Final Transcribed: {full_transcription}")
            print("\n❌ Verification FAILED: Transcription incomplete or mismatch.")
                
    except Exception as e:
        print(f"\n❌ Verification FAILED: {str(e)}")
        # If connection refused, maybe server isn't running
        print("   (Make sure the backend server is running on port 8000)")

if __name__ == "__main__":
    asyncio.run(verify_stt())
