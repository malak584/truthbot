import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def verify_content(text: str):
    """
    Sends text to Google Gemini API to verify accuracy.
    """
    if not text or len(text.strip()) < 5:
        return {"status": "Error", "reason": "No readable text found in file."}

    # Prompt Engineering for specific output
    prompt = f"""
    Analyze the following text for factual accuracy.
    
    TEXT: "{text[:2000]}"
    
    Reply ONLY in valid JSON format:
    {{
        "status": "APPROVED" (if true) or "FALSE" (if contains misinformation),
        "reason": "Short explanation of why."
    }}
    """

    try:
        # Call Google Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=500
            )
        )
        
        raw_output = response.text
        
        # Clean up potential markdown formatting (```json ... ```)
        clean_json = raw_output.replace("```json", "").replace("```", "").strip()
        
        try:
            parsed = json.loads(clean_json)
            return parsed
        except json.JSONDecodeError:
            # If model replied with text but not perfect JSON
            return {"status": "Review", "reason": raw_output}

    except Exception as e:
        print(f"DEBUG: Gemini API Exception: {e}")
        return {"status": "Error", "reason": str(e)}