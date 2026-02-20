from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.company import Company
from app.models.company_history import CompanyHistory
from app.schemas.company_schema import CompanyCreateRequest


class CompanyController:

    # =========================
    # GET ALL COMPANIES
    # =========================
    @staticmethod
    def get_all_companies(db: Session):
        companies = db.query(Company).order_by(desc(Company.id)).all()

        result = []
        for company in companies:
            histories = [h.history for h in company.histories]

            result.append({
                "id": company.id,
                "name": company.name,
                "symbol": company.symbol,
                "country": company.country,
                "state": company.state,
                "city": company.city,
                "zip": company.zip,
                "website": company.website,
                "timezone_id": company.timezone_id,
                "timezone": company.timezone.label if company.timezone else None,
                "previous_company_name": company.previous_company_name,
                "previous_company_symbol": company.previous_company_symbol,
                "histories": histories
            })

        return result

    # =========================
    # CREATE COMPANY
    # =========================
    @staticmethod
    def create_company_in_db(request: CompanyCreateRequest, db: Session):
        # Check if company name already exists
        existing = db.query(Company).filter(Company.name == request.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Company name already exists")

        # Auto-generate symbol if not provided
        symbol = request.symbol or request.name[:3].upper()

        new_company = Company(
            name=request.name,
            symbol=symbol,
            country=request.country,
            city=request.city,
            state=request.state,
            zip=request.zip,
            website=request.website,
            timezone_id=request.timezone_id,
        )

        try:
            db.add(new_company)
            db.commit()
            db.refresh(new_company)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Company name must be unique")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        return {
            "id": new_company.id,
            "name": new_company.name,
            "symbol": new_company.symbol,
            "country": new_company.country,
            "state": new_company.state,
            "city": new_company.city,
            "zip": new_company.zip,
            "timezone": new_company.timezone.label if new_company.timezone else None
        }

    # =========================
    # UPDATE COMPANY
    # =========================
    @staticmethod
    def update_company(company_id: int, request: CompanyCreateRequest, db: Session, current_user=None):
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        # Unique name check
        existing = db.query(Company).filter(Company.name == request.name, Company.id != company_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Company name already exists")

        symbol = request.symbol or request.name[:3].upper()
        now = datetime.utcnow()
        username = current_user.username if current_user else "System"

        # Prepare history
        history_parts = []

        # Name change
        if company.name != request.name:
            company.previous_company_name = company.name
            company.backup_company_name = request.name
            company.last_modified_time_name = now
            company.last_modified_by_name = username
            history_parts.append(f"name {company.name} to {request.name}")

        # Symbol change
        if company.symbol != symbol:
            company.previous_company_symbol = company.symbol
            company.backup_company_symbol = symbol
            company.last_modified_time_symbol = now
            company.last_modified_by_symbol = username
            history_parts.append(f"symbol {company.symbol} to {symbol}")

        # Other fields
        fields_to_track = ["country", "state", "city", "zip", "website", "timezone_id"]
        for field in fields_to_track:
            old_value = getattr(company, field)
            new_value = getattr(request, field, None)
            if old_value != new_value:
                setattr(company, field, new_value)
                history_parts.append(f"{field} {old_value} to {new_value}")

        company.name = request.name
        company.symbol = symbol

        # Save history
        if history_parts:
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            history_text = f"{now_str} - Modified by {username} - Company " + ", ".join(history_parts)
            history_record = CompanyHistory(
                company_id=company.id,
                user_id=current_user.id if current_user else None,
                history=history_text,
                changed_at=now
            )
            db.add(history_record)

        # Commit
        try:
            db.commit()
            db.refresh(company)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        return {
            "id": company.id,
            "name": company.name,
            "symbol": company.symbol,
            "country": company.country,
            "state": company.state,
            "city": company.city,
            "zip": company.zip,
            "website": company.website,
            "timezone": company.timezone.label if company.timezone else None
        }

    # =========================
    # DELETE COMPANY
    # =========================
    @staticmethod
    def delete_company(company_id: int, db: Session):
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        db.delete(company)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        return {"message": "Company deleted successfully"}