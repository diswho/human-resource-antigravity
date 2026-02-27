from typing import Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import SessionDep, CurrentUser
from app.crud import attendance as attendance_crud
from app.models.attendance import AttendanceLog

router = APIRouter()


from app.models.hr import Employee
from sqlmodel import select

@router.get("/my", response_model=List[AttendanceLog])
def read_my_attendance(
    current_user: CurrentUser,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Any:
    """
    Retrieve attendance logs for the current logged in employee.
    Requires linking the User to an Employee (not implemented yet, assuming emp_pin match).
    """
    # Placeholder: find employee by email or similar
    # This is a bit simplified; in reality, we'd have a stronger link.
    employee = session.exec(
        select(Employee).where(Employee.emp_pin == current_user.email.split('@')[0])
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee record not linked to user")
        
    return attendance_crud.get_attendance_logs(
        session=session, 
        employee_id=employee.id,
        skip=skip, 
        limit=limit, 
        start_date=start_date, 
        end_date=end_date
    )

@router.get("/{employee_id}", response_model=List[AttendanceLog])
def read_employee_attendance(
    employee_id: int,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Any:
    """
    Retrieve attendance logs for a specific employee (for HR Managers).
    """
    return attendance_crud.get_attendance_logs(
        session=session, 
        employee_id=employee_id,
        skip=skip, 
        limit=limit, 
        start_date=start_date, 
        end_date=end_date
    )
