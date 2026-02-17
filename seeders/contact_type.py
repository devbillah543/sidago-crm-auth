from sqlalchemy.orm import Session
from database.db import SessionLocal
from app.models.contact_type_option import ContactTypeOption

def get_or_create_contact_type_option(db: Session, label: str) -> ContactTypeOption:
    contact_type_option = db.query(ContactTypeOption).filter(ContactTypeOption.label == label).first()
    if not contact_type_option:
        contact_type_option = ContactTypeOption(label=label)
        db.add(contact_type_option)
        db.commit()
        db.refresh(contact_type_option)
    return contact_type_option


def run_contact_type_option_seeder():
    db = SessionLocal()
    try:
        options = [
            "Validated",
            "Prospecting",
        ]

        for label in options:
            get_or_create_contact_type_option(db, label)

        print("✅ ContactTypeOption seeder executed successfully")

    except Exception as e:
        print("❌ ContactTypeOption seeder failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_contact_type_option_seeder()
