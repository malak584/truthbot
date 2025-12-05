#!/usr/bin/env python3
"""
Quick test script to verify Gemini API is working
"""

import sys
sys.path.insert(0, 'app')

from app.services.verifier import verify_content

# Test with a simple claim
test_text = "The Earth is the third planet from the Sun and has one natural satellite called the Moon."

print("🧪 Testing Gemini API...")
print(f"Test text: {test_text}")
print("\n" + "="*60 + "\n")

result = verify_content(test_text)

print("📊 Result:")
print(f"  ✓ Verified: {result.get('verified')}")
print(f"  ✓ Percentage: {result.get('percentage')}%")
print(f"  ✓ Summary: {result.get('summary')}")
print(f"  ✓ Analysis: {result.get('analysis')[:100]}...")
print(f"  ✓ Errors: {result.get('errors')}")

print("\n✅ API test complete!")
