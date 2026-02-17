from sqlalchemy.orm import Session
from database.db import SessionLocal
from app.models.lead_type_option import LeadTypeOption

def get_or_create_lead_type_option(db: Session, label: str) -> LeadTypeOption:
    lead_type_option = db.query(LeadTypeOption).filter(LeadTypeOption.label == label).first()
    if not lead_type_option:
        lead_type_option = LeadTypeOption(label=label)
        db.add(lead_type_option)
        db.commit()
        db.refresh(lead_type_option)
    return lead_type_option


def run_lead_type_option_seeder():
    db = SessionLocal()
    try:
        options = [
            "Hot",
            "General",
        ]

        for label in options:
            get_or_create_lead_type_option(db, label)

        print("✅ LeadTypeOption seeder executed successfully")

    except Exception as e:
        print("❌ LeadTypeOption seeder failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_lead_type_option_seeder()
