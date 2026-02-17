from sqlalchemy.orm import Session
from app.models.contact_type_option import ContactTypeOption

class ContactTypeOptionController:
    @staticmethod
    def get_all_contact_type_options(db: Session):
        """
        Returns all contact type options.
        """
        contact_type_options = db.query(ContactTypeOption).all()
        return [
            {
                "id": cto.id,
                "label": cto.label
            }
            for cto in contact_type_options
        ]
