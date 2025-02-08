from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List  

class OrderItem(BaseModel):
    product_id: str = Field(..., title="Product ID", description="Foreign key from Products collection")
    quantity: int = Field(..., title="Quantity", description="Quantity of the product")
    unit_price: float = Field(..., title="Unit Price", description="Price of the product")
    subtotal: float = Field(..., title="Subtotal", description="Subtotal of the product")


class Order(BaseModel):
    id: Optional[str] = Field(None, title="Order ID", description="Unique identifier for the order")
    order_id: str = Field(..., title="Order ID", description="Unique identifier for the order")
    user_id: str = Field(..., title="User ID", description="Foreign key from Users collection")
    status: str = Field(..., title="Status", description="Order status (Pending, Shipped, Completed)")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="Created At", description="Order creation timestamp")
    updated_at: Optional[datetime] = Field(None, title="Updated At", description="Last update timestamp")
    total_amount: float = Field(..., title="Total Amount", description="Total amount of the order")
    payment_status: str = Field(..., title="Payment Status", description="Payment status of the order")
    items: List[OrderItem] = Field(..., title="Items", description="Items in the order")
    