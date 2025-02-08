import httpx
import json
import re  # NEW: To remove code block formatting

API_KEY = "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"

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

async def get_risks_and_decisions(context_data: dict):
    """
    Calls the OpenRouter LLM API asynchronously to analyze logistics context and return risks and decisions.
    """
    print("📤 Context Data Received in FastAPI:", context_data)

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

    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [
            {"role": "system", "content": "You are an AI assisting with logistics optimization."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, headers=HEADERS, json=data)

            print("📥 Raw API Response:", response.text)
            print("📥 Response Status Code:", response.status_code)

            if response.status_code != 200:
                return {"error": f"LLM API error: {response.text}"}

            # Extract LLM response
            response_json = response.json()  # Ensure this is a dict
            response_content = response_json["choices"][0]["message"]["content"]

            # 🔥 FIX: Remove markdown code block markers
            clean_json = re.sub(r"```json\n|\n```", "", response_content).strip()

            # ✅ Attempt to parse the cleaned response
            risks_decisions = json.loads(clean_json)

            print("✅ Parsed Response:", risks_decisions)

            return {
                "risks_decisions": risks_decisions
            }

        except json.JSONDecodeError:
            return {"error": "Failed to parse response JSON. Ensure the LLM API returns valid JSON."}

        except httpx.HTTPStatusError as http_err:
            return {"error": f"HTTP error occurred: {str(http_err)}"}

        except Exception as e:
            return {"error": f"Exception during LLM API call: {str(e)}"}

