import requests
import time

print("Testing TruthBot API...")
print("Uploading test file...")

start_time = time.time()

with open('test_false.txt', 'rb') as f:
    files = {'file': ('test_false.txt', f)}
    try:
        response = requests.post('http://localhost:8001/verify', files=files, timeout=150)
        elapsed = time.time() - start_time
        
        print(f"\nResponse received in {elapsed:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        print(f"\nResponse JSON:")
        
        result = response.json()
        print(f"Verified: {result.get('verified')}")
        print(f"Percentage: {result.get('percentage')}%")
        print(f"Errors: {result.get('errors')}")
        print(f"Analysis: {result.get('analysis')}")
        
    except requests.exceptions.Timeout:
        print(f"\nRequest timed out after {time.time() - start_time:.2f} seconds")
    except Exception as e:
        print(f"\nError: {e}")
