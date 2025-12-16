import React from 'react';

interface HeaderProps {
    onNewChat: () => void;
    onTranslate: () => void;
}

const Header: React.FC<HeaderProps> = ({ onNewChat, onTranslate }) => {
    return (
        <header className="flex items-center justify-between px-4 py-3 bg-bg-glass border-b border-white/5 backdrop-blur-xl z-10 sticky top-0">
            <div className="flex items-center relative">
                {/* Small white circle behind the speech bubble icon */}
                <div className="absolute left-[22px] top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-white" />
                <img
                    src="/logo.png"
                    alt="SautiNa Logo"
                    className="w-32 h-auto object-contain relative z-10"
                />
            </div>
            <div className="flex items-center gap-2">
                <button
                    onClick={onTranslate}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary/10 border border-primary/30 text-primary hover:bg-primary/20 hover:border-primary transition-all duration-200"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
                    </svg>
                    <span className="text-xs font-medium">Translate</span>
                </button>
                <button
                    onClick={onNewChat}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-text-secondary hover:bg-white/10 hover:text-primary hover:border-primary transition-all duration-200"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>
                    <span className="text-xs font-medium">New</span>
                </button>
            </div>
        </header>
    );
};

export default Header;
