from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import SessionDep, get_current_active_superuser
from app.crud import employee as employee_crud
from app.models.hr import Employee, EmployeesPublic, DepartmentsPublic

router = APIRouter()


@router.get("/", response_model=EmployeesPublic)
def read_employees(
    session: SessionDep,
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
        skip=skip, 
        limit=limit, 
        dept_id=dept_id, 
        pos_id=pos_id, 
        query=query
    )
    count = employee_crud.get_employees_count(
        session=session,
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
    emp_in: dict, # Simplified for now, can use a Pydantic model for partial update
    superuser: Any = Depends(get_current_active_superuser),
) -> Any:
    """
    Update an employee's extended information (Lao name, bank account, etc.).
    """
    db_emp = employee_crud.get_employee(session=session, id=id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_crud.update_employee(session=session, db_emp=db_emp, emp_in=emp_in)
