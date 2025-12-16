import React, { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    audioUrl?: string;
}

interface ChatInterfaceProps {
    messages: Message[];
    isThinking: boolean;
    selectedLanguage: string;
    onSelectLanguage: (lang: string) => void;
}

const LANGUAGES = [
    { code: 'en', label: 'English' },
    { code: 'ha', label: 'Hausa' },
    { code: 'yo', label: 'Yoruba' },
    { code: 'ig', label: 'Igbo' },
    { code: 'pcm', label: 'Pidgin' },
];

const ChatInterface: React.FC<ChatInterfaceProps> = ({ messages, isThinking, selectedLanguage, onSelectLanguage }) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isThinking]);

    return (
        <div className="flex-1 overflow-y-auto p-8 flex flex-col gap-6 scroll-smooth">
            {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full gap-6 animate-fade-in text-center py-12">
                    <div className="text-7xl animate-float drop-shadow-xl">🇳🇬</div>
                    <div>
                        <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-green-200 bg-clip-text text-transparent mb-2">
                            SautiNa
                        </h2>
                        <p className="text-text-secondary text-lg max-w-xs mx-auto">
                            Your Nigerian Voice AI Assistant. Speak freely in English, Hausa, Yoruba, Igbo, or Pidgin.
                        </p>
                    </div>
                    <div className="flex flex-wrap justify-center gap-3 mt-4">
                        {LANGUAGES.map((lang) => (
                            <button
                                key={lang.code}
                                onClick={() => onSelectLanguage(lang.code)}
                                className={`px-4 py-2 rounded-full border text-sm transition-all ${selectedLanguage === lang.code
                                        ? 'bg-primary text-white border-primary shadow-glow'
                                        : 'bg-white/5 border-white/10 text-text-secondary hover:bg-white/10 hover:border-primary hover:text-primary-light'
                                    }`}
                            >
                                {lang.label}
                            </button>
                        ))}
                    </div>
                </div>
            ) : (
                <>
                    {messages.map((msg) => (
                        <MessageBubble
                            key={msg.id}
                            role={msg.role}
                            content={msg.content}
                            timestamp={msg.timestamp}
                            audioUrl={msg.audioUrl}
                        />
                    ))}

                    {isThinking && (
                        <div className="self-start items-start animate-fade-in-up">
                            <div className="bg-bg-tertiary border border-white/5 text-text-primary px-6 py-4 rounded-3xl rounded-bl-sm shadow-sm flex items-center gap-2">
                                <span className="text-sm text-text-muted">Thinking</span>
                                <div className="flex gap-1">
                                    <div className="w-1.5 h-1.5 bg-text-muted rounded-full animate-bounce [animation-delay:-0.32s]" />
                                    <div className="w-1.5 h-1.5 bg-text-muted rounded-full animate-bounce [animation-delay:-0.16s]" />
                                    <div className="w-1.5 h-1.5 bg-text-muted rounded-full animate-bounce" />
                                </div>
                            </div>
                        </div>
                    )}
                </>
            )}
            <div ref={messagesEndRef} />
        </div>
    );
};

export default ChatInterface;
