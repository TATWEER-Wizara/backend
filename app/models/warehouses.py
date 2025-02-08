from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Warehouse(BaseModel):
    id: Optional[str] = Field(None, title="Warehouse ID", description="Unique identifier for the warehouse")
    name: str = Field(..., title="Warehouse Name", description="Name of the warehouse")
    location: str = Field(..., title="Warehouse Location", description="Location of the warehouse")
    capacity: int = Field(..., title="Warehouse Capacity", description="Capacity of the warehouse")
    manager: str = Field(..., title="Warehouse Manager", description="Manager of the warehouse")
    is_active: bool = Field(..., title="Warehouse Active", description="Active status of the warehouse")

