/**
 * ChatMessage.tsx
 * Individual chat message bubble component.
 */

import React from 'react';
import { Bot, User } from 'lucide-react';
import type { ChatMessage as IChatMessage } from '../../types';

interface Props {
  message: IChatMessage;
}

const ChatMessage: React.FC<Props> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: isUser ? 'flex-end' : 'flex-start', gap: '4px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: '#6b7280' }}>
        {isUser ? (
          <><span>You</span><User size={14} /></>
        ) : (
          <><Bot size={14} /><span>AI Copilot</span></>
        )}
      </div>
      <div className={`message-bubble ${message.role}`}>
        {message.content}
      </div>
    </div>
  );
};

export default ChatMessage;
