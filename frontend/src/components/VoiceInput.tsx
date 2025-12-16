import React, { useState } from 'react';

interface VoiceInputProps {
    onSend: (text: string) => void;
    isProcessing: boolean;
    selectedLanguage: string;
    onSelectLanguage: (lang: string) => void;
    isLearnMode: boolean;
    onToggleLearnMode: () => void;
}

const LANGUAGES = [
    { code: 'en', label: 'English', flag: '🇬🇧' },
    { code: 'ha', label: 'Hausa', flag: '🇳🇬' },
    { code: 'yo', label: 'Yoruba', flag: '🇳🇬' },
    { code: 'ig', label: 'Igbo', flag: '🇳🇬' },
    { code: 'pcm', label: 'Pidgin', flag: '🇳🇬' },
];

// Add type definitions for Web Speech API
declare global {
    interface Window {
        SpeechRecognition: any;
        webkitSpeechRecognition: any;
    }
}

const VoiceInput: React.FC<VoiceInputProps> = ({ onSend, isProcessing, selectedLanguage, onSelectLanguage, isLearnMode, onToggleLearnMode }) => {
    const [inputText, setInputText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [recognition, setRecognition] = useState<any>(null);

    // Map app languages to browser locales
    const getBrowserLocale = (langCode: string) => {
        switch (langCode) {
            case 'ha': return 'ha-NG';
            case 'yo': return 'yo-NG';
            case 'ig': return 'ig-NG';
            case 'pcm': return 'en-NG';
            case 'en': return 'en-NG';
            default: return 'en-US';
        }
    };

    const handleSend = () => {
        if (inputText.trim()) {
            onSend(inputText);
            setInputText('');
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const startRecording = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert('Your browser does not support speech recognition. Please try Chrome.');
            return;
        }

        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = getBrowserLocale(selectedLanguage);

        recognitionInstance.onstart = () => {
            setIsRecording(true);
        };

        recognitionInstance.onresult = (event: any) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript) {
                setInputText(prev => {
                    const prefix = prev.trim() ? prev + ' ' : '';
                    return prefix + finalTranscript;
                });
            }
        };

        recognitionInstance.onerror = (event: any) => {
            console.error('Speech recognition error', event.error);
            stopRecording();
        };

        recognitionInstance.onend = () => {
            setIsRecording(false);
        };

        recognitionInstance.start();
        setRecognition(recognitionInstance);
    };

    const stopRecording = () => {
        if (recognition) {
            recognition.stop();
            setRecognition(null);
        }
        setIsRecording(false);
    };

    const toggleRecording = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const currentLang = LANGUAGES.find(l => l.code === selectedLanguage) || LANGUAGES[0];

    return (
        <div className="p-4 bg-transparent relative">
            {isRecording && (
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 flex items-center gap-2 px-3 py-1.5 bg-error/15 border border-error/20 rounded-full text-error text-xs font-medium backdrop-blur-md">
                    <div className="w-2 h-2 bg-error rounded-full animate-pulse" />
                    Listening...
                </div>
            )}

            <div className={`flex items-center gap-2 bg-bg-tertiary border border-white/10 rounded-xl p-2 transition-all ${isRecording ? 'border-error/50' : 'focus-within:border-primary/50'}`}>

                {/* + Menu Button */}
                <div className="relative">
                    <button
                        onClick={() => setShowMenu(!showMenu)}
                        className="w-10 h-10 rounded-lg flex items-center justify-center bg-bg-card border border-white/10 text-text-secondary hover:bg-white/5 hover:text-primary transition-all"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className={`w-5 h-5 transition-transform ${showMenu ? 'rotate-45' : ''}`}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    </button>

                    {/* Dropdown Menu */}
                    {showMenu && (
                        <div className="absolute bottom-full left-0 mb-2 w-48 bg-bg-tertiary border border-white/10 rounded-xl shadow-xl overflow-hidden backdrop-blur-xl z-20">
                            {/* Learn Mode Toggle */}
                            <button
                                onClick={() => {
                                    onToggleLearnMode();
                                    setShowMenu(false);
                                }}
                                className={`w-full px-4 py-3 text-left text-sm flex items-center gap-3 hover:bg-white/5 transition-colors ${isLearnMode ? 'text-amber-400 bg-amber-500/10' : 'text-text-secondary'}`}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                                </svg>
                                <span>{isLearnMode ? '✓ Learn Mode On' : 'Learn Mode'}</span>
                            </button>

                            <div className="border-t border-white/10" />

                            {/* Language Options */}
                            <div className="py-1">
                                <div className="px-4 py-2 text-xs text-text-muted uppercase tracking-wide">Language</div>
                                {LANGUAGES.map((lang) => (
                                    <button
                                        key={lang.code}
                                        onClick={() => {
                                            onSelectLanguage(lang.code);
                                            setShowMenu(false);
                                        }}
                                        className={`w-full px-4 py-2.5 text-left text-sm flex items-center gap-3 hover:bg-white/5 transition-colors ${selectedLanguage === lang.code ? 'text-primary bg-primary/5' : 'text-text-secondary'}`}
                                    >
                                        <span>{lang.flag}</span>
                                        <span>{lang.label}</span>
                                        {selectedLanguage === lang.code && <span className="ml-auto text-primary">✓</span>}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Text Input */}
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask anything..."
                    className="flex-1 bg-transparent border-none text-text-primary text-base placeholder:text-text-muted focus:outline-none py-2"
                    disabled={isProcessing}
                />

                {/* Right side icons */}
                <div className="flex items-center gap-1">
                    {/* Learn mode indicator */}
                    {isLearnMode && (
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-amber-500/20 text-amber-400" title="Learn Mode Active">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                            </svg>
                        </div>
                    )}

                    {/* Language indicator */}
                    <div className="px-2 h-8 rounded-lg flex items-center justify-center bg-primary/20 text-primary text-xs font-medium" title={currentLang.label}>
                        {currentLang.label}
                    </div>

                    {/* Mic Button */}
                    <button
                        onClick={toggleRecording}
                        className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all ${isRecording ? 'bg-error text-white animate-pulse' : 'text-text-secondary hover:bg-white/5 hover:text-primary'}`}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                            <path d="M8.25 4.5a3.75 3.75 0 117.5 0v8.25a3.75 3.75 0 11-7.5 0V4.5z" />
                            <path d="M6 10.5a.75.75 0 01.75.75v1.5a5.25 5.25 0 1010.5 0v-1.5a.75.75 0 011.5 0v1.5a6.751 6.751 0 01-6 6.709v2.291h3a.75.75 0 010 1.5h-7.5a.75.75 0 010-1.5h3v-2.291a6.751 6.751 0 01-6-6.709v-1.5A.75.75 0 016 10.5z" />
                        </svg>
                    </button>

                    {/* Send Button */}
                    <button
                        onClick={handleSend}
                        disabled={!inputText.trim() || isProcessing}
                        className={`w-10 h-10 rounded-lg bg-primary text-white flex items-center justify-center transition-all ${!inputText.trim() || isProcessing ? 'opacity-40 cursor-not-allowed' : 'hover:bg-primary-light'}`}
                    >
                        {isProcessing ? (
                            <div className="flex gap-0.5">
                                <div className="w-1 h-1 bg-white rounded-full animate-bounce [animation-delay:-0.32s]" />
                                <div className="w-1 h-1 bg-white rounded-full animate-bounce [animation-delay:-0.16s]" />
                                <div className="w-1 h-1 bg-white rounded-full animate-bounce" />
                            </div>
                        ) : (
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                                <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                            </svg>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VoiceInput;
