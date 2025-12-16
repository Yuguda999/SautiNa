import React, { useState } from 'react';
import { translateText } from '../services/api';

const LANGUAGES = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'ha', name: 'Hausa', native: 'Hausa' },
    { code: 'yo', name: 'Yoruba', native: 'Yorùbá' },
    { code: 'ig', name: 'Igbo', native: 'Igbo' },
    { code: 'pcm', name: 'Pidgin', native: 'Pidgin' },
];

interface TranslatorProps {
    onClose: () => void;
}

const Translator: React.FC<TranslatorProps> = ({ onClose }) => {
    const [sourceText, setSourceText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [sourceLanguage, setSourceLanguage] = useState('en');
    const [targetLanguage, setTargetLanguage] = useState('ha');
    const [isTranslating, setIsTranslating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleTranslate = async () => {
        if (!sourceText.trim()) return;

        setIsTranslating(true);
        setError(null);

        try {
            const result = await translateText(sourceText, sourceLanguage, targetLanguage);
            setTranslatedText(result.translated_text);
        } catch (err) {
            setError('Translation failed. Please try again.');
            console.error(err);
        } finally {
            setIsTranslating(false);
        }
    };

    const handleSwapLanguages = () => {
        setSourceLanguage(targetLanguage);
        setTargetLanguage(sourceLanguage);
        setSourceText(translatedText);
        setTranslatedText(sourceText);
    };

    const handleCopyTranslation = () => {
        navigator.clipboard.writeText(translatedText);
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-bg-secondary border border-white/10 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden">
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-bg-glass">
                    <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-primary">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
                        </svg>
                        Translate
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-white/10 text-text-secondary hover:text-text-primary transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Language Selectors */}
                <div className="flex items-center justify-center gap-4 px-6 py-4 bg-bg-tertiary/50">
                    <select
                        value={sourceLanguage}
                        onChange={(e) => setSourceLanguage(e.target.value)}
                        className="flex-1 px-4 py-2 rounded-xl bg-bg-tertiary border border-white/10 text-text-primary focus:outline-none focus:border-primary transition-colors"
                    >
                        {LANGUAGES.map((lang) => (
                            <option key={lang.code} value={lang.code}>
                                {lang.native}
                            </option>
                        ))}
                    </select>

                    <button
                        onClick={handleSwapLanguages}
                        className="p-2 rounded-full bg-primary/20 text-primary hover:bg-primary/30 transition-colors"
                        title="Swap languages"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                        </svg>
                    </button>

                    <select
                        value={targetLanguage}
                        onChange={(e) => setTargetLanguage(e.target.value)}
                        className="flex-1 px-4 py-2 rounded-xl bg-bg-tertiary border border-white/10 text-text-primary focus:outline-none focus:border-primary transition-colors"
                    >
                        {LANGUAGES.map((lang) => (
                            <option key={lang.code} value={lang.code}>
                                {lang.native}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Text Areas */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-px bg-white/5">
                    {/* Source Text */}
                    <div className="bg-bg-secondary p-4">
                        <textarea
                            value={sourceText}
                            onChange={(e) => setSourceText(e.target.value)}
                            placeholder="Enter text to translate..."
                            className="w-full h-40 px-4 py-3 rounded-xl bg-bg-tertiary border border-white/10 text-text-primary placeholder-text-muted resize-none focus:outline-none focus:border-primary transition-colors"
                        />
                    </div>

                    {/* Translated Text */}
                    <div className="bg-bg-secondary p-4 relative">
                        <div className="w-full h-40 px-4 py-3 rounded-xl bg-bg-tertiary/50 border border-white/10 text-text-primary overflow-y-auto">
                            {isTranslating ? (
                                <div className="flex items-center gap-2 text-text-secondary">
                                    <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                                    Translating...
                                </div>
                            ) : translatedText ? (
                                <p>{translatedText}</p>
                            ) : (
                                <p className="text-text-muted">Translation will appear here...</p>
                            )}
                        </div>

                        {translatedText && !isTranslating && (
                            <button
                                onClick={handleCopyTranslation}
                                className="absolute bottom-6 right-6 p-2 rounded-lg bg-white/5 hover:bg-white/10 text-text-secondary hover:text-primary transition-colors"
                                title="Copy translation"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                                </svg>
                            </button>
                        )}
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="px-6 py-3 bg-red-500/10 border-t border-red-500/20 text-red-400 text-sm">
                        {error}
                    </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-white/10 bg-bg-glass">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 rounded-xl text-text-secondary hover:text-text-primary hover:bg-white/5 transition-colors"
                    >
                        Close
                    </button>
                    <button
                        onClick={handleTranslate}
                        disabled={!sourceText.trim() || isTranslating}
                        className="px-6 py-2 rounded-xl bg-gradient-to-r from-primary to-primary-light text-white font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                    >
                        {isTranslating ? (
                            <>
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                Translating...
                            </>
                        ) : (
                            <>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
                                </svg>
                                Translate
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Translator;
