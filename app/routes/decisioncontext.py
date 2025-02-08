from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.decisioncontext import DecisionContext, Context
from app.services.llm_service import get_risks_and_decisions
from app.routes.websockets import send_decision_update
from app.database import database, decision_context_collection
import json


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


@decision_context_router.post("/decision-context/approve/")
async def approve_decision_context(decision_context: DecisionContext):
    """
    Save the full DecisionContext object after approval/denial.
    """
    decision_context_id = await database.decision_context_collection.insert_one(decision_context.model_dump())

    return {"message": "DecisionContext saved", "id": str(decision_context_id.inserted_id)}


# get all decision contexts for a user
@decision_context_router.get("/decision-contexts/user/{user_id}")
async def get_all_decision_contexts_for_user(user_id: str):
    decision_contexts = await database.decision_context_collection.find({"user_id": user_id}).to_list(None)
    if not decision_contexts:
        raise HTTPException(status_code=404, detail="No decision contexts found for this user")
    return decision_contexts





