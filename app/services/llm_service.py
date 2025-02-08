import os
import httpx
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = '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'
if not API_KEY:
    raise ValueError("❌ Missing API Key! Set OPENROUTER_API_KEY in your .env file.")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

async def get_risks_and_decisions(context_data: dict):
    """
    Calls the OpenRouter LLM API asynchronously to analyze logistics context and return risks and decisions.
    """
    print("📤 Context Data Received:", context_data)

    prompt = f"""
    Given the following logistics context:
    - Previsions: {context_data.get('previsions', [])}
    - Processes: {context_data.get('processes', [])}
    - Constraints: {context_data.get('constraints', [])}
    
    Identify potential risks and suggest decisions to optimize logistics.
    Format your response as a JSON list of objects, each containing:
    - "risk": A description of the risk.
    - "decision": A recommended decision to mitigate the risk.
    """
    print(API_KEY)

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [
            {"role": "system", "content": "You are an AI assisting with logistics optimization."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, headers=HEADERS, json=data)

            print("📥 Response Status Code:", response.status_code)
            print("📥 Raw API Response:", response.text)

            if response.status_code == 401:
                return {"error": "Unauthorized: Check your API key."}

            if response.status_code != 200:
                return {"error": f"LLM API error: {response.text}"}

            # Extract and clean JSON response
            response_json = response.json()
            response_content = response_json["choices"][0]["message"]["content"]

            clean_json = re.sub(r"```json\n|\n```", "", response_content).strip()

            risks_decisions = json.loads(clean_json)
            print("✅ Parsed Response:", risks_decisions)

            return {"risks_decisions": risks_decisions}

        except json.JSONDecodeError:
            print("❌ Failed to parse response JSON:", response.text)
            return {"error": "Failed to parse response JSON. Ensure the LLM API returns valid JSON."}

        except httpx.HTTPStatusError as http_err:
            print(f"❌ HTTP error: {http_err}")
            return {"error": f"HTTP error: {str(http_err)}"}

        except Exception as e:
            print(f"❌ Exception: {e}")
            return {"error": f"Exception during LLM API call: {str(e)}"}

async def get_best_decision(problem: str, decision_contexts: list):
    """
    Calls the LLM to analyze past decision contexts and suggest the best decision for the given problem.
    """
    print("📤 Problem:", problem)
    print("📤 Old Decision Contexts:", decision_contexts)

    prompt = f"""
    Given the following problem:
    - Problem: {problem}

    Based on previous decision contexts:
    {json.dumps(decision_contexts, indent=2)}

    Suggest the best decision to resolve the problem, considering past decisions.
    Format your response as a JSON object with:
    - "best_decision": The recommended decision.
    """
    print(API_KEY)

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [
            {"role": "system", "content": "You are an AI assisting with logistics optimization."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, headers=HEADERS, json=data)

            print("📥 Response Status Code:", response.status_code)
            print("📥 Raw API Response:", response.text)

            if response.status_code == 401:
                return {"error": "Unauthorized: Check your API key."}

            if response.status_code != 200:
                return {"error": f"LLM API error: {response.text}"} 

            response_json = response.json()
            response_content = response_json["choices"][0]["message"]["content"]

            clean_json = re.sub(r"```json\n|\n```", "", response_content).strip()

            best_decision = json.loads(clean_json)  
            print("✅ Parsed Response:", best_decision)

            return {"best_decision": best_decision}

        except json.JSONDecodeError:
            print("❌ Failed to parse response JSON:", response.text)
            return {"error": "Failed to parse response JSON. Ensure the LLM API returns valid JSON."}  
    
