from database.database import Base, engine, get_session
import models
from models.department_model import Department
from models.user_model import User
from auth.password_utils import hash_password
from config import ADMIN_EMAIL, ADMIN_PASSWORD, AGENT_EMAIL, AGENT_PASSWORD


def init_db():
    Base.metadata.create_all(bind=engine)
    db = get_session()
    try:
        if db.query(Department).count() == 0:
            db.add_all([
                Department(name="Operations", description="Operations team"),
                Department(name="Sales", description="Sales team"),
                Department(name="Support", description="Customer support"),
                Department(name="Technology", description="Technical team"),
            ])
            db.commit()

        if db.query(User).count() == 0:
            dept = db.query(Department).filter(Department.name == "Operations").first()
            admin = User(
                full_name="System Moderator",
                email=ADMIN_EMAIL.lower().strip(),
                password_hash=hash_password(ADMIN_PASSWORD),
                role="Moderator",
                department_id=dept.id,
            )
            agent = User(
                full_name="Demo Agent",
                email=AGENT_EMAIL.lower().strip(),
                password_hash=hash_password(AGENT_PASSWORD),
                role="Agent",
                department_id=dept.id,
            )
            db.add_all([admin, agent])
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
