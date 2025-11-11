# Debugging Guide for FarmerAI Assistant

## Recent Fixes Applied

### 1. **Enhanced Response Handling**
- Fixed handling of different Gemini API response structures
- Added support for `response.text`, `response.candidates`, and `response.parts`
- Better error messages when responses are blocked or empty

### 2. **Improved Error Logging**
- All errors now show `[ERROR]` prefix with detailed information
- Debug messages show `[DEBUG]` prefix for tracking flow
- Full stack traces for debugging

### 3. **Robust Error Handling**
- Handles API quota errors
- Handles authentication errors
- Handles timeout errors
- Handles blocked responses (safety filters)

## How to Debug Issues

### Step 1: Run the Diagnostic Script

```bash
cd /home/aminul/Documents/FarmerAI/backend
source venv/bin/activate
python test_gemini_direct.py
```

This will test:
- Basic Gemini API connectivity
- System instruction parameter support
- Intent extraction style prompts
- Reasoning node style prompts

### Step 2: Check Server Console Logs

When you test the assistant, look for these log messages:

**Success indicators:**
- `[DEBUG] call_gemini_llm called with system_instruction: True/False`
- `[DEBUG] Response received successfully`
- `[DEBUG] Response length: XXX characters`

**Error indicators:**
- `[ERROR] Gemini LLM call failed!`
- `[ERROR] Error type: XXX`
- `[ERROR] Error message: XXX`

### Step 3: Common Error Types and Solutions

#### 1. Quota/Rate Limit Error
```
[ERROR] Quota/rate limit error detected
```
**Solution:**
- Check API quota at: https://ai.dev/usage?tab=rate-limit
- Set up billing in Google Cloud Console
- Wait a few minutes and try again

#### 2. Authentication Error
```
[ERROR] API key authentication error
```
**Solution:**
- Verify `GEMINI_API_KEY` in `.env` file
- Check if API key is valid at: https://aistudio.google.com/
- Regenerate API key if needed

#### 3. System Instruction Error
```
[WARNING] System instruction failed: XXX
[DEBUG] Trying without system instruction as fallback...
```
**Solution:**
- This is handled automatically with fallback
- If you see this, the system will still work but may be less accurate

#### 4. Empty Response Error
```
[ERROR] Empty or invalid response from Gemini API
```
**Solution:**
- Check if response was blocked by safety filters
- Try rephrasing the query
- Check API status

#### 5. Timeout Error
```
[ERROR] Timeout error
```
**Solution:**
- Network connectivity issue
- API server may be slow
- Try again with a shorter query

## Testing the Fixes

### Test Voice Assistant:
1. Record a voice message
2. Check console for `[DEBUG]` messages
3. Look for transcription success
4. Check for reasoning node execution

### Test Image Upload:
1. Upload an image
2. Check console for image processing messages
3. Look for multimodal response generation
4. Verify response contains image analysis

### Test Chat:
1. Send a text message
2. Check console for intent extraction
3. Verify reasoning node generates response
4. Check response quality

## What to Share for Further Debugging

If issues persist, share:
1. **Full error logs** from console (lines with `[ERROR]`)
2. **Debug messages** showing where it fails
3. **Error type and message** from the logs
4. **Which feature** you're testing (voice/image/chat)

## Quick Fixes Applied

✅ Fixed response structure handling (supports multiple Gemini response formats)
✅ Added comprehensive error logging
✅ Added fallback for system instruction parameter
✅ Improved error messages with specific error types
✅ Added safety filter detection
✅ Enhanced timeout handling

## Next Steps

1. **Run the diagnostic script** to verify API connectivity
2. **Test each feature** (voice, image, chat)
3. **Check console logs** for `[ERROR]` messages
4. **Share specific error messages** if issues persist

The system should now provide much better error messages to help identify the exact problem!

