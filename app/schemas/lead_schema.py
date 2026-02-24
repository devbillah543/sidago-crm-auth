from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class LeadCreateRequest(BaseModel):
    company_id: int
    full_name: str
    role: str
    phone: str
    email: Optional[Union[EmailStr, str]] = ""
    others_contacts: Optional[str] = None
    contact_type_id: int
    lead_type_id: Optional[int] = None       # integer ID of lead type

class LeadUpdateRequest(BaseModel):
    company_id: int
    full_name: str
    role: str
    phone: str
    email: Optional[Union[EmailStr, str]] = ""
    contact_type_id: int
    others_contacts: Optional[str] = None
    lead_type_id: Optional[int] = None       # integer ID of lead type