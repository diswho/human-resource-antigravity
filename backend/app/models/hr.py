from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class DepartmentBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    external_id: Optional[int] = Field(default=None, index=True) # id in hr_department
    dept_code: Optional[int] = Field(default=None, index=True)

class Department(DepartmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    parent: Optional["Department"] = Relationship(
        back_populates="children", 
        sa_relationship_kwargs={"remote_side": "Department.id"}
    )
    children: List["Department"] = Relationship(back_populates="parent")
    employees: List["Employee"] = Relationship(back_populates="department")

class PositionBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    external_id: Optional[int] = Field(default=None, index=True) # position_id in ZKTime

class Position(PositionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employees: List["Employee"] = Relationship(back_populates="position")

class EmployeeBase(SQLModel):
    emp_pin: str = Field(unique=True, index=True, max_length=50)
    firstname: Optional[str] = Field(default=None, max_length=255)
    lastname: Optional[str] = Field(default=None, max_length=255)
    gender: Optional[int] = Field(default=None) # -1=Unknown, 1=Female, 2=Male
    hire_date: Optional[datetime] = Field(default=None)
    external_id: Optional[int] = Field(default=None, index=True) # id in hr_employee
    
    # Extended fields
    lao_name: Optional[str] = Field(default=None, max_length=255)
    bank_account: Optional[str] = Field(default=None, max_length=100)
    gasoline_allowance: float = Field(default=0.0)
    
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    position_id: Optional[int] = Field(default=None, foreign_key="position.id")
    base_salary: float = Field(default=0.0)

class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    department: Optional[Department] = Relationship(back_populates="employees")
    position: Optional[Position] = Relationship(back_populates="employees")
    attendance_logs: List["AttendanceLog"] = Relationship(back_populates="employee")
    user: Optional["User"] = Relationship(back_populates="employee")

class SyncState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    table_name: str = Field(unique=True, index=True)
    last_external_id: int = Field(default=0)
    last_sync: datetime = Field(default_factory=datetime.utcnow)

class EmployeePublic(EmployeeBase):
    id: int
    email: Optional[str] = None
    role: Optional[str] = None

class EmployeesPublic(SQLModel):
    data: List[EmployeePublic]
    count: int

class DepartmentsPublic(SQLModel):
    data: List[Department]
    count: int
