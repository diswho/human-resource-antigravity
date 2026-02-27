import sqlite3
from sqlmodel import Session, select, SQLModel, func
from app.core.db import engine
from app.models.hr import Employee, Department, Position, SyncState
from app.models.attendance import AttendanceLog, AttendanceSummary
from app.models.user import User, UserCreate
from app.crud.user import create_user
from datetime import datetime, timezone
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the local SQLite DB (should be mounted in Docker)
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "/app/ZKTimeNet08.db")

def get_last_sync_id(session: Session, table_name: str) -> int:
    state = session.exec(select(SyncState).where(SyncState.table_name == table_name)).first()
    if not state:
        state = SyncState(table_name=table_name, last_external_id=0)
        session.add(state)
        session.commit()
        session.refresh(state)
    return state.last_external_id

def update_last_sync_id(session: Session, table_name: str, last_id: int):
    state = session.exec(select(SyncState).where(SyncState.table_name == table_name)).first()
    if state:
        state.last_external_id = last_id
        state.last_sync = datetime.now(timezone.utc).replace(tzinfo=None)
        session.add(state)
        session.commit()

def sync_departments(sqlite_cursor, session: Session):
    sqlite_cursor.execute("SELECT id, dept_name FROM hr_department")
    count = 0
    for d_id, d_name in sqlite_cursor.fetchall():
        db_dept = session.exec(select(Department).where(Department.external_id == d_id)).first()
        if not db_dept:
            db_dept = Department(name=d_name, external_id=d_id)
        else:
            db_dept.name = d_name
        session.add(db_dept)
        count += 1
    session.commit()
    logger.info(f"Synced {count} Departments.")

def sync_positions(sqlite_cursor, session: Session):
    sqlite_cursor.execute("SELECT id, posi_name FROM hr_position")
    count = 0
    for p_id, p_name in sqlite_cursor.fetchall():
        db_pos = session.exec(select(Position).where(Position.external_id == p_id)).first()
        if not db_pos:
            db_pos = Position(name=p_name, external_id=p_id)
        else:
            db_pos.name = p_name
        session.add(db_pos)
        count += 1
    session.commit()
    logger.info(f"Synced {count} Positions.")

def sync_employees(sqlite_cursor, session: Session):
    sqlite_cursor.execute("""
        SELECT id, emp_pin, emp_firstname, emp_lastname, emp_gender, emp_hiredate, department_id, position_id 
        FROM hr_employee
    """)
    count = 0
    for e_id, pin, fname, lname, gender, hdate, d_id, p_id in sqlite_cursor.fetchall():
        db_emp = session.exec(select(Employee).where(Employee.external_id == e_id)).first()
        if not db_emp:
            # Fallback to pin if external_id not set yet
            db_emp = session.exec(select(Employee).where(Employee.emp_pin == pin)).first()
        
        dept = session.exec(select(Department).where(Department.external_id == d_id)).first()
        pos = session.exec(select(Position).where(Position.external_id == p_id)).first()
        
        hire_date = None
        if hdate:
            try: hire_date = datetime.strptime(hdate, "%Y-%m-%d %H:%M:%S")
            except: pass

        if not db_emp:
            db_emp = Employee(
                emp_pin=pin,
                firstname=fname,
                lastname=lname,
                gender=gender,
                hire_date=hire_date,
                external_id=e_id,
                department_id=dept.id if dept else None,
                position_id=pos.id if pos else None
            )
        else:
            db_emp.emp_pin = pin
            db_emp.firstname = fname
            db_emp.lastname = lname
            db_emp.gender = gender
            db_emp.hire_date = hire_date
            db_emp.external_id = e_id
            db_emp.department_id = dept.id if dept else None
            db_emp.position_id = pos.id if pos else None
            
        session.add(db_emp)
        count += 1
    session.commit()
    logger.info(f"Synced {count} Employees.")

def sync_users_from_employees(sqlite_cursor, session: Session):
    # Fetch employees who don't have a user account yet
    # We use a subquery to find employees without linked users
    employees = session.exec(select(Employee)).all()
    count = 0
    for emp in employees:
        db_user = session.exec(select(User).where(User.employee_id == emp.id)).first()
        if not db_user:
            # Try to get email from SQLite
            sqlite_cursor.execute("SELECT emp_email FROM hr_employee WHERE id = ?", (emp.external_id,))
            row = sqlite_cursor.fetchone()
            
            email = row[0] if row and row[0] else f"{emp.emp_pin}@internal.com"
            
            # Check for email conflicts
            existing_user = session.exec(select(User).where(User.email == email)).first()
            if existing_user:
                email = f"{emp.emp_pin}.{emp.id}@internal.com"
            
            user_in = UserCreate(
                email=email,
                password=f"password_{emp.emp_pin}" if len(emp.emp_pin) >= 3 else f"password_emp_{emp.emp_pin}",
                full_name=f"{emp.firstname} {emp.lastname}" if emp.firstname else emp.emp_pin,
                employee_id=emp.id
            )
            try:
                create_user(session=session, user_create=user_in)
                count += 1
            except Exception as e:
                logger.error(f"Failed to create user for employee {emp.emp_pin}: {e}")
                session.rollback()
                
    session.commit()
    if count > 0:
        logger.info(f"Created {count} new system user accounts for employees.")

def migrate_data():
    if not os.path.exists(SQLITE_DB_PATH):
        logger.error(f"Error: SQLite database not found at {SQLITE_DB_PATH}")
        return

    # Ensure tables exist in Postgres
    SQLModel.metadata.create_all(engine)

    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_cursor = sqlite_conn.cursor()
    except Exception as e:
        logger.error(f"Failed to connect to SQLite: {e}")
        return

    with Session(engine) as session:
        # Check sys_log for any changes in Dept, Position, Employee
        last_log_id = get_last_sync_id(session, "sys_log")
        sqlite_cursor.execute("SELECT MAX(id) FROM sys_log")
        row = sqlite_cursor.fetchone()
        max_log_id = row[0] if row and row[0] else 0
        
        should_sync_users = False
        
        if max_log_id > last_log_id:
            logger.info(f"New sys_log entries found (last: {last_log_id}, max: {max_log_id}). Checking for relevant changes...")
            
            sqlite_cursor.execute("""
                SELECT DISTINCT TableName FROM sys_log 
                WHERE id > ? AND TableName IN ('Department', 'Position', 'Employee')
            """, (last_log_id,))
            
            changed_tables = [row[0] for row in sqlite_cursor.fetchall()]
            
            if 'Department' in changed_tables:
                sync_departments(sqlite_cursor, session)
            if 'Position' in changed_tables:
                sync_positions(sqlite_cursor, session)
            if 'Employee' in changed_tables:
                sync_employees(sqlite_cursor, session)
                should_sync_users = True
            
            # If it's the first time
            if last_log_id == 0:
                sync_departments(sqlite_cursor, session)
                sync_positions(sqlite_cursor, session)
                sync_employees(sqlite_cursor, session)
                should_sync_users = True

            update_last_sync_id(session, "sys_log", max_log_id)
        else:
            logger.info("No new changes detected in sys_log.")

        # Always run user sync if explicitly requested or first time
        # Or if we just synced employees
        if should_sync_users or last_log_id == 0:
            sync_users_from_employees(sqlite_cursor, session)

        # 4. Migrate Attendance Logs (Incremental by ID)
        max_att_id_stmt = select(func.max(AttendanceLog.external_id))
        max_att_id_res = session.exec(max_att_id_stmt).first()
        last_att_external_id = max_att_id_res if max_att_id_res is not None else 0

        sqlite_cursor.execute(
            "SELECT id, employee_id, punch_time, punch_type, terminal_id FROM att_punches WHERE id > ? ORDER BY id ASC LIMIT 5000", 
            (last_att_external_id,)
        )
        
        logs = sqlite_cursor.fetchall()
        if logs:
            logger.info(f"Syncing {len(logs)} new Attendance Logs...")
            log_count = 0
            for log_id, e_id_ext, p_time, p_type, t_id in logs:
                # Match employee by external_id (id in hr_employee)
                db_emp = session.exec(select(Employee).where(Employee.external_id == e_id_ext)).first()
                if not db_emp:
                    continue

                ts = datetime.strptime(p_time, "%Y-%m-%d %H:%M:%S")
                session.add(AttendanceLog(
                    timestamp=ts,
                    punch_type=str(p_type),
                    terminal_id=t_id,
                    external_id=log_id,
                    employee_id=db_emp.id
                ))
                log_count += 1
            
            session.commit()
            logger.info(f"Successfully synced {log_count} new Attendance Logs.")
        else:
            logger.info("No new Attendance Logs.")

    sqlite_conn.close()

if __name__ == "__main__":
    migrate_data()
