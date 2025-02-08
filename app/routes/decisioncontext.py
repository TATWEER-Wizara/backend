from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.decisioncontext import DecisionContext, Context
from app.services.llm_service import get_risks_and_decisions, get_best_decision
from app.routes.websockets import send_decision_update
from app.database import database, decision_context_collection
import json
from fastapi import Query
from bson import ObjectId
from fastapi import Body
from app.models.decisioncontext import ProblemRequest


decision_context_router = APIRouter()

@decision_context_router.post("/decision-context/submit/")
async def submit_decision_context(context: Context, user_id: str = Query(..., description="User ID")):

    """
    Send context to LLM and retrieve risks/decisions.
    This does NOT save data to the database yet.
    """
    print(context.model_dump())
    llm_response = await get_risks_and_decisions(context.model_dump())
    risks_decisions = llm_response
    
    if "error" in llm_response:
        raise HTTPException(status_code=500, detail=llm_response["error"])

    # Transform the array response into a structured object
    response_data = risks_decisions

    # Send update to WebSocket clients
    await send_decision_update({"user_id": user_id, "risks_decisions": llm_response})

    return response_data

@decision_context_router.post("/decision-context/best-decision/")
async def get_best_decision_endpoint(
    problem_request: ProblemRequest = Body(..., description="The problem description in the request body"),
    user_id: str = Query(..., description="User ID")
):
    # Extract the problem from the request body
    problem = problem_request

    # Clean up the user_id (remove accidental quotes)
    if isinstance(user_id, str):
        user_id = user_id.strip("'")
    
    print(f"🔍 Searching for user_id: '{user_id}'")  # Debugging print

    # Fetch all decision contexts for the user
    decision_contexts = await database.decision_context_collection.find({"user_id": user_id}).to_list(None)
    if not decision_contexts:
        raise HTTPException(status_code=404, detail="No decision contexts found for this user")

    # Get the best decision
    best_decision = await get_best_decision(problem, decision_contexts)
    return best_decision
    



@decision_context_router.get("/decision-contexts/user")
async def get_all_decision_contexts_for_user(user_id: str = Query(..., description="User ID")):
    user_id = user_id.strip("'").strip('"')  

    print(f"🔍 Searching for user_id: '{user_id}'")  # Debugging print

    decision_contexts = await database.decision_context_collection.find({"user_id": user_id}).to_list(None)

    if not decision_contexts:
        raise HTTPException(status_code=404, detail="No decision contexts found for this user")

    # ✅ Convert `_id` from `ObjectId` to `str` before returning
    for context in decision_contexts:
        context["_id"] = str(context["_id"])

    return decision_contexts


#create a new decision context
@decision_context_router.post("/decision-context/create/")
async def create_decision_context(decision_context: DecisionContext):
    await database.decision_context_collection.insert_one(decision_context.model_dump())
    return decision_context





