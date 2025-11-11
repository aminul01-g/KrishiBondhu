# Gemini API Quota and Billing Setup

## Current Status

The Gemini API key is integrated and working, but you may encounter quota limitations. This document explains how to set up billing and manage quotas.

## API Quota Error

If you see this error:
```
429 You exceeded your current quota, please check your plan and billing details.
```

This means:
- ✅ The integration is working correctly
- ✅ The API key is valid
- ⚠️  Quota/billing needs to be set up

## Setting Up Billing

### Step 1: Access Google AI Studio

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Navigate to **Get API Key** or **API Keys** section

### Step 2: Check Current Quota

1. Go to [API Usage Dashboard](https://ai.dev/usage?tab=rate-limit)
2. Check your current quota and usage
3. Review rate limits and quotas

### Step 3: Set Up Billing (If Required)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Billing** section
3. Create a billing account or link an existing one
4. Enable billing for the Gemini API

### Step 4: Manage API Keys

1. In Google AI Studio, go to **API Keys**
2. Create a new API key or use the existing one
3. Set up quota limits if needed
4. Monitor usage regularly

## Free Tier Limits

Google Gemini API offers a free tier with limitations:
- **Rate Limits**: Requests per minute/day
- **Token Limits**: Input/output tokens per day
- **Model Access**: Some models may require paid tier

Check the [official documentation](https://ai.google.dev/gemini-api/docs/rate-limits) for current limits.

## Updating API Key

To update the API key in the project:

1. Edit `.env` file:
   ```bash
   GEMINI_API_KEY=your_new_api_key_here
   ```

2. Restart the server:
   ```bash
   ./start_server.sh
   ```

## Monitoring Usage

### Check Usage Dashboard

Visit: https://ai.dev/usage?tab=rate-limit

You can see:
- Current usage
- Rate limits
- Quota consumption
- Billing information

### Programmatic Monitoring

You can also check usage programmatically:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List models (shows available models and their quotas)
models = list(genai.list_models())
for model in models:
    print(f"{model.name}: {model.supported_generation_methods}")
```

## Rate Limiting Strategies

### 1. Implement Retry Logic

The code already includes error handling, but you can add retry logic:

```python
import time
from google.api_core import retry

@retry.Retry()
def call_gemini_with_retry(prompt):
    # Your Gemini API call
    pass
```

### 2. Implement Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, time_window):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def wait_if_needed(self):
        now = time.time()
        # Remove old calls
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        # Wait if at limit
        if len(self.calls) >= self.max_calls:
            sleep_time = self.time_window - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(time.time())
```

### 3. Use Caching

Cache responses to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_gemini_call(prompt_hash):
    # Your Gemini API call
    pass
```

## Troubleshooting

### Error: 429 Quota Exceeded

**Solution:**
1. Check your quota at https://ai.dev/usage?tab=rate-limit
2. Wait for quota reset (usually daily)
3. Upgrade to paid tier if needed
4. Implement rate limiting in your code

### Error: 403 Permission Denied

**Solution:**
1. Verify API key is correct
2. Check if API is enabled in Google Cloud Console
3. Verify billing is set up (if required)

### Error: 401 Unauthorized

**Solution:**
1. Check API key is valid
2. Regenerate API key if needed
3. Verify API key has proper permissions

## Best Practices

1. **Monitor Usage**: Regularly check your usage dashboard
2. **Set Alerts**: Set up billing alerts in Google Cloud Console
3. **Implement Caching**: Cache responses to reduce API calls
4. **Use Appropriate Models**: Use Flash model for faster, cheaper responses
5. **Handle Errors Gracefully**: Implement proper error handling and retries
6. **Rate Limiting**: Implement rate limiting to avoid quota errors

## Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Rate Limits Documentation](https://ai.google.dev/gemini-api/docs/rate-limits)
- [API Usage Dashboard](https://ai.dev/usage?tab=rate-limit)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

## Support

If you encounter issues:
1. Check the [Gemini API Troubleshooting Guide](https://ai.google.dev/gemini-api/docs/troubleshooting)
2. Review [API Status](https://status.cloud.google.com/)
3. Contact Google Cloud Support if needed

