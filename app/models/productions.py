from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, UTC

class Production(BaseModel):
    id: Optional[str] = Field(None, title="Production ID", description="Unique identifier for the production")
    product_id: str = Field(..., title="Product ID", description="Foreign key from Products collection")
    quantity_produced: int = Field(..., title="Quantity Produced", description="Quantity of the product produced")
    production_date: datetime = Field(default_factory=lambda: datetime.now(UTC), title="Production Date", description="Date of the production")
    factory_location: str = Field(..., title="Factory Location", description="Location of the factory where the production occurred")
    batch_number: str = Field(..., title="Batch Number", description="Batch number of the production")
    production_cost: float = Field(..., title="Production Cost", description="Cost of the production")
    quality_status: str = Field(..., title="Quality Status", description="Quality status of the production")
    waste_quantity: int = Field(..., title="Waste Quantity", description="Quantity of waste produced during the production")


