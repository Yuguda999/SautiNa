import React from 'react';

interface MessageBubbleProps {
    role: 'user' | 'assistant';
    content: string;
    audioUrl?: string;
    timestamp: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content, audioUrl, timestamp }) => {
    const isUser = role === 'user';
    const [isPlaying, setIsPlaying] = React.useState(false);
    const audioRef = React.useRef<HTMLAudioElement | null>(null);

    const toggleAudio = () => {
        if (!audioUrl) return;

        if (!audioRef.current) {
            audioRef.current = new Audio(audioUrl);
            audioRef.current.onended = () => setIsPlaying(false);
        }

        if (isPlaying) {
            audioRef.current.pause();
            setIsPlaying(false);
        } else {
            audioRef.current.play().catch(e => console.error("Audio play failed:", e));
            setIsPlaying(true);
        }
    };

    // Cleanup audio on unmount
    React.useEffect(() => {
        return () => {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current = null;
            }
        };
    }, []);

    return (
        <div className={`flex flex-col max-w-[80%] animate-fade-in-up ${isUser ? 'self-end items-end' : 'self-start items-start'}`}>
            <div
                className={`px-6 py-4 rounded-3xl text-base leading-relaxed shadow-sm relative
          ${isUser
                        ? 'bg-gradient-to-br from-primary to-primary-light text-white rounded-br-sm'
                        : 'bg-bg-tertiary border border-white/5 text-text-primary rounded-bl-sm'
                    }`}
            >
                <p>{content}</p>

                {audioUrl && (
                    <div className="mt-3 flex items-center gap-3 bg-black/20 p-2 rounded-xl">
                        <button
                            onClick={toggleAudio}
                            className="w-9 h-9 rounded-full bg-primary hover:bg-primary-light flex items-center justify-center transition-transform hover:scale-110"
                        >
                            {isPlaying ? (
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-white">
                                    <path fillRule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clipRule="evenodd" />
                                </svg>
                            ) : (
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-white">
                                    <path fillRule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clipRule="evenodd" />
                                </svg>
                            )}
                        </button>
                        <div className="flex-1 h-6 flex items-center justify-center gap-1 px-2">
                            {[40, 70, 50, 80, 60, 40].map((height, i) => (
                                <div
                                    key={i}
                                    className={`w-1 bg-primary rounded-sm ${isPlaying ? 'animate-pulse' : ''}`}
                                    style={{ height: `${height}%`, animationDelay: `${i * 0.1}s` }}
                                />
                            ))}
                        </div>
                    </div>
                )}
            </div>
            <span className="text-xs text-text-muted mt-1.5 px-1 opacity-80">
                {timestamp}
            </span>
        </div>
    );
};

export default MessageBubble;
