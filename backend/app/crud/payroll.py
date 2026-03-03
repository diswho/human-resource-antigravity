from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, func
from app.models.payroll import Payroll, PayrollPublic
from app.models.hr import Employee
from app.models.attendance import AttendanceSummary
from app.models.user import User

def get_payrolls(
    session: Session, 
    *, 
    month: Optional[int] = None, 
    year: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[PayrollPublic]:
    statement = select(Payroll, Employee.firstname, Employee.lastname).join(Employee, Payroll.employee_id == Employee.id)
    if month:
        statement = statement.where(Payroll.month == month)
    if year:
        statement = statement.where(Payroll.year == year)
    
    statement = statement.offset(skip).limit(limit).order_by(Payroll.timestamp.desc())
    results = session.exec(statement).all()
    
    return [
        PayrollPublic(**p.model_dump(), employee_name=f"{fn} {ln}")
        for p, fn, ln in results
    ]

def get_payrolls_count(session: Session, *, month: Optional[int] = None, year: Optional[int] = None) -> int:
    statement = select(func.count()).select_from(Payroll)
    if month:
        statement = statement.where(Payroll.month == month)
    if year:
        statement = statement.where(Payroll.year == year)
    return session.exec(statement).one()

def get_my_payrolls(
    session: Session, 
    *, 
    employee_id: int,
    skip: int = 0, 
    limit: int = 100
) -> List[PayrollPublic]:
    statement = (
        select(Payroll)
        .where(Payroll.employee_id == employee_id)
        .order_by(Payroll.year.desc(), Payroll.month.desc())
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()
    return [PayrollPublic(**p.model_dump()) for p in results]

def calculate_monthly_payroll(
    session: Session, 
    *, 
    employee_id: int, 
    month: int, 
    year: int
) -> Payroll:
    # Get employee info
    employee = session.get(Employee, employee_id)
    if not employee:
        raise ValueError("Employee not found")

    # Fetch attendance summaries for the month
    # This is a simplification: assuming 1 record per day in AttendanceSummary
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    summaries = session.exec(
        select(AttendanceSummary)
        .where(AttendanceSummary.employee_id == employee_id)
        .where(AttendanceSummary.date >= start_date)
        .where(AttendanceSummary.date < end_date)
    ).all()

    actual_days = len(summaries)
    total_ot = sum(s.overtime_hours for s in summaries)
    
    # Calculate Earnings
    required_days = 26.0 # Default
    base_earned = (employee.base_salary / required_days) * actual_days
    # OT pay calculation (placeholder: 1.5x hourly rate)
    hourly_rate = (employee.base_salary / required_days) / 8.0
    ot_pay = total_ot * hourly_rate * 1.5
    
    # Create or update payroll record
    existing = session.exec(
        select(Payroll)
        .where(Payroll.employee_id == employee_id)
        .where(Payroll.month == month)
        .where(Payroll.year == year)
    ).first()

    payroll_data = {
        "employee_id": employee_id,
        "month": month,
        "year": year,
        "actual_work_days": actual_days,
        "required_work_days": required_days,
        "ot_hours": total_ot,
        "base_salary_earned": base_earned,
        "gasoline_allowance": employee.gasoline_allowance,
        "bonus_other": ot_pay, # Using OT pay as bonus for now or add a separate field
        "total_earnings": base_earned + employee.gasoline_allowance + ot_pay,
        "net_salary": (base_earned + employee.gasoline_allowance + ot_pay) # - total_deductions (initially 0)
    }

    if existing:
        for key, value in payroll_data.items():
            setattr(existing, key, value)
        db_obj = existing
    else:
        db_obj = Payroll(**payroll_data)
        
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
