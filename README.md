# AI-Powered Complaint Management System

## Project Overview
The AI-Powered Complaint Management System is an end-to-end full-stack application that leverages natural language processing and Large Language Models to automate customer complaint logging, editing, and risk assessment. It features a modern, responsive two-panel UI where an AI Copilot assists the user in generating structured complaint data directly from natural language input or document uploads.

## Tech Stack
### Frontend
- **React (TypeScript)**: UI Framework
- **Redux Toolkit**: State Management (Single Source of Truth)
- **React Router**: Client-side routing
- **Vite**: Build tool and dev server
- **Vanilla CSS**: Modern styling, glassmorphism, dynamic variables
- **Lucide React**: Beautiful scalable icons

### Backend
- **FastAPI**: Asynchronous web framework for the API
- **PostgreSQL & SQLAlchemy 2.0 (asyncpg)**: Relational database and ORM
- **Alembic**: Database migrations
- **LangGraph & LangChain**: AI Workflow orchestration
- **Groq API (llama-3.1-8b-instant)**: Large Language Model for processing

## Folder Structure
```
AIVOA-task/
├── backend/
│   ├── ai/               # LangGraph workflow, nodes, and LLM configuration
│   ├── api/              # FastAPI routes, dependencies, and exception handlers
│   ├── core/             # Application configuration and environment settings
│   ├── database/         # SQLAlchemy session and engine setup
│   ├── models/           # SQLAlchemy ORM models (Complaint, RiskAssessment)
│   ├── repositories/     # Database CRUD logic
│   ├── schemas/          # Pydantic validation schemas
│   ├── services/         # Business logic bridging APIs and AI Graph
│   ├── utils/            # Shared utilities like structured loggers
│   └── alembic/          # Database migration scripts
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── assets/       # Images, global styles
│   │   ├── components/   # Reusable UI elements (Chat, Form, Upload)
│   │   ├── hooks/        # Custom React hooks
│   │   ├── pages/        # Route-level components
│   │   ├── services/     # Axios API client
│   │   ├── store/        # Redux store and slices
│   │   ├── types/        # TypeScript interfaces
│   │   └── utils/        # Helper functions
│   └── index.html        # Entry HTML
├── README.md             # Project documentation
└── .gitignore            # Git ignore rules
```

## Features
- **Natural Language Complaint Logging**: Describe issues conversationally; the AI extracts relevant data into a structured JSON payload.
- **Context-Aware Editing**: Mention specific updates (e.g., "Actually, the date was yesterday"), and the AI patches only the relevant fields.
- **Document Processing**: Upload complaint PDFs or TXT files to automatically extract and populate the form without manual entry.
- **Dynamic Risk Assessment**: The AI generates a structured severity, priority, and risk level with clear reasoning and recommended actions.
- **Fully Automated Form Population**: The UI auto-populates the complaint form exclusively from AI responses—no manual form filling required.

## Setup Instructions

### Environment Variables
#### Backend (`backend/.env`)
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/aivoa
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=llama-3.1-8b-instant
APP_NAME="AI Complaint Management API"
APP_VERSION="1.0.0"
DEBUG=True
```

#### Frontend (`frontend/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000
```

> **Note on Model Selection**: The assignment specified `gemma2-9b-it` via Groq. Since that model has been decommissioned, the implementation uses a currently supported Groq model (`llama-3.1-8b-instant`) while preserving the same architecture and workflow.

### Running the Backend
1. Navigate to the `backend/` directory.
2. Ensure you have Python 3.10+ installed and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Running the Frontend
1. Navigate to the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Access the UI at the localhost URL provided by Vite.

## Architecture Overview
The system employs a strict separation of concerns:
- **Backend API Layer**: Exposes stateless REST endpoints. 
- **AI Orchestration (LangGraph)**: Uses independent, reusable nodes for intent detection, structured extraction, editing, and risk assessment.
- **Frontend State (Redux)**: Acts as the single source of truth. Form inputs are disabled for the user, ensuring all structured data strictly mirrors the backend's AI outputs.

## API Integration
The frontend utilizes a robust Axios service layer to communicate with the FastAPI backend.
- `POST /api/chat`: Handles conversational logging and context-aware editing.
- `POST /api/upload`: Handles file uploads for automated document extraction.
- `GET /api/complaints`: Retrieves historical complaints.

## AI Workflow
1. **Input**: User sends a natural language message or uploads a document.
2. **Intent Detection**: The AI classifies the action (log, edit, upload).
3. **Extraction**: Natural language is parsed into a strict Pydantic JSON schema.
4. **Risk Assessment**: The structured data is analyzed to assign Severity and Priority scores.
5. **Database Save**: The final payload is persisted to PostgreSQL.
6. **State Update**: The backend returns the joined Complaint object, which updates Redux, instantly reflecting in the UI's Two-Panel view.

## Future Improvements
- Implement User Authentication (JWT) and Role-Based Access Control (RBAC).
- Expand LangGraph to include CAPA (Corrective and Preventive Action) generation.
- Add historical conversation context memory within the Chat API.
- Duplicate complaint detection using vector embeddings and semantic search.
