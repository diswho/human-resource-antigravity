from sqlmodel import SQLModel
from app.core.db import engine
# Import all models to ensure they are registered with SQLModel.metadata
from app.models.hr import Employee, Department, Position, SyncState
from app.models.attendance import AttendanceLog
from app.models.user import User

def reset_db():
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Tables dropped successfully.")

if __name__ == "__main__":
    reset_db()
