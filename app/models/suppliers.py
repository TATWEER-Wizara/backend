from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from pydantic import EmailStr


class Supplier(BaseModel):
    id: Optional[str] = Field(None, title="Supplier ID", description="Unique identifier for the supplier")
    name: str = Field(..., title="Supplier Name", description="Name of the supplier")
    contact_person: str = Field(..., title="Supplier Contact Person", description="Contact person of the supplier")
    email: EmailStr = Field(..., title="Supplier Email", description="Email of the supplier")
    phone: str = Field(..., title="Supplier Phone", description="Phone number of the supplier")
    address: str = Field(..., title="Supplier Address", description="Address of the supplier")
    payment_terms: str = Field(..., title="Supplier Payment Terms", description="Payment terms of the supplier")
    lead_time: int = Field(..., title="Supplier Lead Time", description="Lead time of the supplier")
