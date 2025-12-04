import requests

def test_api():
    url = "http://localhost:8000/verify"
    
    # Create a dummy file
    with open("test_claim.txt", "w") as f:
        f.write("The earth is flat and the moon is made of cheese.")
        
    files = {'file': open('test_claim.txt', 'rb')}
    
    try:
        print("Sending request to API...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API is running! (uvicorn app:app --reload)")

if __name__ == "__main__":
    test_api()
