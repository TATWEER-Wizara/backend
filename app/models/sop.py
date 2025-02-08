from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, UTC

#sop plan Model 

class SOP(BaseModel):
    id: Optional[str] = Field(None, title="SOP ID", description="Unique identifier for the SOP")
    product_id: str = Field(..., title="Product ID", description="Foreign key from Products collection")
    forecasted_demand: List[dict] = Field(..., description="The forecasted demand for the product")
    planned_production: int = Field(..., title="Planned Production", description="Planned production for the product")
    planned_inventory: int = Field(..., title="Planned Inventory", description="Planned inventory for the product")
    period: datetime = Field(..., title="Period", description="Period of the SOP")
    confidence_level: float = Field(..., title="Confidence Level", description="Confidence level of the SOP")
    actual_demand: int = Field(..., title="Actual Demand", description="Actual demand for the product")
    revision_number: int = Field(..., title="Revision Number", description="Revision number of the SOP")
    notes: Optional[str] = Field(None, title="Notes", description="Notes for the SOP")
    production_capacity: List[dict] = Field(..., description="The production capacity for the product")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), title="Created At", description="Creation timestamp")