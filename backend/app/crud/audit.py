from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.audit import AuditLog, AuditLogPublic
from app.models.user import User

def create_audit_log(
    session: Session, 
    *, 
    user_id: Optional[int], 
    action: str, 
    target_type: str, 
    target_id: Optional[int] = None, 
    details: Optional[dict] = None
) -> AuditLog:
    db_obj = AuditLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_audit_logs(
    session: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100
) -> List[AuditLogPublic]:
    statement = (
        select(AuditLog, User.email)
        .outerjoin(User, AuditLog.user_id == User.id)
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()
    
    return [
        AuditLogPublic(**log.model_dump(), user_email=email)
        for log, email in results
    ]

def get_audit_logs_count(session: Session) -> int:
    return session.exec(select(func.count()).select_from(AuditLog)).one()
