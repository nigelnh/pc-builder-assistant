from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from datetime import datetime

class BuildComponentBase(BaseModel):
    name: str
    price: float

class BuildBase(BaseModel):
    name: str
    description: Optional[str] = None
    components: Dict[str, Any]
    total_price: float
    performance_score: Optional[int] = None
    use_case: Optional[str] = None

class BuildCreate(BuildBase):
    pass

class Build(BuildBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BuildResponse(Build):
    pass 