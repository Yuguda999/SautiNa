# SautiNa 🇳🇬

**SautiNa** (meaning "My Voice") is a multilingual, voice-first AI assistant designed specifically for Nigerian users. It bridges the digital divide by allowing users to interact with technology in their native languages—**Hausa**, **Yoruba**, **Igbo**, and **Nigerian Pidgin**—as well as English.

## 🚀 Key Features

-   **Voice-First Interaction**: Speak naturally to the assistant and receive audio responses.
-   **Multilingual Support**: Seamlessly switches between English, Hausa, Yoruba, Igbo, and Pidgin.
-   **Powered by N-ATLaS**: Leverages the **N-ATLaS** (Nigerian-Adaptive Transfer Learning and Speech) Large Language Model, fine-tuned for Nigerian languages and cultural context.
-   **YarnGPT TTS**: Utilizes **YarnGPT** for high-quality, natural-sounding text-to-speech in Nigerian accents and languages.
-   **Real-Time Processing**: Fast speech-to-text and text-to-speech pipelines for a conversational experience.

## 🛠️ Technology Stack

-   **Backend**: Python, FastAPI
-   **Frontend**: React, TypeScript, Vite, Tailwind CSS
-   **AI/ML**:
    -   **LLM**: N-ATLaS (hosted on Modal)
    -   **TTS**: YarnGPT API
    -   **STT**: Google Speech Recognition (or similar)

## 📦 Installation

### Prerequisites

-   Python 3.10+
-   Node.js 18+
-   `pip` and `npm`

### Backend Setup

1.  Navigate to the project root:
    ```bash
    cd SautiNa
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  Set up environment variables:
    Create a `backend/.env` file and add your API keys (see `.env.example` if available, or ask the maintainer).
    ```env
    YARNGPT_API_KEY=your_key_here
    NATLAS_API_URL=your_modal_url_here
    ```

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

## 🏃‍♂️ Usage

### Running the Backend

From the project root (with venv activated):

```bash
python backend/main.py
```

The API will be available at `http://localhost:8000`.

### Running the Frontend

From the `frontend` directory:

```bash
npm run dev
```

The application will launch at `http://localhost:5173`.

### How to Use

1.  Open the frontend in your browser.
2.  Select your preferred language.
3.  Click the microphone button and speak.
4.  SautiNa will process your request and respond with both text and audio.

## 📚 Documentation

-   [N-ATLaS Deployment Guide](docs/NATLAS_DEPLOY_GUIDE.md): Learn how to deploy the N-ATLaS model on Modal.
-   [YarnGPT Documentation](docs/YARNGPT_DOCS.md): Details on the Text-to-Speech API and available voices.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

[MIT License](LICENSE)
