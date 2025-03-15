from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    id: int
    user_id: int
    symbol: str
    quantity: int
    price: float
    timestamp: datetime