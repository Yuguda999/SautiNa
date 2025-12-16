import requests
import json

def verify_audio_response():
    url = "http://localhost:8000/api/text"
    payload = {
        "text": "Hello, how are you?",
        "language": "en"
    }
    
    try:
        print("Sending request to /api/text...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "audio_url" in data and data["audio_url"]:
                print("\n✅ Verification SUCCESS: audio_url is present.")
            else:
                print("\n❌ Verification FAILED: audio_url is missing or empty.")
        else:
            print(f"\n❌ Verification FAILED: API error {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"\n❌ Verification FAILED: {str(e)}")

if __name__ == "__main__":
    verify_audio_response()
