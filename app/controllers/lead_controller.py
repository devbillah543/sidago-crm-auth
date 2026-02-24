# lead_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.lead import Lead
from app.schemas.lead_schema import LeadCreateRequest, LeadUpdateRequest


class LeadController:

    @staticmethod
    def create_lead_in_db(request: LeadCreateRequest, db: Session):
        """
        Create a lead in the database using provided company_id.
        """

        lead = Lead(
            full_name=request.full_name,
            company_id=request.company_id,
            role=request.role,
            phone=request.phone,
            email=request.email if request.email else None,
            others_contacts=request.others_contacts if request.others_contacts else None,
            contact_type_id=request.contact_type_id,
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)

        return LeadController._serialize_lead(lead)

    @staticmethod
    def update_lead(lead_id: int, updates: LeadUpdateRequest, db: Session):
        """
        Update an existing lead by ID with provided fields, including company_id.
        """
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Update only fields present in LeadUpdateRequest
        update_fields = [
            "full_name", "role", "phone", "email",
            "others_contacts", "company_id", "contact_type_id"
        ]

        for field in update_fields:
            value = getattr(updates, field)
            if value is not None:
                setattr(lead, field, value)

        db.commit()
        db.refresh(lead)

        return LeadController._serialize_lead(lead)

    @staticmethod
    def get_all_leads(db: Session):
        leads = db.query(Lead).all()
        return [LeadController._serialize_lead(lead) for lead in leads]

    @staticmethod
    def get_lead_by_id(lead_id: int, db: Session):
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None
        return LeadController._serialize_lead(lead)

    @staticmethod
    def get_leads_for_user(user_id: int, db: Session):
        leads = db.query(Lead).filter(Lead.user_id == user_id).all()
        return [LeadController._serialize_lead(lead) for lead in leads]

    @staticmethod
    def _serialize_lead(lead: Lead):
        """
        Helper method to serialize lead with full company + timezone data,
        and generate a custom lead_id in the format: COMPANYNAME-FULLNAME
        """
        company_data = None
        company_name_safe = ""
        if lead.company:
            company_data = {
                "id": lead.company.id,
                "name": lead.company.name,
                "symbol": lead.company.symbol,
                "timezone": lead.company.timezone.label if lead.company.timezone else None,
            }
            company_name_safe = lead.company.symbol

        full_name_safe = lead.full_name

        return {
            "id": lead.id,
            "lead_id": f"{company_name_safe}-{full_name_safe}",
            "full_name": lead.full_name,
            "role": lead.role,
            "phone": lead.phone,
            "email": lead.email,
            "assigned_to": getattr(lead, "assigned_to", None),
            "agent": lead.agent.username if getattr(lead, "agent", None) else None,
            "follow_up_date": getattr(lead, "follow_up_date", None),
            "lead_type": lead.lead_type.label if getattr(lead, "lead_type", None) else None,
            "contact_type": lead.contact_type.label if getattr(lead, "contact_type", None) else None,
            "date_become_hot": getattr(lead, "date_become_hot", None),
            "others_contacts": getattr(lead, "others_contacts", None),
            "company": company_data
        }