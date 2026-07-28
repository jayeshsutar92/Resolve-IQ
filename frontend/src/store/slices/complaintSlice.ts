import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { Complaint, ChatRequest } from '../../types';
import { apiService } from '../../services/api';

interface ComplaintState {
  activeComplaint: Complaint | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: ComplaintState = {
  activeComplaint: null,
  isLoading: false,
  error: null,
};

export const processChatAction = createAsyncThunk(
  'complaint/processChat',
  async (request: ChatRequest, { rejectWithValue }) => {
    try {
      const response = await apiService.processChat(request);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'An error occurred while processing chat.');
    }
  }
);

export const uploadDocumentAction = createAsyncThunk(
  'complaint/uploadDocument',
  async (file: File, { rejectWithValue }) => {
    try {
      const response = await apiService.uploadDocument(file);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'An error occurred while uploading document.');
    }
  }
);

const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    clearActiveComplaint: (state) => {
      state.activeComplaint = null;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(processChatAction.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(processChatAction.fulfilled, (state, action) => {
      state.isLoading = false;
      if (action.payload.complaint) {
        state.activeComplaint = action.payload.complaint;
      }
    });
    builder.addCase(processChatAction.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(uploadDocumentAction.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(uploadDocumentAction.fulfilled, (state, action) => {
      state.isLoading = false;
      if (action.payload.complaint) {
        state.activeComplaint = action.payload.complaint;
      }
    });
    builder.addCase(uploadDocumentAction.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });
  },
});

export const { clearActiveComplaint } = complaintSlice.actions;
export default complaintSlice.reducer;
