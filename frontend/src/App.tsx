import { useState } from 'react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import VoiceInput from './components/VoiceInput';
import Translator from './components/Translator';
import { sendMessage } from './services/api';

// Define ChatMode inline to avoid import issues
type ChatMode = 'chat' | 'learn';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  audioUrl?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [showTranslator, setShowTranslator] = useState(false);
  const [chatMode, setChatMode] = useState<ChatMode>('chat');

  const handleSend = async (text: string) => {
    // Add user message
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);
    setIsProcessing(true);

    try {
      // Call Backend API with mode
      const response = await sendMessage(text, selectedLanguage, chatMode);

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.text,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        audioUrl: response.audio_url ? `http://localhost:8000${response.audio_url}` : undefined
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I encountered an error processing your request.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setChatMode('chat'); // Reset to chat mode
  };

  const handleToggleLearnMode = () => {
    // Toggle between chat and learn modes
    const newMode = chatMode === 'chat' ? 'learn' : 'chat';
    setChatMode(newMode);
    // Clear messages when switching modes
    setMessages([]);
  };

  return (
    <div className="app-container flex flex-col h-screen max-w-4xl mx-auto bg-bg-secondary shadow-2xl relative overflow-hidden">
      <Header
        onNewChat={handleNewChat}
        onTranslate={() => setShowTranslator(true)}
      />

      <ChatInterface
        messages={messages}
        isThinking={isProcessing}
        selectedLanguage={selectedLanguage}
        onSelectLanguage={setSelectedLanguage}
      />
      <VoiceInput
        onSend={handleSend}
        isProcessing={isProcessing}
        selectedLanguage={selectedLanguage}
        onSelectLanguage={setSelectedLanguage}
        isLearnMode={chatMode === 'learn'}
        onToggleLearnMode={handleToggleLearnMode}
      />

      {/* Translator Modal */}
      {showTranslator && (
        <Translator onClose={() => setShowTranslator(false)} />
      )}
    </div>
  );
}

export default App;
