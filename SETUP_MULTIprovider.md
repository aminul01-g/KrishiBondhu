# KrishiBondhu Multi-Provider LLM Setup Guide

## 🎯 Quick Setup (5 minutes)

### Option 1: Using Gemini (Default, Free)

```bash
# 1. Get API key from https://aistudio.google.com/apikey

# 2. Create .env file
cd backend
cp .env.example .env

# 3. Edit .env
nano .env
# Set:
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=your-key-here

# 4. Install dependencies
pip install google-generativeai

# 5. Start backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Using OpenAI

```bash
# 1. Get API key from https://platform.openai.com/api-keys

# 2. Create .env file
cd backend
cp .env.example .env

# 3. Edit .env
nano .env
# Set:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4-turbo  (or gpt-3.5-turbo for cheaper)

# 4. Install dependencies
pip install openai

# 5. Start backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Anthropic Claude

```bash
# 1. Get API key from https://console.anthropic.com/keys

# 2. Create .env file
cd backend
cp .env.example .env

# 3. Edit .env
nano .env
# Set:
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your-key-here

# 4. Install dependencies
pip install anthropic

# 5. Start backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔧 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/aminul01-g/KrishiBondhu.git
cd KrishiBondhu
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Base Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Install Provider-Specific Dependencies

**For Gemini only:**
```bash
pip install google-generativeai
```

**For OpenAI only:**
```bash
pip install openai
```

**For Anthropic only:**
```bash
pip install anthropic
```

**For Cohere only:**
```bash
pip install cohere
```

**For All Providers:**
```bash
pip install -r requirements-all.txt
```

### Step 5: Setup Environment

```bash
cp .env.example .env
nano .env  # Edit with your API keys
```

---

## 📋 Environment Configuration

### Minimal Configuration (Gemini)

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/krishibondhu
UPLOAD_DIR=/tmp/uploads
```

### Full Configuration (All Providers)

```env
# Choose one
LLM_PROVIDER=gemini

# Gemini
GEMINI_API_KEY=your-key
GEMINI_MODEL=models/gemini-2.5-flash

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
OPENAI_ORG_ID=

# Anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Cohere
COHERE_API_KEY=your-key
COHERE_MODEL=command-r-plus

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/krishibondhu

# Upload
UPLOAD_DIR=/tmp/uploads

# Settings
DEBUG=true
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

---

## 🚀 Running the Application

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Frontend
```bash
cd frontend
npm install
npm run dev
```

Then visit: **http://localhost:5173**

---

## 🧪 Testing

### Test with Your Chosen Provider

```bash
# Test API
curl -X POST http://localhost:8000/api/chat \
  -F "message=What is rice leaf scorch disease?" \
  -F "user_id=test" \
  -F "lat=23.8103" \
  -F "lon=90.3563"

# Should work regardless of which provider is configured!
```

### Check Which Provider Is Active

```python
from app.llm import get_llm_config
config = get_llm_config()
print(f"Provider: {config.provider}")
print(f"Model: {config.gemini_model}")  # or openai_model, anthropic_model, etc.
```

---

## 💰 Cost Estimates

### Monthly Usage (100k API calls)

| Provider | Model | Cost |
|----------|-------|------|
| Gemini | 2.5-flash | ~$3-5 |
| OpenAI | GPT-3.5-turbo | ~$20-30 |
| OpenAI | GPT-4-turbo | ~$200-300 |
| Anthropic | Claude 3 Sonnet | ~$100-150 |

**Recommendation:** Use Gemini for development/testing, GPT-3.5 or Claude for production if needed.

---

## 🔄 Switching Providers

Super easy - no code changes needed!

```bash
# Currently using Gemini?
nano .env
# Change to:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...

# Restart backend
# ctrl+c to stop
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Done! System now uses OpenAI ✅
```

---

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'google'"
```bash
pip install google-generativeai
```

### Error: "API Key not found"
```
Check .env file has correct key name:
- GEMINI_API_KEY (for Gemini)
- OPENAI_API_KEY (for OpenAI)
- ANTHROPIC_API_KEY (for Anthropic)
- COHERE_API_KEY (for Cohere)
```

### Error: "LLM_PROVIDER not set"
```
Add to .env:
LLM_PROVIDER=gemini  # or your chosen provider
```

### Backend not responding
```bash
# Check if backend is running
curl http://localhost:8000/api/conversations

# Restart backend with reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📚 Documentation

- **LLM_PROVIDER_GUIDE.md** - Detailed provider documentation
- **FIXES_FINAL_REPORT.md** - Critical fixes applied
- **CODE_CHANGES_DETAILED.md** - Code changes detail

---

## 🎓 Learning Resources

### Provider Documentation
- **Gemini:** https://ai.google.dev
- **OpenAI:** https://platform.openai.com/docs
- **Anthropic:** https://docs.anthropic.com
- **Cohere:** https://docs.cohere.com

### API Costs
- **Gemini:** https://ai.google.dev/pricing
- **OpenAI:** https://openai.com/pricing
- **Anthropic:** https://www.anthropic.com/pricing
- **Cohere:** https://cohere.com/pricing

---

## ✅ Verification Checklist

- [ ] Git cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file created with API key
- [ ] Database configured (if using)
- [ ] Backend started on port 8000
- [ ] Frontend started on port 5173
- [ ] API responds to test query
- [ ] Responses generated correctly

---

## 🆘 Getting Help

If issues persist:

1. Check `.env` file is correct
2. Verify API key is valid at provider's website
3. Check backend logs: `tail -f /tmp/backend.log`
4. Try with Gemini (free, most reliable)
5. Check requirements: `pip list | grep -E "google|openai|anthropic|cohere"`

---

**Status: ✅ Ready for Production**

You can now:
- ✅ Use any LLM provider
- ✅ Switch providers with `.env` change
- ✅ No code modifications needed
- ✅ Scale with your preferred provider

Enjoy! 🎉
