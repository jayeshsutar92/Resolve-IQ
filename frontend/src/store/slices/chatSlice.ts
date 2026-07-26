/**
 * chatSlice.ts
 * Redux slice managing the chat messages history.
 */

import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { ChatMessage } from '../../types';
import { v4 as uuidv4 } from 'uuid';
import { processChatAction, uploadDocumentAction } from './complaintSlice';

interface ChatState {
  messages: ChatMessage[];
}

const initialState: ChatState = {
  messages: [
    {
      id: uuidv4(),
      role: 'ai',
      content: 'Hello! I am your AI Copilot. How can I help you log a complaint today?',
      timestamp: new Date().toISOString(),
    },
  ],
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addUserMessage: (state, action: PayloadAction<string>) => {
      state.messages.push({
        id: uuidv4(),
        role: 'user',
        content: action.payload,
        timestamp: new Date().toISOString(),
      });
    },
    addAiMessage: (state, action: PayloadAction<string>) => {
      state.messages.push({
        id: uuidv4(),
        role: 'ai',
        content: action.payload,
        timestamp: new Date().toISOString(),
      });
    },
  },
  extraReducers: (builder) => {
    // Automatically add AI's response message when chat processing is successful
    builder.addCase(processChatAction.fulfilled, (state, action) => {
      state.messages.push({
        id: uuidv4(),
        role: 'ai',
        content: action.payload.message,
        timestamp: new Date().toISOString(),
      });
    });

    // Automatically add AI's response message when document upload is successful
    builder.addCase(uploadDocumentAction.fulfilled, (state, action) => {
      state.messages.push({
        id: uuidv4(),
        role: 'ai',
        content: action.payload.message,
        timestamp: new Date().toISOString(),
      });
    });
  },
});

export const { addUserMessage, addAiMessage } = chatSlice.actions;
export default chatSlice.reducer;
