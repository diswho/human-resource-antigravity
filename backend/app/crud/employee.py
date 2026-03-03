from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.hr import Employee, Department, Position, EmployeePublic
from app.models.user import User, UserRole
from app.crud import audit as audit_crud

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
    current_user: User,
    skip: int = 0, 
    limit: int = 100,
    dept_id: Optional[int] = None,
    pos_id: Optional[int] = None,
    query: Optional[str] = None
) -> List[EmployeePublic]:
    statement = select(Employee, User.email).outerjoin(User, Employee.id == User.employee_id)
    
    # RBAC: Employees can only see themselves
    if current_user.role == UserRole.employee:
        if current_user.employee_id:
            statement = statement.where(Employee.id == current_user.employee_id)
        else:
            return [] # No linked employee record
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
    
    results = session.exec(statement.offset(skip).limit(limit)).all()
    
    return [
        EmployeePublic(**emp.model_dump(), email=email)
        for emp, email in results
    ]

def get_employees_count(
    session: Session,
    *,
    current_user: User,
    dept_id: Optional[int] = None,
    pos_id: Optional[int] = None,
    query: Optional[str] = None
) -> int:
    statement = select(func.count()).select_from(Employee)
    
    # RBAC: Employees can only count themselves
    if current_user.role == UserRole.employee:
        if current_user.employee_id:
            statement = statement.where(Employee.id == current_user.employee_id)
        else:
            return 0
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

def update_employee(session: Session, *, db_emp: Employee, emp_in: dict, user_id: Optional[int] = None) -> Employee:
    old_data = db_emp.model_dump()
    changes = {}
    
    for field, value in emp_in.items():
        if hasattr(db_emp, field):
            old_val = getattr(db_emp, field)
            if old_val != value:
                setattr(db_emp, field, value)
                changes[field] = {"old": old_val, "new": value}
    
    session.add(db_emp)
    session.commit()
    session.refresh(db_emp)
    
    if changes:
        audit_crud.create_audit_log(
            session=session,
            user_id=user_id,
            action="update",
            target_type="employee",
            target_id=db_emp.id,
            details=changes
        )
        
    return db_emp
