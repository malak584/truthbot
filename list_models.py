#!/usr/bin/env python3
"""
List all available Gemini models from your API key
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Fetching available Gemini models...\n")

try:
    models = genai.list_models()
    
    print("📋 Available Models:")
    print("=" * 80)
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
    
    print("\n" + "=" * 80)
    print("\n💡 Recommended for TruthBot:")
    print("   • gemini-1.5-flash-002 (fast, stable)")
    print("   • gemini-1.5-pro-002 (more accurate)")
    print("   • gemini-2.0-flash-001 (newest, GA)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check your API key is valid")
    print("2. Visit: https://makersuite.google.com/app/apikey")
    print("3. Ensure you have API access enabled")
