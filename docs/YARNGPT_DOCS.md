# YarnGPT API Documentation

## 🔐 Authentication

All API requests must be authenticated using a **Bearer token**. You can obtain your personal API key from your Account Page.

Include your API key in the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
```

## 🗣️ Text-to-Speech (TTS)

### Endpoint

**POST** `https://yarngpt.ai/api/v1/tts`

### Request Body (JSON)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `text` | string | Yes | The text to be converted to speech. Max 2000 characters. |
| `voice` | string | No | The voice character to use. Defaults to `'Idera'`. |
| `response_format` | string | No | The audio format. Can be `mp3`, `wav`, `opus`, `flac`. Defaults to `mp3`. |

### 🎙️ Available Voices

Use any of the following names for the `voice` parameter in your request.

| Voice Name | Description |
| :--- | :--- |
| **Idera** | Melodic, gentle. |
| **Emma** | Authoritative, deep. |
| **Zainab** | Soothing, gentle. |
| **Osagie** | Smooth, calm. |
| **Wura** | Young, sweet. |
| **Jude** | Warm, confident. |
| **Chinenye** | Engaging, warm. |
| **Tayo** | Upbeat, energetic. |
| **Regina** | Mature, warm. |
| **Femi** | Rich, reassuring. |
| **Adaora** | Warm, Engaging. |
| **Umar** | Calm, smooth. |
| **Mary** | Energetic, youthful. |
| **Nonso** | Bold, resonant. |
| **Remi** | Melodious, warm. |
| **Adam** | Deep, Clear. |

## 📝 Examples

### Python Example

```python
import requests

API_URL = "https://yarngpt.ai/api/v1/tts"
API_KEY = "YOUR_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "text": "Ólajide sọ pé ó yẹ kí ìjọba tètè dá sí àtúnṣe àwọn òòfísì náà kó tó pẹ́ ju kí ìjàmbá má baà wáyé sí àwọn tó ń ṣiṣẹ́ nínú rẹ̀.",
    "voice": "Idera",
}

response = requests.post(API_URL, headers=headers, json=payload, stream=True)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Audio file saved as output.mp3")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### cURL Example

```bash
curl -X POST https://yarngpt.ai/api/v1/tts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bawo ni gbogbo ile?",
    "voice": "Idera"
  }' \
  --output output.mp3
```