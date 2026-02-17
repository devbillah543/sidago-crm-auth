from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class LeadCreateRequest(BaseModel):
    full_name: str
    role: str
    company: str
    phone: str
    email: Optional[Union[EmailStr, str]] = ""
    follow_up_date: Optional[str] = None
    assigned_to: Optional[str] = None
    agent_id: int
    lead_type_id: Optional[int] = None       # integer ID of lead type
    contact_type_id: Optional[int] = None    # integer ID of contact type
    date_become_hot: Optional[str] = None

class LeadUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    follow_up_date: Optional[str] = None
    assigned_to: Optional[str] = None
    lead_type_id: Optional[int] = None       # integer ID of lead type
    contact_type_id: Optional[int] = None    # integer ID of contact type
    date_become_hot: Optional[str] = None