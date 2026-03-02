from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.hr import Employee, Department, Position, EmployeePublic
from app.models.user import User, UserRole


def get_all_sub_department_ids(session: Session, dept_id: int) -> List[int]:
    """
    Recursively get all sub-department IDs for a given department ID.
    Includes the parent dept_id itself.
    """
    ids = [dept_id]
    children = session.exec(select(Department.id).where(
        Department.parent_id == dept_id)).all()
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
    statement = select(Employee, User.email).outerjoin(
        User, User.employee_id == Employee.id)

    # RBAC: Employees can only see themselves
    if current_user.role == UserRole.employee:
        if current_user.employee_id:
            statement = statement.where(
                Employee.id == current_user.employee_id)
        else:
            return []  # No linked employee record
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

    out = []
    for emp, email in results:
        emp_dict = emp.model_dump()
        emp_dict["email"] = email
        out.append(EmployeePublic(**emp_dict))

    return out

    return out


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
            statement = statement.where(
                Employee.id == current_user.employee_id)
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


def get_employee(session: Session, id: int) -> Optional[EmployeePublic]:
    statement = select(Employee, User.email).outerjoin(
        User, User.employee_id == Employee.id).where(Employee.id == id)
    result = session.exec(statement).first()
    if not result:
        return None

    emp, email = result
    emp_dict = emp.model_dump()
    emp_dict["email"] = email
    return EmployeePublic(**emp_dict)


def update_employee(session: Session, *, db_emp: Employee, emp_in: dict) -> Employee:
    for field, value in emp_in.items():
        if hasattr(db_emp, field):
            setattr(db_emp, field, value)
    session.add(db_emp)
    session.commit()
    session.refresh(db_emp)
    return db_emp
