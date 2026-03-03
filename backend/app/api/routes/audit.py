from typing import Any
from fastapi import APIRouter, Depends
from app.api.deps import SessionDep, get_current_active_admin
from app.crud import audit as audit_crud
from app.models.audit import AuditLogsPublic

router = APIRouter()

@router.get("/", response_model=AuditLogsPublic)
def read_audit_logs(
    session: SessionDep,
    admin_user: Any = Depends(get_current_active_admin),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve audit logs (Admin only).
    """
    logs = audit_crud.get_audit_logs(session=session, skip=skip, limit=limit)
    count = audit_crud.get_audit_logs_count(session=session)
    return AuditLogsPublic(data=logs, count=count)
