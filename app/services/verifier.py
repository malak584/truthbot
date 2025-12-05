# app/services/verifier.py
import os
import json
import ollama
from app.utils.search import search_web

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen:7b")

def verify_content(text: str):
    """
    Verifies text by searching the web via Serper and analyzing with Ollama (Qwen).
    """
    try:
        print(f"🤖 Processing with {MODEL_NAME}...")

        # 1. Summarize text to create a search query
        # (We use a simple truncation or a quick LLM call to get a query)
        search_query = text[:200].replace("\n", " ") # Simple approach for speed
        
        # 2. Get Fact-Checking Context from Serper
        print(f"🔍 Searching Serper for: {search_query[:50]}...")
        search_context = search_web(search_query)
        
        if not search_context:
            search_context = "No external search results available. Verify based on logic only."

        # 3. Construct the Prompt for Qwen
        prompt = f"""
        You are a professional Fact-Checker API. verify the following text based strictly on the provided Search Context.
        
        INPUT TEXT:
        "{text}"

        SEARCH CONTEXT (Evidence from Google):
        {search_context}

        INSTRUCTIONS:
        1. Compare the Input Text against the Search Context.
        2. Determine if the claims are True, False, or Misleading.
        3. Provide an accuracy score (0-100).
        4. List specific errors if any.
        
        OUTPUT FORMAT:
        You must respond with valid JSON only. Do not add markdown blocks like ```json.
        Format:
        {{
            "verified": boolean,
            "percentage": integer,
            "analysis": "string explanation",
            "errors": ["list of false claims found"],
            "summary": "short summary"
        }}
        """

        # 4. Call Ollama
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt}
        ])

        content = response['message']['content']
        
        # Clean up code blocks if the LLM adds them
        content = content.replace("```json", "").replace("```", "").strip()

        # 5. Parse JSON
        result = json.loads(content)
        return result

    except json.JSONDecodeError:
        # Fallback if LLM fails to generate valid JSON
        return {
            "verified": False,
            "percentage": 0,
            "analysis": f"AI Verification failed to format response. Raw output: {content[:100]}...",
            "errors": ["Internal AI Format Error"],
            "summary": "Error parsing AI response"
        }
    except Exception as e:
        return {
            "verified": False,
            "percentage": 0,
            "analysis": str(e),
            "errors": ["System Error"],
            "summary": "Verification crashed"
        }

def verify_content_with_image(image_bytes):
    """
    Note: Standard Qwen is text-only. 
    To use images, you need 'llava' or 'qwen-vl' installed via Ollama.
    """
    # Placeholder for Vision support
    return {
        "verified": False,
        "percentage": 0,
        "errors": ["Image verification requires a Vision Model (e.g., LLaVA)"],
        "analysis": "Current configuration uses text-only Qwen model.",
        "summary": "Image verification not configured"
    }
def extract_text_from_image(image_bytes):
    """
    Uses LLaVA to extract text and context from an image.
    """
    print("👀 LLaVA is analyzing the image...")
    
    prompt = """
    Analyze this image in detail. 
    1. Transcribe any text visible in the image exactly as it appears.
    2. Describe the visual context or any claims made by the image.
    Output the result as plain text.
    """

    try:
        response = ollama.chat(
            model='llava',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_bytes]
            }]
        )
        return response['message']['content']
    except Exception as e:
        print(f"LLaVA Error: {e}")
        return None

def verify_content_with_image(image_bytes):
    """
    Pipeline: Image -> LLaVA (Extraction) -> Text -> Qwen (Verification)
    """
    # 1. Extract text using LLaVA
    extracted_text = extract_text_from_image(image_bytes)
    
    if not extracted_text:
        return {
            "verified": False,
            "percentage": 0,
            "errors": ["Could not extract text or context from the image using LLaVA."],
            "analysis": "Image analysis failed.",
            "summary": "Error processing image."
        }

    print(f"📝 Extracted Text: {extracted_text[:100]}...")

    # 2. Pass the extracted text to your EXISTING text verifier
    # This reuses your logic for Serper/Gemini/Qwen
    return verify_content(extracted_text)