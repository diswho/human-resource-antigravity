from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.crud import employee as employee_crud
from app.models.hr import Employee, EmployeesPublic, DepartmentsPublic
from app.models.user import UserRole

router = APIRouter()


@router.get("/", response_model=EmployeesPublic)
def read_employees(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    dept_id: Optional[int] = None,
    pos_id: Optional[int] = None,
    query: Optional[str] = None,
) -> Any:
    """
    Retrieve employees with pagination and filtering.
    """
    employees = employee_crud.get_employees(
        session=session, 
        current_user=current_user,
        skip=skip, 
        limit=limit, 
        dept_id=dept_id, 
        pos_id=pos_id, 
        query=query
    )
    count = employee_crud.get_employees_count(
        session=session,
        current_user=current_user,
        dept_id=dept_id,
        pos_id=pos_id,
        query=query
    )
    return EmployeesPublic(data=employees, count=count)


@router.get("/departments", response_model=DepartmentsPublic)
def read_departments(session: SessionDep) -> Any:
    """
    Retrieve all departments.
    """
    departments = employee_crud.get_departments(session=session)
    return DepartmentsPublic(data=departments, count=len(departments))


@router.get("/{id}", response_model=Employee)
def read_employee_by_id(
    id: int,
    session: SessionDep,
) -> Any:
    """
    Get employee by ID.
    """
    employee = employee_crud.get_employee(session=session, id=id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/{id}", response_model=Employee)
def update_employee(
    id: int,
    session: SessionDep,
    emp_in: dict,
    current_user: CurrentUser,
) -> Any:
    """
    Update an employee's extended information.
    """
    db_emp = employee_crud.get_employee(session=session, id=id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # RBAC rules for editing
    if current_user.role == UserRole.employee:
        if current_user.employee_id != id:
            raise HTTPException(status_code=403, detail="You can only edit your own personal information")
        # Employee can only edit specific personal fields
        allowed_fields = {"lao_name", "bank_account"}
        emp_in = {k: v for k, v in emp_in.items() if k in allowed_fields}
    elif current_user.role not in [UserRole.admin, UserRole.hr]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    return employee_crud.update_employee(session=session, db_emp=db_emp, emp_in=emp_in, user_id=current_user.id)
