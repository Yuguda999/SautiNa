const API_BASE = 'http://localhost:8000/api';

export type ChatMode = 'chat' | 'learn';

export interface ChatResponse {
    text: string;
    audio_url?: string;
    language: string;
}

export const sendMessage = async (
    text: string,
    language: string = 'en',
    mode: ChatMode = 'chat'
): Promise<ChatResponse> => {
    try {
        const response = await fetch(`${API_BASE}/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                language,
                mode,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

export const sendVoice = async (audioBlob: Blob, language: string = 'en'): Promise<ChatResponse> => {
    const formData = new FormData();
    formData.append('file', audioBlob);
    formData.append('language', language);

    try {
        const response = await fetch(`${API_BASE}/voice`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to send voice');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

export interface TranslateResponse {
    original_text: string;
    translated_text: string;
    source_language: string;
    target_language: string;
}

export const translateText = async (
    text: string,
    sourceLanguage: string,
    targetLanguage: string
): Promise<TranslateResponse> => {
    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                source_language: sourceLanguage,
                target_language: targetLanguage,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to translate');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};
