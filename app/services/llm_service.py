"""
LLM Service Module

This module provides integration with OpenRouter's LLM API for logistics decision-making and risk analysis.
It handles the communication with the API and processes responses for the application's needs.

Dependencies:
    - httpx: For async HTTP requests
    - python-dotenv: For environment variable management
    - bson: For MongoDB ObjectId handling

Environment Variables Required:
    - OPENROUTER_API_KEY: API key for OpenRouter service
"""

import os
import httpx
import json
import re
from dotenv import load_dotenv
from bson import ObjectId
from typing import Any, Dict, List

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ Missing API Key! Set OPENROUTER_API_KEY in your .env file.")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def convert_objectid_to_str(data: Any) -> Any:
    """
    Recursively convert ObjectId fields to strings in a MongoDB document.

    Args:
        data (Any): The input data to convert. Can be a dictionary, list, ObjectId, or any other type.

    Returns:
        Any: The converted data with all ObjectId instances replaced with their string representations.

    Example:
        >>> doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "items": [{"id": ObjectId("507f191e810c19729de860ea")}]}
        >>> convert_objectid_to_str(doc)
        {'_id': '507f1f77bcf86cd799439011', 'items': [{'id': '507f191e810c19729de860ea'}]}
    """
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

async def get_risks_and_decisions(context_data: dict):
    """
    Analyze logistics context using OpenRouter LLM API and return potential risks and recommended decisions.

    Args:
        context_data (dict): A dictionary containing logistics context with the following keys:
            - previsions (list): List of logistics forecasts or predictions
            - processes (list): List of current logistics processes
            - constraints (list): List of operational constraints

    Returns:
        dict: A dictionary containing either:
            - {"risks_decisions": list}: List of dictionaries, each containing:
                - "risk": str - Description of identified risk
                - "decision": str - Recommended decision to mitigate the risk
            - {"error": str}: Error message if the API call or processing fails

    Raises:
        json.JSONDecodeError: If the API response cannot be parsed as JSON
        httpx.HTTPStatusError: If the API request fails
        Exception: For any other unexpected errors

    Example:
        >>> context = {
        ...     "previsions": ["High demand expected next month"],
        ...     "processes": ["Current delivery route through city center"],
        ...     "constraints": ["Limited warehouse capacity"]
        ... }
        >>> result = await get_risks_and_decisions(context)
        >>> print(result)
        {
            "risks_decisions": [
                {
                    "risk": "Warehouse overflow due to high demand",
                    "decision": "Temporarily lease additional storage space"
                }
            ]
        }
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
    Analyze past decision contexts and suggest the best decision for a given problem using OpenRouter LLM API.

    Args:
        problem (str): Description of the current logistics problem to solve
        decision_contexts (list): List of previous decision contexts from MongoDB, containing ObjectId fields

    Returns:
        dict: A dictionary containing either:
            - {"best_decision": dict}: The recommended decision based on historical context
            - {"error": str}: Error message if the API call or processing fails

    Raises:
        json.JSONDecodeError: If the API response cannot be parsed as JSON
        httpx.HTTPStatusError: If the API request fails
        Exception: For any other unexpected errors

    Example:
        >>> problem = "Delivery delays in downtown area"
        >>> contexts = [
        ...     {
        ...         "_id": ObjectId("507f1f77bcf86cd799439011"),
        ...         "problem": "Urban congestion",
        ...         "solution": "Rerouted through suburbs"
        ...     }
        ... ]
        >>> result = await get_best_decision(problem, contexts)
        >>> print(result)
        {
            "best_decision": {
                "best_decision": "Implement alternative route through less congested areas"
            }
        }
    """
    print("📤 Problem:", problem)
    print("📤 Old Decision Contexts:", decision_contexts)

    # Convert ObjectId fields to strings
    decision_contexts = convert_objectid_to_str(decision_contexts)

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