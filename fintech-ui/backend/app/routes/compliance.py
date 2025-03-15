from fastapi import APIRouter, Depends, HTTPException
from ..models.compliance import ComplianceLog
from ..utils.auth_utils import get_current_user
from typing import List

router = APIRouter()

mock_compliance_logs = [
    ComplianceLog(
        id=1,
        user_id=1,
        action="Trade Execution",
        timestamp="2023-10-01T12:00:00",
        details="Executed trade for 100 shares of AAPL",
    ),
    ComplianceLog(
        id=2,
        user_id=1,
        action="Portfolio Update",
        timestamp="2023-10-01T12:30:00",
        details="Updated portfolio with new risk parameters",
    ),
    ComplianceLog(
        id=3,
        user_id=2,
        action="Fraud Detection",
        timestamp="2023-10-01T13:00:00",
        details="Detected suspicious activity in account 12345",
    ),
]

@router.get("/logs", response_model=List[ComplianceLog])
async def get_compliance_logs(current_user: dict = Depends(get_current_user)):
    """
    Fetch all compliance logs.
    """
    return mock_compliance_logs

@router.post("/logs", response_model=ComplianceLog)
async def create_compliance_log(
    action: str,
    details: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new compliance log.
    """
    new_log = ComplianceLog(
        id=len(mock_compliance_logs) + 1,
        user_id=current_user.id,
        action=action,
        timestamp="2023-10-01T14:00:00",  # Replace with actual timestamp logic
        details=details,
    )
    mock_compliance_logs.append(new_log)
    return new_log