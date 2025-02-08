from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Sale(BaseModel):
    id: Optional[str] = Field(None, title="Sale ID", description="Unique identifier for the sale")
    product_id: str = Field(..., title="Product ID", description="Foreign key from Products collection")
    quantity_sold: int = Field(..., title="Quantity Sold", description="Quantity of the product sold")
    revenue: float = Field(..., title="Revenue", description="Revenue generated from the sale")
    sale_date: datetime = Field(default_factory=datetime.utcnow, title="Sale Date", description="Date of the sale")
    region: str = Field(..., title="Region", description="Region where the sale occurred")
    customer_segment: str = Field(..., title="Customer Segment", description="Segment of the customer who made the purchase")
    discount: float = Field(..., title="Discount", description="Discount applied to the sale")
    cost_of_goods_sold: float = Field(..., title="Cost of Goods Sold", description="Cost of the goods sold")

