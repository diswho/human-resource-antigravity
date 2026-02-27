from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.hr import Employee, Department, Position

def get_employees(
    session: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100,
    dept_id: Optional[int] = None,
    pos_id: Optional[int] = None,
    query: Optional[str] = None
) -> List[Employee]:
    statement = select(Employee)
    if dept_id:
        statement = statement.where(Employee.department_id == dept_id)
    if pos_id:
        statement = statement.where(Employee.position_id == pos_id)
    if query:
        statement = statement.where(
            (Employee.firstname.ilike(f"%{query}%")) | 
            (Employee.lastname.ilike(f"%{query}%")) |
            (Employee.emp_pin.ilike(f"%{query}%")) |
            (Employee.lao_name.ilike(f"%{query}%"))
        )
    return session.exec(statement.offset(skip).limit(limit)).all()

def get_employee_by_pin(session: Session, pin: str) -> Optional[Employee]:
    return session.exec(select(Employee).where(Employee.emp_pin == pin)).first()

def get_employee(session: Session, id: int) -> Optional[Employee]:
    return session.get(Employee, id)

def update_employee(session: Session, *, db_emp: Employee, emp_in: dict) -> Employee:
    for field, value in emp_in.items():
        if hasattr(db_emp, field):
            setattr(db_emp, field, value)
    session.add(db_emp)
    session.commit()
    session.refresh(db_emp)
    return db_emp
