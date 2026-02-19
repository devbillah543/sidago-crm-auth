from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class CompanyCreateRequest(BaseModel):
    name: str
    symbol: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    website: Optional[str] = None
    timezone_id: int