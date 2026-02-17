# app/controllers/lead_controller.py

from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.models.company import Company
from app.schemas.lead_schema import LeadCreateRequest, LeadUpdateRequest
from datetime import datetime
from typing import Optional, Dict, Any

class LeadController:

    @staticmethod
    def create_lead_in_db(request: LeadCreateRequest, db: Session):
        """
        Create a lead in the database.
        If the company does not exist, create it first.
        """

        # ------------------ Ensure company exists ------------------
        company = db.query(Company).filter(Company.name == request.company).first()
        if not company:
            company = Company(
                name=request.company,
                symbol=request.company[:3].upper() if len(request.company) >= 3 else request.company.upper(),
                timezone_id=1,
            )
            db.add(company)
            db.commit()
            db.refresh(company)

        # ------------------ Create lead ------------------
        lead = Lead(
            full_name=request.full_name,
            user_id=request.agent_id,
            role=request.role,
            phone=request.phone,
            email=request.email,
            follow_up_date=request.follow_up_date,
            assigned_to=request.assigned_to,
            lead_type_id=request.lead_type_id,
            contact_type_id=request.contact_type_id,
            date_become_hot=request.date_become_hot,
            company_id=company.id
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)

        return {
            "id": lead.id,
            "full_name": lead.full_name,
            "company": lead.company.name if lead.company else None,
            "role": lead.role,
            "email": lead.email,
            "assigned_to": lead.assigned_to,
            "agent": lead.agent.username if lead.agent else None,
            "follow_up_date": lead.follow_up_date,
            "lead_type": lead.lead_type.label if lead.lead_type else None,
            "contact_type": lead.contact_type.label if lead.contact_type else None,
            "date_become_hot": lead.date_become_hot,
        }

    @staticmethod
    def get_all_leads(db: Session):
        leads = db.query(Lead).all()
        result = []

        for lead in leads:
            result.append({
                "id": lead.id,
                "full_name": lead.full_name,
                "company": lead.company.name if lead.company else None,
                "role": lead.role,
                "email": lead.email,
                "assigned_to": lead.assigned_to,
                "agent": lead.agent.username if lead.agent else None,
                "follow_up_date": lead.follow_up_date,
                "lead_type": lead.lead_type.label if lead.lead_type else None,
                "contact_type": lead.contact_type.label if lead.contact_type else None,
                "date_become_hot": lead.date_become_hot,
            })

        return result

    @staticmethod
    def get_lead_by_id(lead_id: int, db: Session):
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None

        return {
            "id": lead.id,
            "full_name": lead.full_name,
            "company": lead.company.name if lead.company else None,
            "role": lead.role,
            "email": lead.email,
            "assigned_to": lead.assigned_to,
            "agent": lead.agent.username if lead.agent else None,
            "follow_up_date": lead.follow_up_date,
            "lead_type": lead.lead_type.label if lead.lead_type else None,
            "contact_type": lead.contact_type.label if lead.contact_type else None,
            "date_become_hot": lead.date_become_hot,
        }
    
    @staticmethod
    def get_leads_for_user(user_id: int, db: Session):
        """
        Fetch all leads assigned to a specific user.
        """
        leads = db.query(Lead).filter(Lead.user_id == user_id).all()
        result = []

        for lead in leads:
            result.append({
                "id": lead.id,
                "full_name": lead.full_name,
                "company": lead.company.name if lead.company else None,
                "role": lead.role,
                "email": lead.email,
                "assigned_to": lead.assigned_to,
                "agent": lead.agent.username if lead.agent else None,
                "follow_up_date": lead.follow_up_date,
                "lead_type": lead.lead_type.label if lead.lead_type else None,
                "contact_type": lead.contact_type.label if lead.contact_type else None,
                "date_become_hot": lead.date_become_hot,
            })

        return result

    @staticmethod
    def update_lead(lead_id: int, updates: LeadUpdateRequest, db: Session):
        """
        Update an existing lead by ID with provided fields, including company
        """
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None

        # ------------------ Handle company update ------------------
        if updates.company:
            company = db.query(Company).filter(Company.name == updates.company).first()
            if not company:
                company = Company(
                    name=updates.company,
                    symbol=updates.company[:3].upper() if len(updates.company) >= 3 else updates.company.upper(),
                    timezone_id=1
                )
                db.add(company)
                db.commit()
                db.refresh(company)
            lead.company_id = company.id

        # ------------------ Update other allowed fields ------------------
        allowed_fields = [
            "full_name", "role", "phone", "email", "follow_up_date",
            "assigned_to", "lead_type_id", "contact_type_id", "date_become_hot"
        ]

        for field in allowed_fields:
            value = getattr(updates, field)
            if value is not None:
                setattr(lead, field, value)

        db.commit()
        db.refresh(lead)

        return {
            "id": lead.id,
            "full_name": lead.full_name,
            "company": lead.company.name if lead.company else None,
            "role": lead.role,
            "email": lead.email,
            "assigned_to": lead.assigned_to,
            "agent": lead.agent.username if lead.agent else None,
            "follow_up_date": lead.follow_up_date,
            "lead_type": lead.lead_type.label if lead.lead_type else None,
            "contact_type": lead.contact_type.label if lead.contact_type else None,
            "date_become_hot": lead.date_become_hot,
        }
