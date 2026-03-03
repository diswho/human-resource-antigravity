from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class PayrollBase(SQLModel):
    employee_id: int = Field(foreign_key="employee.id", index=True)
    month: int = Field(index=True)
    year: int = Field(index=True)
    
    # Part A: Work Info
    actual_work_days: float = Field(default=0.0)
    required_work_days: float = Field(default=26.0)
    late_early_minutes: int = Field(default=0)
    ot_hours: float = Field(default=0.0)
    
    # Part B: Earnings (+)
    base_salary_earned: float = Field(default=0.0)
    gasoline_allowance: float = Field(default=0.0)
    bonus_other: float = Field(default=0.0)
    
    # Part C: Deductions (-)
    social_insurance: float = Field(default=0.0)
    discipline_late: float = Field(default=0.0)
    discipline_rules: float = Field(default=0.0)
    discipline_cashier: float = Field(default=0.0)
    utility_electric: float = Field(default=0.0)
    utility_water: float = Field(default=0.0)
    advance_payment: float = Field(default=0.0)
    security_deposit: float = Field(default=0.0)
    
    # Calculated Totals
    total_earnings: float = Field(default=0.0)
    total_deductions: float = Field(default=0.0)
    net_salary: float = Field(default=0.0)
    
    status: str = Field(default="draft", max_length=20) # draft, paid
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Payroll(PayrollBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PayrollPublic(PayrollBase):
    id: int
    employee_name: Optional[str] = None

class PayrollsPublic(SQLModel):
    data: List[PayrollPublic]
    count: int
