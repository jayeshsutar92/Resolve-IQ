import React, { useState, useRef, useEffect } from 'react';
import { Send, BotMessageSquare } from 'lucide-react';
import { useAppDispatch, useAppSelector } from '../../hooks/reduxHooks';
import { addUserMessage } from '../../store/slices/chatSlice';
import { processChatAction } from '../../store/slices/complaintSlice';
import ChatMessage from './ChatMessage';
import DocumentUpload from '../DocumentUpload/DocumentUpload';

const ChatPanel: React.FC = () => {
  const dispatch = useAppDispatch();
  const { messages } = useAppSelector((state) => state.chat);
  const { activeComplaint, isLoading } = useAppSelector((state) => state.complaint);
  
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const messageText = input.trim();
    setInput('');
    
    dispatch(addUserMessage(messageText));
    
    dispatch(processChatAction({
      message: messageText,
      complaint_id: activeComplaint?.id
    }));
  };

  return (
    <div className="right-panel">
      <div className="chat-header">
        <BotMessageSquare size={24} color="var(--primary-color)" />
        <h2>AI Copilot</h2>
      </div>
      
      <div className="chat-messages">
        <DocumentUpload />
        
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        
        {isLoading && (
          <div className="message-bubble ai">
            <div className="loading-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            type="text"
            className="chat-input"
            placeholder="Describe the complaint or specify what to edit..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
