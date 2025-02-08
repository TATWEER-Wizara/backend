from typing import List, Optional
from datetime import datetime, UTC
from pydantic import BaseModel, Field
from bson import ObjectId

class Context(BaseModel):
    previsions: List[str] = Field(..., title="Previsions", description="Previsions for the decision context")
    processes: List[str] = Field(..., title="Processes", description="Processes for the decision context")
    constraints: List[str] = Field(..., title="Constraints", description="Constraints for the decision context")


class RiskDecision(BaseModel):
    risk: str = Field(..., title="Risk", description="Risk for the decision context")
    decision: str = Field(..., title="Decision", description="Decision for the decision context")
    justification: Optional[str] = Field(None, title="Justification", description="Justification for the decision context")
    approved: bool = Field(False, title="Approved", description="Approved for the decision context")


class DecisionContext(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str = Field(..., title="User ID", description="User ID for the decision context")
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    context: Context = Field(..., title="Context", description="Context for the decision context")
    risks_decisions: List[RiskDecision] = []

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user12345",
                "date": "2025-02-07T12:00:00Z",
                "context": {
                    "previsions": ["Increase in demand by 15%", "Expected supplier delays"],
                    "processes": ["Just-in-time inventory", "Automated warehouse sorting"],
                    "constraints": ["Limited storage space", "Budget restrictions"]
                },
                "risks_decisions": [
                    {
                        "risk": "Stockouts due to high demand",
                        "decision": "Increase buffer stock by 20%",
                        "justification": "Not needed as supplier lead time is reliable",
                        "approved": False
                    },
                    {
                        "risk": "Delays in shipment",
                        "decision": "Use alternative supplier with faster delivery",
                        "justification": None,
                        "approved": True
                    }
                ]
            }
        }
