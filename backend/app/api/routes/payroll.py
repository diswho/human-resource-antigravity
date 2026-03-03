from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import SessionDep, get_current_active_hr, get_current_user
from app.crud import payroll as payroll_crud
from app.models.payroll import PayrollPublic, PayrollsPublic, Payroll
from app.models.user import User, UserRole
from app.models.hr import Employee
from sqlmodel import select

router = APIRouter()

@router.get("/", response_model=PayrollsPublic)
def read_payrolls(
    session: SessionDep,
    current_user: User = Depends(get_current_active_hr),
    month: int = Query(default=None),
    year: int = Query(default=None),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve payrolls (HR only).
    """
    payrolls = payroll_crud.get_payrolls(session=session, month=month, year=year, skip=skip, limit=limit)
    count = payroll_crud.get_payrolls_count(session=session, month=month, year=year)
    return PayrollsPublic(data=payrolls, count=count)

@router.get("/me", response_model=PayrollsPublic)
def read_my_payrolls(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve own payroll slips.
    """
    if not current_user.employee_id:
        return PayrollsPublic(data=[], count=0)
    
    payrolls = payroll_crud.get_my_payrolls(
        session=session, employee_id=current_user.employee_id, skip=skip, limit=limit
    )
    return PayrollsPublic(data=payrolls, count=len(payrolls))

@router.post("/calculate", response_model=List[PayrollPublic])
def calculate_payrolls(
    session: SessionDep,
    month: int,
    year: int,
    current_user: User = Depends(get_current_active_hr),
) -> Any:
    """
    Trigger payroll calculation for all employees for a given month.
    """
    employees = session.exec(select(Employee)).all()
    results = []
    for emp in employees:
        try:
            payroll = payroll_crud.calculate_monthly_payroll(
                session=session, employee_id=emp.id, month=month, year=year
            )
            results.append(payroll)
        except Exception as e:
            print(f"Failed to calculate for {emp.id}: {e}")
            
    return [PayrollPublic(**p.model_dump()) for p in results]

@router.patch("/{id}", response_model=PayrollPublic)
def update_payroll(
    session: SessionDep,
    id: int,
    payroll_in: dict,
    current_user: User = Depends(get_current_active_hr),
) -> Any:
    """
    Manual adjustments to payroll (HR only).
    """
    db_obj = session.get(Payroll, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Payroll not found")
    
    for field, value in payroll_in.items():
        if hasattr(db_obj, field):
            setattr(db_obj, field, value)
    
    # Recalculate totals
    db_obj.total_earnings = (
        db_obj.base_salary_earned + 
        db_obj.gasoline_allowance + 
        db_obj.bonus_other
    )
    db_obj.total_deductions = (
        db_obj.social_insurance + 
        db_obj.discipline_late + 
        db_obj.discipline_rules + 
        db_obj.discipline_cashier + 
        db_obj.utility_electric + 
        db_obj.utility_water + 
        db_obj.advance_payment + 
        db_obj.security_deposit
    )
    db_obj.net_salary = db_obj.total_earnings - db_obj.total_deductions
    
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return PayrollPublic(**db_obj.model_dump())
