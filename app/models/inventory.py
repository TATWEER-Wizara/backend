from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Inventory(BaseModel):
    id: Optional[str] = Field(None, title="Inventory ID", description="Unique identifier for the inventory")
    product_id: str = Field(..., title="Product ID", description="Foreign key from Products collection")
    stock_level: int = Field(..., title="Stock Level", description="Current stock quantity")
    warehouse_id: Optional[str] = Field(None, title="Warehouse ID", description="Reference to Warehouses collection")
    last_updated: datetime = Field(default_factory=datetime.utcnow, title="Last Updated", description="Last update timestamp")
    min_stock_level: int = Field(..., title="Minimum Stock Level", description="Minimum stock level")
    max_stock_level: int = Field(..., title="Maximum Stock Level", description="Maximum stock level")
    reorder_point: int = Field(..., title="Reorder Point", description="Reorder point")
    batch_number: Optional[str] = Field(None, title="Batch Number", description="Batch number")