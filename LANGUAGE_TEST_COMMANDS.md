# Language Fix - Quick Test Commands

## Current Status
✅ Code modified and syntax verified
⏳ Awaiting your test to verify it's working

## Test Commands (Copy & Paste)

### Test 1: Bengali Text Input
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -F "message=আমার ধানের পাতা হলুদ হয়ে যাচ্ছে, এটা কি সমস্যা?" \
  -F "user_id=test_user" \
  -F "lat=23.8103" \
  -F "lon=90.3563" | jq '.reply_text'
```
**Expected**: Response in Bengali script (আ ই উ ঈ ও etc visible)

### Test 2: English Text Input
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -F "message=My cucumber plant has yellow leaves, what should I do?" \
  -F "user_id=test_user" \
  -F "lat=23.8103" \
  -F "lon=90.3563" | jq '.reply_text'
```
**Expected**: Response in English

### Test 3: Watch Backend Logs
```bash
tail -f backend.log | grep -E "Language|STT|detected language|Response language"
```
**Expected logs to see**:
- `[DEBUG] STT node: Detected language: bn` (for Bengali)
- `[DEBUG] STT node: Detected language: en` (for English)
- `[DEBUG] Reasoning node: Response language selected: Bengali`
- `🚨 CRITICAL LANGUAGE REQUIREMENT`

## What to Look For

### ✅ PASS - Bengali Input
- Response contains Bengali characters
- System prompt mentions "বাংলা"
- Logs show `detected language: bn`

### ❌ FAIL - Bengali Input
- Response in English
- No Bengali characters in response
- Logs show `detected language: en`

### ✅ PASS - English Input
- Response in English
- No Bengali characters mixed in
- Logs show `detected language: en`

### ❌ FAIL - English Input  
- Response in Bengali
- Wrong language detected
- Logs show `detected language: bn`

## One-Line Test (Bengali)

```bash
curl -s -X POST http://localhost:8000/api/chat -F "message=আমার ধানে রোগ" -F "user_id=test" -F "lat=23.8" -F "lon=90.3" | grep -o '"reply_text":"[^"]*"' | cut -d'"' -f4 | head -c 50
```

## One-Line Test (English)

```bash
curl -s -X POST http://localhost:8000/api/chat -F "message=My rice has disease" -F "user_id=test" -F "lat=23.8" -F "lon=90.3" | grep -o '"reply_text":"[^"]*"' | cut -d'"' -f4 | head -c 50
```

## Check Backend Status

```bash
# Is backend running?
curl http://localhost:8000/api/conversations | head -c 100

# Yes if you see: [{"id": or []
# No if you see: Connection refused
```

## If Tests Fail

### Check 1: Backend Error
```bash
tail -f backend.log | head -50
# Look for: SyntaxError, ImportError, or connection errors
```

### Check 2: Language Detection
```bash
tail -f backend.log | grep "STT node"
# Should show: Detected language: bn or en
```

### Check 3: System Instruction Sent
```bash
tail -f backend.log | grep "CRITICAL LANGUAGE"
# Should show the critical language instruction
```

### Check 4: Response Language Check
```bash
tail -f backend.log | grep "Response language mismatch"
# If present = system detected wrong language and regenerating
```

## Files That Were Modified

1. `backend/app/farm_agent/langgraph_app.py` - Language detection improved
2. `backend/app/main.py` - Better error logging
3. `.gitignore` - New file (ignores build artifacts)

## Next If Still Not Working

1. Check logs match expected pattern
2. Try different Bengali text (more characters)
3. Check if Gemini API is responding correctly
4. See `LANGUAGE_FIX_DEBUGGING.md` for detailed debugging

## Summary

| Input | Expected | Check With |
|-------|----------|-----------|
| Bengali text | Bengali response | Test 1 |
| English text | English response | Test 2 |
| Logs | Language detection | Test 3 |

---

**Ready to test?** Run Test 1, Test 2, and Test 3 above and share the outputs!
