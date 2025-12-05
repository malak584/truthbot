# 🔧 TruthBot AI - Troubleshooting Guide

## Fixed Issue: Gemini Model Error

### Problem
```
404 models/gemini-pro is not found for API version v1beta
```

### Solution
✅ **Updated model from `gemini-pro` to `gemini-2.5-flash`**

The old `gemini-pro` model has been deprecated. The application now uses:
- **Text verification**: `gemini-2.5-flash` (latest stable)
- **Image verification**: `gemini-2.5-flash` (multimodal support)

---

## Common Issues & Solutions

### 1. API Key Issues

**Symptoms:**
- "Invalid API key" errors
- "GEMINI_API_KEY not found" errors

**Solution:**
1. Check your `.env` file exists in the project root
2. Ensure it contains: `GEMINI_API_KEY=your_actual_key_here`
3. Get a key from: https://makersuite.google.com/app/apikey
4. Restart the server after updating

### 2. Rate Limit Exceeded

**Symptoms:**
- "API rate limit exceeded" errors
- 429 status codes

**Solution:**
- Gemini free tier has limits (60 requests/minute)
- Wait 1 minute before retrying
- Consider upgrading to paid tier for higher limits

### 3. Tesseract OCR Not Found

**Symptoms:**
- "tesseract is not installed" errors
- Image text extraction fails

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 4. Virtual Environment Issues

**Symptoms:**
- "ModuleNotFoundError" for installed packages
- Packages not found

**Solution:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Port Already in Use

**Symptoms:**
- "Address already in use" error
- Server won't start

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 6. File Upload Errors

**Symptoms:**
- "No text could be extracted"
- Empty results

**Solution:**
- Ensure PDF is not password-protected
- Check image quality (not blurry)
- Verify file is not corrupted
- Supported formats: PDF, PNG, JPG, JPEG, BMP, WEBP, TXT

### 7. CORS Issues

**Symptoms:**
- Frontend can't connect to API
- Cross-origin errors in browser

**Solution:**
Already configured in `app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
)
```

---

## Testing the API

### Quick Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
    "status": "healthy",
    "service": "TruthBot AI",
    "version": "2.0.0",
    "ai_engine": "Google Gemini"
}
```

### Test Verification with curl
```bash
curl -X POST "http://localhost:8000/verify" \
  -F "file=@test.pdf"
```

### Test with Python
```bash
source venv/bin/activate
python3 test_gemini.py
```

---

## Performance Tips

1. **Optimize PDF Size**: Compress PDFs before uploading
2. **Image Quality**: Use clear, high-contrast images for better OCR
3. **Text Length**: Longer texts take more time to analyze
4. **Batch Processing**: For multiple files, add delays between requests

---

## Monitoring

### Check Logs
```bash
# Server logs are shown in terminal
# For production, redirect to file:
python3 app.py > logs/app.log 2>&1 &
```

### API Documentation
Visit: http://localhost:8000/docs

Interactive API testing interface with all endpoints documented.

---

## Getting Help

1. Check the error message in the UI
2. Look at server terminal for DEBUG logs
3. Verify API key is valid at: https://makersuite.google.com
4. Test with the provided test files
5. Check Gemini API status: https://status.cloud.google.com/

---

## Current Configuration

✅ **Model**: `gemini-2.5-flash` (Latest stable, June 2025)  
✅ **Temperature**: `0.2` (more factual, less creative)  
✅ **Max Tokens**: `1000`  
✅ **Supported Files**: PDF, Images, Text  
✅ **Max File Size**: Unlimited (browser dependent)  
✅ **Context Window**: Up to 1 million tokens  

---

## Production Checklist

Before deploying to production:

- [ ] Change CORS to specific domain
- [ ] Use environment variables for secrets
- [ ] Add rate limiting
- [ ] Set up logging
- [ ] Add authentication if needed
- [ ] Use HTTPS
- [ ] Monitor API usage
- [ ] Set up error alerts
- [ ] Add file size limits
- [ ] Configure timeout settings

---

**Last Updated**: December 5, 2025  
**Version**: 2.0.0
