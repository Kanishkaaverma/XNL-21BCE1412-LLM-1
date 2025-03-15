from fastapi import APIRouter, Depends, HTTPException
from ..utils.auth_utils import get_current_user

router = APIRouter()

@router.post("/execute")
async def execute_trade(asset_type: str, symbol: str, quantity: int, current_user: dict = Depends(get_current_user)):
    """
    Execute a trade for the selected asset type.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Mock trade execution logic
    if asset_type == "stocks":
        # Execute stock trade
        return {"status": f"Executed trade for {quantity} shares of {symbol} (Stocks)"}
    elif asset_type == "crypto":
        # Execute crypto trade
        return {"status": f"Executed trade for {quantity} units of {symbol} (Crypto)"}
    elif asset_type == "forex":
        # Execute forex trade
        return {"status": f"Executed trade for {quantity} units of {symbol} (Forex)"}
    else:
        raise HTTPException(status_code=400, detail="Invalid asset type")