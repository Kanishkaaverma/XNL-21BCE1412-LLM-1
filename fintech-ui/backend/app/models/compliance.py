from pydantic import BaseModel
from datetime import datetime

class ComplianceLog(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime
    details: str