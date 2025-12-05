# app/utils/search.py
import requests
import os
import json

def search_web(query: str):
    """
    Searches the web using Serper.dev API to find fact-checking context.
    """
    url = "https://google.serper.dev/search"
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        print("❌ Error: SERPER_API_KEY not found.")
        return ""

    payload = json.dumps({
        "q": query,
        "num": 5  # Get top 5 results
    })
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        
        # Parse organic results into a context string
        snippets = []
        if 'organic' in data:
            for item in data['organic']:
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                snippets.append(f"Source: {title}\nContent: {snippet}")
        
        return "\n\n".join(snippets)
        
    except Exception as e:
        print(f"❌ Serper Error: {str(e)}")
        return ""