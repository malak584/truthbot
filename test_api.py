# test_integration.py
import requests
import os

# Create a test file containing a fake claim
with open("test_claim.txt", "w") as f:
    f.write("The capital of France is London.")

print("🚀 Sending False Claim to TruthBot (Qwen + Serper)...")
url = "http://localhost:8000/verify"
files = {'file': open('test_claim.txt', 'rb')}

try:
    response = requests.post(url, files=files)
    print("\nResponse Status:", response.status_code)
    data = response.json()
    print("AI Analysis:", data.get('analysis'))
    print("Score:", data.get('percentage'))
    print("Errors:", data.get('errors'))
    
    # Clean up
    os.remove("test_claim.txt")
except Exception as e:
    print("Connection failed. Is Uvicorn running?", e)