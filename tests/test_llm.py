import requests
import json
import os

# Load API key from environment variables
API_KEY = "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" # Ensure this is set

# Ensure API key is correctly loaded
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is not set. Please check your environment variables!")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",  
    "Content-Type": "application/json",
}
context = {
  "previsions": ["Increase in demand by 15%", "Expected supplier delays"],
  "processes": ["Just-in-time inventory", "Automated warehouse sorting"],
  "constraints": ["Limited storage space", "Budget restrictions"]
}


prompt = f"""
    Given the following logistics context:
    - Previsions: {context['previsions']}
    - Processes: {context['processes']}
    - Constraints: {context['constraints']}
    
    Identify potential risks and suggest decisions to optimize logistics.
    Format your response as a JSON list of objects, each containing:
    - "risk": A description of the risk.
    - "decision": A recommended decision to mitigate the risk.
    """

DATA = {
    "model": "google/gemini-2.0-flash-lite-preview-02-05:free",  
    "messages": [ {"role": "system", "content": "You are an AI assisting with logistics optimization."},
                    {"role": "user", "content": prompt}]
}



# Send request
response = requests.post(URL, headers=HEADERS, data=json.dumps(DATA))

# Debugging output
print("🔹 Request Headers:", HEADERS)
print("🔹 API Key Sent:", "Yes" if API_KEY else "No")
print("🔹 Response Status:", response.status_code)
print("🔹 Response Body:", response.json()["choices"][0]["message"]["content"])
