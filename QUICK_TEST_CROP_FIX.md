# Quick Testing Script for Crop Identification Fix

Run this script to quickly test if the crop identification bug is fixed.

## Test 1: Cucumber vs Rice (Basic Context Isolation)

```bash
#!/bin/bash

# Restart backend to apply changes
echo "Restarting backend..."
cd /home/aminul/Documents/KrishiBondhu/backend
pkill -f "uvicorn"
sleep 2
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
sleep 5

echo "✓ Backend restarted"
echo ""
echo "Test Steps:"
echo "1. Go to http://localhost:5173 (frontend)"
echo "2. Switch to CAMERA or CHAT tab"
echo "3. Try this sequence:"
echo ""
echo "   A) Ask: 'My cucumber plant has yellow leaves, what should I do?'"
echo "      Expected: Advice about cucumber, NOT rice"
echo ""
echo "   B) Ask: 'How do I detect rice blast disease?'"
echo "      Expected: Advice about rice blast, not jumping back to cucumber"
echo ""
echo "   C) Upload image of cucumber"
echo "      Expected: Analysis identifies cucumber, not rice"
echo ""
echo "4. Check backend logs for:"
echo "   - [DEBUG] ===== REASONING NODE START ====="
echo "   - [DEBUG] Crop detected: (whatever the actual crop is)"
echo "   - Should NOT see old crop mentioned"
```

## Test 2: Check Backend Debug Output

```bash
# Terminal 1: Start backend with verbose output
cd /home/aminul/Documents/KrishiBondhu/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Watch for these lines in the output:
# [DEBUG] ===== REASONING NODE START =====
# [DEBUG] Transcript: <current query>
# [DEBUG] Crop detected: <should be appropriate for current request>
# [DEBUG] Vision result keys: <should be appropriate>
```

## Test 3: Language Enforcement

```bash
# Test that language is properly detected and enforced

# Voice Test:
echo "Test: Record in Bengali → Should respond in Bengali"
echo "Test: Record in English → Should respond in English"

# Chat Test:
echo "Test: Type in Bengali → Should respond in Bengali"
echo "Test: Type in English → Should respond in English"
```

## Test 4: Sequential Crop Analysis

```bash
# Upload images in this order:
# 1. Rice with disease → Check response mentions rice
# 2. Tomato with spots → Check response mentions tomato (NOT rice)
# 3. Potato with issues → Check response mentions potato (NOT rice/tomato)

# If you see old crop names in responses → Bug still exists
```

## Expected Behavior After Fix

❌ **BEFORE FIX (Wrong)**:
```
User: "My cucumber has yellow leaves"
System: "This looks like rice plant disease. You should apply..."
                     ^^^^^ WRONG! It's cucumber, not rice!
```

✅ **AFTER FIX (Correct)**:
```
User: "My cucumber has yellow leaves"
System: "Yellow leaves on cucumber can indicate... [cucumber-specific advice]"
                                       ^^^^^^^^ CORRECT!
```

## Quick Verification Checklist

- [ ] Cucumber image → Describes cucumber, not rice
- [ ] Rice question → Describes rice disease, not previous crop
- [ ] Tomato image → Describes tomato, not previous crops
- [ ] Language detection correct (Bengali in → Bengali out)
- [ ] Backend logs show fresh analysis for each request
- [ ] No mention of previous crops in new responses

## If Tests Fail

### Issue: Still seeing wrong crop mentioned
**Solution**: 
1. Check backend logs for `[DEBUG] Crop detected:`
2. Verify prompt contains `🚨 CRITICAL - PROCESS ONLY CURRENT REQUEST 🚨`
3. Look for error in `call_gemini_llm()` 

### Issue: Language not matching
**Solution**:
1. Check `detect_language_from_text()` function
2. Verify system_instruction contains language requirement
3. Look for language mismatch warning in logs

### Issue: Same response for different crops
**Solution**:
1. Restart backend completely
2. Clear browser cache
3. Test with completely different crops (rice, tomato, potato)

## Commands to Run

```bash
# 1. Restart backend cleanly
cd /home/aminul/Documents/KrishiBondhu/backend
pkill -f "uvicorn"
sleep 2
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# 2. Watch logs in real-time
tail -f backend.log | grep -E "(REASONING|Crop detected|CRITICAL)"

# 3. Test with curl (if needed)
curl -X POST http://localhost:8000/api/chat \
  -F "message=My cucumber plant has yellow leaves" \
  -F "user_id=test_user" \
  -F "lat=23.8103" \
  -F "lon=90.3563"

# 4. Check if response mentions cucumber, not rice
```

## Success Criteria

✅ All test cases pass
✅ Crop names match input (cucumber→cucumber, rice→rice, tomato→tomato)
✅ No old context appears in new responses
✅ Language correctly detected and enforced
✅ Backend logs show clean state for each request

---

**Run these tests after applying the fix from `CROP_IDENTIFICATION_FIX.md`**
