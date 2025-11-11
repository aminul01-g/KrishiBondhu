# 🚀 Running FarmerAI Project - Complete Guide

## ✅ Current Status

All services are **RUNNING** and ready to use!

### Services Status

| Service | Status | URL | Port |
|---------|--------|-----|------|
| **PostgreSQL Database** | ✅ Running | - | 5432 |
| **Backend API (FastAPI)** | ✅ Running | http://localhost:8000 | 8000 |
| **Frontend (React + Vite)** | ✅ Running | http://localhost:5173 | 5173 |

---

## 🎯 Quick Start

### 1. Access the Application

**Open your browser and navigate to:**
```
http://localhost:5173
```

You should see the **FarmerAI Assistant** interface with:
- Modern, professional UI
- Voice recording section
- Conversation history panel

### 2. Test Voice Recording

1. **Click "Start Recording"** button
   - Grant microphone permission if prompted
   - You'll see a pulsing red indicator while recording

2. **Speak your question** in Bengali or English:
   - Example: "My rice crop has yellow leaves, what should I do?"
   - Example: "আমার ধানের পাতায় হলুদ দাগ, কি করব?" (Bengali)

3. **Click "Stop"** when finished
   - The system will process your query
   - You'll see a loading indicator

4. **View the response:**
   - Your transcript will appear
   - AI response will be displayed
   - Audio response will play automatically
   - All metadata (crop, weather, etc.) will be shown

### 3. View Conversation History

- All conversations are automatically saved
- History panel shows all previous queries
- Click "Refresh" to manually update
- Each conversation shows:
  - Transcript
  - AI Response
  - Detected Crop
  - Language
  - Vision Analysis (if image provided)
  - Weather Information
  - GPS Location

---

## 🔧 Service Management

### Start All Services

If services are not running, start them:

#### 1. Start PostgreSQL (Docker)
```bash
cd /home/aminul/Documents/FarmerAI/backend
docker compose -f docker-compose.yml up -d postgres
```

#### 2. Start Backend API
```bash
cd /home/aminul/Documents/FarmerAI/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3. Start Frontend
```bash
cd /home/aminul/Documents/FarmerAI/frontend
npm run dev
```

### Stop Services

#### Stop Backend
Press `Ctrl+C` in the terminal running uvicorn

#### Stop Frontend
Press `Ctrl+C` in the terminal running vite

#### Stop PostgreSQL
```bash
docker compose -f backend/docker-compose.yml stop postgres
```

---

## 🧪 Testing the System

### Test Backend API

#### 1. Check API Health
```bash
curl http://localhost:8000/api/conversations
```

#### 2. View API Documentation
Open in browser: http://localhost:8000/docs

#### 3. Test Audio Upload (using curl)
```bash
# Record audio first, then:
curl -X POST "http://localhost:8000/api/upload_audio" \
  -F "file=@/path/to/audio.webm" \
  -F "user_id=test_user" \
  -F "lat=23.7" \
  -F "lon=90.4"
```

### Test Frontend

1. **Open Browser Console** (F12)
   - Check for any errors
   - Monitor network requests

2. **Test Voice Recording**
   - Click Start → Speak → Click Stop
   - Verify audio is uploaded
   - Check response appears

3. **Test GPS Detection**
   - Check if location is detected automatically
   - Verify coordinates appear in response

4. **Test Conversation History**
   - Record a query
   - Verify it appears in history
   - Check all metadata is displayed

---

## 📋 API Endpoints

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload_audio` | Upload audio and process through LangGraph |
| `GET` | `/api/conversations` | Get all stored conversations |
| `GET` | `/api/get_tts?path=<path>` | Download generated TTS audio |
| `GET` | `/docs` | Interactive API documentation (Swagger) |

### Example API Response

```json
{
  "transcript": "My rice crop has yellow leaves",
  "reply_text": "Yellow leaves in rice can indicate...",
  "crop": "rice",
  "language": "en",
  "vision_result": {
    "disease": "pest_or_damage_detected",
    "confidence": 0.85
  },
  "weather_forecast": {
    "hourly": {
      "temperature_2m": [28.5]
    }
  },
  "tts_path": "/tmp/tts_audio.mp3"
}
```

---

## 🐛 Troubleshooting

### Backend Issues

#### Problem: Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Check Python environment
cd backend
source venv/bin/activate
python --version

# Check dependencies
pip list | grep -E "fastapi|uvicorn"
```

#### Problem: Database connection error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check .env file
cat backend/.env | grep DATABASE_URL

# Test database connection
docker exec -it farmassist_postgres psql -U postgres -d farmdb -c "SELECT 1;"
```

#### Problem: Import errors
```bash
# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

#### Problem: Frontend won't start
```bash
# Check if port 5173 is in use
lsof -i :5173

# Clear node_modules and reinstall
cd frontend
rm -rf node_modules
npm install
npm run dev
```

#### Problem: CORS errors
- Backend CORS is configured to allow all origins
- Check backend is running on port 8000
- Verify API_BASE in frontend components

#### Problem: Audio recording fails
- Check browser permissions (microphone access)
- Use HTTPS or localhost (required for MediaRecorder)
- Check browser console for errors

### Database Issues

#### Problem: Migrations not applied
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

#### Problem: Database connection refused
```bash
# Restart PostgreSQL
docker compose -f backend/docker-compose.yml restart postgres

# Check logs
docker logs farmassist_postgres
```

---

## 📊 System Requirements

### Backend
- Python 3.12+
- PostgreSQL 15
- 2GB+ RAM
- Internet connection (for Gemini API)

### Frontend
- Modern browser (Chrome, Firefox, Safari, Edge)
- Microphone access
- GPS access (optional, for location)

---

## 🔐 Environment Variables

Ensure `.env` file in `backend/` directory has:

```bash
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/farmdb
UPLOAD_DIR=/tmp/uploads
```

---

## 📝 Logs

### Backend Logs
- Check terminal running uvicorn
- Logs show API requests and processing

### Frontend Logs
- Check browser console (F12)
- Network tab shows API calls

### Database Logs
```bash
docker logs farmassist_postgres
```

---

## ✅ Verification Checklist

- [ ] PostgreSQL container is running
- [ ] Backend API responds at http://localhost:8000
- [ ] Frontend loads at http://localhost:5173
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can record audio in browser
- [ ] GPS location is detected
- [ ] Audio uploads successfully
- [ ] Response appears with all metadata
- [ ] Conversation history displays
- [ ] TTS audio plays

---

## 🎉 Success!

If all services are running and you can:
- ✅ Record audio
- ✅ See responses
- ✅ View conversation history

**The project is running properly!** 🚀

---

## 📞 Next Steps

1. **Test with real queries** - Try different farming questions
2. **Monitor performance** - Check response times
3. **Review conversations** - Check stored data in database
4. **Customize** - Adjust UI or add features as needed

---

**Happy Farming with AI! 🌾🤖**

