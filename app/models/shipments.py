from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional, List

class ShipmentStatusUpdate(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), title="Timestamp", description="Timestamp of the shipment status update")
    status: str = Field(..., title="Status", description="Current shipment status (Pending, In Transit, Delivered)")


class Shipment(BaseModel):
    id: Optional[str] = Field(None, title="Shipment ID", description="Unique identifier for the shipment")
    order_id: str = Field(..., title="Order ID", description="Foreign key from Orders collection")
    origin: str = Field(..., title="Origin", description="Starting point of the shipment")
    destination: str = Field(..., title="Destination", description="End point of the shipment")
    status: str = Field(..., title="Status", description="Current shipment status (Pending, In Transit, Delivered)")
    expected_delivery: datetime = Field(..., title="Expected Delivery", description="Estimated arrival date")
    actual_delivery: Optional[datetime] = Field(None, title="Actual Delivery", description="Actual delivery date")
    tracking_number: str = Field(..., title="Tracking Number", description="Tracking number of the shipment")
    carrier: str = Field(..., title="Carrier", description="Carrier of the shipment")
    shipping_cost: float = Field(..., title="Shipping Cost", description="Cost of the shipment")
    tracking_history: List[ShipmentStatusUpdate] = Field(..., title="Tracking History", description="Tracking history of the shipment")