# Backend - Farm Assist

## Setup

1. Create `.env` file with the following variables:
   ```bash
   # Gemini API Key (required)
   GEMINI_API_KEY=AIzaSyDlWQCKSKKtHl1wLQvnb9QaPRUODn8sMQ0
   
   # Database Configuration
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/farmdb
   
   # File Upload Directory
   UPLOAD_DIR=/tmp/uploads
   
   # AWS S3 Configuration (optional)
   S3_BUCKET=
   AWS_ACCESS_KEY_ID=
   AWS_SECRET_ACCESS_KEY=
   
   # OpenAI API Key (optional, kept for fallback)
   OPENAI_API_KEY=
   ```

2. Build & run:
   ```bash
   docker-compose up --build
   ```

3. Run Alembic migrations inside the container:
   ```bash
   docker exec -it farmassist_backend bash
   alembic upgrade head
   ```

## Features

- **Audio Transcription**: Uses Google Gemini API for audio transcription (supports multiple languages including Bengali and English)
- **Intent Extraction**: Uses Gemini to extract structured information (crop, symptoms, need_image) from farmer queries
- **Intelligent Reasoning**: Uses Gemini to generate context-aware responses integrating vision, weather, and transcript data
- **Vision Analysis**: YOLOv8-based disease/pest detection
- **Weather Integration**: Open-Meteo API for weather forecasts
- **Text-to-Speech**: gTTS for generating audio responses in multiple languages
- **Database Persistence**: PostgreSQL with async SQLAlchemy for storing conversations

## API Endpoints

- `POST /api/upload_audio` - Upload audio file and process through LangGraph pipeline
- `GET /api/conversations` - Retrieve stored conversations
- `GET /api/get_tts?path=<tts_path>` - Download generated TTS audio files

## Gemini API Integration

The project uses Google Gemini 1.5 Flash for:
- Audio transcription (multimodal audio input)
- Intent extraction and JSON parsing
- Context-aware response generation
- Multimodal understanding (text + images when available)

The Gemini API key is configured in the `.env` file as `GEMINI_API_KEY`.
