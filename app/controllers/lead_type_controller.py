from sqlalchemy.orm import Session
from app.models.lead_type_option import LeadTypeOption

class LeadTypeOptionController:
    @staticmethod
    def get_all_lead_type_options(db: Session):
        """
        Returns all lead type options.
        """
        lead_type_options = db.query(LeadTypeOption).all()
        return [
            {
                "id": lto.id,
                "label": lto.label
            }
            for lto in lead_type_options
        ]
