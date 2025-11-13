# KrishiBondhu - Multi-Provider LLM Support

## Overview

KrishiBondhu now supports multiple LLM providers through a flexible configuration system. Switch between providers by simply changing the `LLM_PROVIDER` value in your `.env` file.

**Supported Providers:**
- ✅ Google Gemini (default)
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic (Claude)
- ✅ Cohere

---

## Quick Start

### Step 1: Update `.env` File

Copy `.env.example` to `.env`:
```bash
cp backend/.env.example backend/.env
```

### Step 2: Choose Your Provider

Edit `backend/.env` and set `LLM_PROVIDER`:

**For Gemini (Default):**
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=models/gemini-2.5-flash
```

**For OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
OPENAI_ORG_ID=  # Optional
```

**For Anthropic (Claude):**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**For Cohere:**
```env
LLM_PROVIDER=cohere
COHERE_API_KEY=your-cohere-api-key-here
COHERE_MODEL=command-r-plus
```

### Step 3: Install Required Dependencies

```bash
cd backend

# For Gemini
pip install google-generativeai

# For OpenAI
pip install openai

# For Anthropic
pip install anthropic

# For Cohere
pip install cohere

# Or install all:
pip install google-generativeai openai anthropic cohere
```

### Step 4: Start Backend

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Configuration Details

### Gemini Configuration

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=models/gemini-2.5-flash

# Available models:
# - models/gemini-2.5-flash (recommended)
# - models/gemini-pro
# - models/gemini-1.5-flash
```

**Get API Key:**
1. Visit https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key to `GEMINI_API_KEY`

---

### OpenAI Configuration

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
OPENAI_ORG_ID=  # Optional

# Available models:
# - gpt-4-turbo (recommended, latest)
# - gpt-4
# - gpt-3.5-turbo (faster, cheaper)
```

**Get API Key:**
1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key to `OPENAI_API_KEY`

**Organization ID (Optional):**
1. Visit https://platform.openai.com/account/org-settings/overview
2. Copy the Organization ID to `OPENAI_ORG_ID`

---

### Anthropic Configuration

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Available models:
# - claude-3-opus-20240229 (most powerful, most expensive)
# - claude-3-sonnet-20240229 (recommended, balanced)
# - claude-3-haiku-20240307 (fastest, cheapest)
```

**Get API Key:**
1. Visit https://console.anthropic.com/keys
2. Click "Create Key"
3. Copy the key to `ANTHROPIC_API_KEY`

---

### Cohere Configuration

```env
LLM_PROVIDER=cohere
COHERE_API_KEY=your-api-key
COHERE_MODEL=command-r-plus

# Available models:
# - command-r-plus (recommended, most powerful)
# - command-r (balanced)
# - command-light (lightweight)
```

**Get API Key:**
1. Visit https://dashboard.cohere.com/api-keys
2. Click "Create Key"
3. Copy the key to `COHERE_API_KEY`

---

## How It Works

### Architecture

```
app/llm/provider.py (LLM Provider Layer)
    ↓
    ├─→ GeminiProvider
    ├─→ OpenAIProvider
    ├─→ AnthropicProvider
    └─→ CohereProvider
    
app/farm_agent/langgraph_app.py (Uses LLM)
    ↓
    Uses get_llm_provider() to get active provider
    ↓
    Calls provider.generate_content(prompt, system_instruction)
    ↓
    Returns response (provider-agnostic)
```

### Code Usage

```python
from app.llm import init_llm_provider

# Initialize LLM provider based on .env
provider = init_llm_provider()

# Use it (same interface for all providers)
system_instruction = "You are a helpful farming assistant..."
prompt = "What's wrong with my rice?"

response = provider.generate_content(
    prompt=prompt,
    system_instruction=system_instruction
)

print(response)
```

### Integrating with Existing Code

The system automatically uses the configured provider. No code changes needed! Just:

1. Set `LLM_PROVIDER` in `.env`
2. Set the corresponding API key
3. Restart backend

The langgraph_app already uses the provider abstraction.

---

## Switching Providers (Easy!)

To switch from Gemini to OpenAI:

**Before:**
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key
```

**After:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
```

**Restart backend** - That's it! ✅

---

## Environment Variables

### All Available Configuration

```env
# Primary selection
LLM_PROVIDER=gemini  # gemini, openai, anthropic, cohere

# Gemini
GEMINI_API_KEY=
GEMINI_MODEL=models/gemini-2.5-flash

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4-turbo
OPENAI_ORG_ID=

# Anthropic
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Cohere
COHERE_API_KEY=
COHERE_MODEL=command-r-plus

# Speech-to-Text
STT_PROVIDER=gemini  # gemini, openai, google_speech

# Text-to-Speech
TTS_PROVIDER=gtts    # gtts, openai, google_speech, elevenlabs
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=

# Other settings
MAX_RETRIES=3
REQUEST_TIMEOUT=30
DEBUG=true
LOG_LEVEL=INFO
```

---

## Testing Different Providers

### Test Gemini
```bash
curl -X POST http://localhost:8000/api/chat \
  -F "message=What is rice leaf scorch?" \
  -F "user_id=test" \
  -F "lat=23.8" \
  -F "lon=90.3"
```

### Test OpenAI (after switching to OpenAI in .env)
```bash
# Same API call - just works! No code change needed
curl -X POST http://localhost:8000/api/chat \
  -F "message=What is rice leaf scorch?" \
  -F "user_id=test" \
  -F "lat=23.8" \
  -F "lon=90.3"
```

Expected: Same type of response, but from different provider ✅

---

## Cost Comparison

| Provider | Model | Cost (1M tokens) | Speed | Quality |
|----------|-------|-----------------|-------|---------|
| Gemini | 2.5-flash | $0.075 input / $0.3 output | Fast | Good |
| OpenAI | GPT-4-turbo | $10 input / $30 output | Moderate | Excellent |
| OpenAI | GPT-3.5-turbo | $0.50 input / $1.50 output | Very Fast | Good |
| Anthropic | Claude 3 Sonnet | $3 input / $15 output | Moderate | Excellent |
| Cohere | Command R+ | $3 input / $15 output | Moderate | Good |

---

## Best Practices

1. **Development:** Use Gemini (free tier available) or GPT-3.5-turbo (cheaper)
2. **Testing:** Keep API keys in `.env.local` (not in git)
3. **Production:** Use `.env` with proper secrets management
4. **Monitoring:** Log which provider is active

```python
from app.llm import get_llm_config
config = get_llm_config()
print(f"Using provider: {config.provider}")
print(f"Model: {config.gemini_model if config.provider == 'gemini' else ...}")
```

---

## Troubleshooting

### Error: "Unknown LLM provider"
```
❌ Check LLM_PROVIDER value in .env is valid
✅ Valid values: gemini, openai, anthropic, cohere
```

### Error: "API_KEY not set"
```
❌ Check corresponding API key is set in .env
✅ E.g., if using OpenAI, OPENAI_API_KEY must be set
```

### Error: "Provider not installed"
```
❌ Install required package
✅ pip install google-generativeai  # for Gemini
✅ pip install openai                 # for OpenAI
✅ pip install anthropic              # for Anthropic
✅ pip install cohere                 # for Cohere
```

### Provider works but responses are weird
```
✅ Check system instructions are being passed correctly
✅ Review logs for provider errors
✅ Try with explicit prompt to debug
```

---

## Adding a New Provider

To add a new provider (e.g., Llama 2, Azure, etc.):

1. Create new provider class in `app/llm/provider.py`:
```python
class LlamaProvider(BaseLLMProvider):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your client
    
    def generate_content(self, prompt, system_instruction=None):
        # Implement generate_content
        pass
    
    def get_model_name(self):
        return self.model
```

2. Add to `get_llm_provider()` factory function

3. Add config to `.env.example`

4. Done! ✅

---

## Security Notes

⚠️ **Never commit `.env` file to git!**

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Keep .env.example for reference
git add .env.example
git commit -m "Add .env.example with all provider configs"
```

---

## Support

For provider-specific issues:
- **Gemini:** https://ai.google.dev/docs
- **OpenAI:** https://platform.openai.com/docs
- **Anthropic:** https://docs.anthropic.com
- **Cohere:** https://docs.cohere.com

---

**Status: ✅ Multi-Provider Support Ready**

Switch LLM providers with a single `.env` change!
