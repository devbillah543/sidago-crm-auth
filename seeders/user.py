from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.db import SessionLocal
from app.models.user import User
from app.models.role import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    truncated = password.encode("utf-8")[:72].decode("utf-8", "ignore")
    return pwd_context.hash(truncated)


def get_or_create_role(db: Session, role_name: str) -> Role:
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        role = Role(name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    roles: list[Role],
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return

    user = User(
        email=email,
        username=username,
        password=hash_password(password),
        roles=roles,
    )
    db.add(user)
    db.commit()


def run_seeder():
    db = SessionLocal()
    try:
        admin_role = get_or_create_role(db, "admin")
        backoffice_role = get_or_create_role(db, "backoffice")
        agent_role = get_or_create_role(db, "agent")

        # Admin users
        for i in range(1, 4):
            create_user(db, f"admin{i}@example.com", f"admin{i}", "password123", [admin_role])

        # Backoffice users
        for i in range(1, 4):
            create_user(db, f"backoffice{i}@example.com", f"backoffice{i}", "password123", [backoffice_role])

        # Agent users
        for i in range(1, 4):
            create_user(db, f"agent{i}@example.com", f"agent{i}", "password123", [agent_role])

        print("✅ Seeder executed successfully")

    except Exception as e:
        print("❌ Seeder failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_seeder()
