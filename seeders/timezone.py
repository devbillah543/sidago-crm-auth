from sqlalchemy.orm import Session
from database.db import SessionLocal
from app.models.timezone import Timezone

def get_or_create_timezone(db: Session, id: int, label: str) -> Timezone:
    """
    Check if a timezone with this ID exists.
    If not, create it.
    """
    timezone = db.query(Timezone).filter(Timezone.id == id).first()
    if not timezone:
        timezone = Timezone(id=id, label=label)
        db.add(timezone)
        db.commit()
        db.refresh(timezone)
    return timezone


def run_timezone_seeder():
    db = SessionLocal()
    try:
        # List of tuples (id, label)
        options = [
            (1, "1 - EST"),
            (2, "2 - CST"),
            (3, "3 - MST"),
            (4, "4 - PST"),
        ]

        for tz_id, label in options:
            get_or_create_timezone(db, tz_id, label)

        print("✅ Timezone seeder executed successfully")

    except Exception as e:
        print("❌ Timezone seeder failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_timezone_seeder()
