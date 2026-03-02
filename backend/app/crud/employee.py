from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.hr import Employee, Department, Position

def get_all_sub_department_ids(session: Session, dept_id: int) -> List[int]:
    """
    Recursively get all sub-department IDs for a given department ID.
    Includes the parent dept_id itself.
    """
    ids = [dept_id]
    children = session.exec(select(Department.id).where(Department.parent_id == dept_id)).all()
    for child_id in children:
        ids.extend(get_all_sub_department_ids(session, child_id))
    return list(set(ids))

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
        dept_ids = get_all_sub_department_ids(session, dept_id)
        statement = statement.where(Employee.department_id.in_(dept_ids))
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

def get_employees_count(
    session: Session,
    *,
    dept_id: Optional[int] = None,
    pos_id: Optional[int] = None,
    query: Optional[str] = None
) -> int:
    statement = select(func.count()).select_from(Employee)
    if dept_id:
        dept_ids = get_all_sub_department_ids(session, dept_id)
        statement = statement.where(Employee.department_id.in_(dept_ids))
    if pos_id:
        statement = statement.where(Employee.position_id == pos_id)
    if query:
        statement = statement.where(
            (Employee.firstname.ilike(f"%{query}%")) | 
            (Employee.lastname.ilike(f"%{query}%")) |
            (Employee.emp_pin.ilike(f"%{query}%")) |
            (Employee.lao_name.ilike(f"%{query}%"))
        )
    return session.exec(statement).one()

def get_departments(session: Session) -> List[Department]:
    return session.exec(select(Department).order_by(Department.name)).all()

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
