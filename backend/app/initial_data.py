from sqlmodel import Session, select, SQLModel
from app.core.db import engine
from app.core.config import settings
from app.crud.user import create_user
from app.models.user import User, UserCreate, UserRole
from app.models.hr import Employee, Department, Position
from app.models.attendance import AttendanceLog  # Required for relationship mapping

def init_db():
    # Ensure tables exist
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                role=UserRole.admin,
            )
            create_user(session=session, user_create=user_in)
            print("Initial superuser created.")
        else:
            print("Initial superuser already exists.")

if __name__ == "__main__":
    init_db()
