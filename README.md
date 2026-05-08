# AI Multimedia Q&A Web App

A full-stack app where users can upload PDF/audio/video files, ask questions, generate summaries, and fetch topic-based timestamps for playback.

## Tech Stack

- Backend: Django + Django REST Framework + LangChain/LangGraph
- Frontend: React (Vite)
- AI: OpenAI models + Whisper (local transcription path)
- Vector Search: FAISS
- Database: MySQL (default) or SQLite (dev/CI via `USE_SQLITE=1`)

## Features

- Upload PDF/audio/video files through `POST /api/upload/`
- Store extracted/transcribed text and metadata
- Ask context-aware questions through `POST /api/chat/`
- Generate content summary through `POST /api/summary/`
- Extract topic-specific timestamps through `POST /api/timestamps/`
- Jump playback to relevant timestamp in the frontend

## API Endpoints

- `POST /api/upload/` (multipart)
  - fields: `title`, `file`
- `POST /api/chat/`
  - body: `{ "question": "..." }`
- `POST /api/summary/`
  - no body required
- `POST /api/timestamps/`
  - body: `{ "topic": "..." }`

## Local Setup

### Backend

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`  
Backend URL: `http://127.0.0.1:8000`

## Docker Setup

```bash
docker compose up --build
```

## Testing

Run backend tests:

```bash
set USE_SQLITE=1
python manage.py test
```

## CI

GitHub Actions workflow is configured in `.github/workflows/ci.yml` for:

- Backend dependency install + Django tests
- Frontend install + production build

## Notes

- Set `OPENAI_API_KEY` in your environment or `.env`.
- For production, replace `runserver` with Gunicorn/Uvicorn and harden CORS/host settings.
