from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.company import Company
from app.schemas.company_schema import CompanyCreateRequest


class CompanyController:

    @staticmethod
    def get_all_companies(db: Session):
        companies = db.query(Company).all()
        return [
            {
                "id": company.id,
                "name": company.name,
                "symbol": company.symbol,
                "country": company.country,
                "state": company.state,
                "city": company.city,
                "zip": company.zip,
                "timezone": company.timezone.label if company.timezone else None
            }
            for company in companies
        ]

    @staticmethod
    def create_company_in_db(request: CompanyCreateRequest, db: Session):
        # 🔎 Check if name already exists
        existing = db.query(Company).filter(Company.name == request.name).first()
        if existing:
            raise ValueError("Company name already exists")

        # 🔤 Auto-generate symbol if not provided
        symbol = request.symbol
        if not symbol:
            symbol = request.name[:3].upper()

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
            raise ValueError("Company name must be unique")

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

    # ✅ UPDATE
    @staticmethod
    def update_company(company_id: int, request: CompanyCreateRequest, db: Session):
        company = db.query(Company).filter(Company.id == company_id).first()

        if not company:
            raise ValueError("Company not found")

        # Check unique name (excluding self)
        existing = (
            db.query(Company)
            .filter(Company.name == request.name, Company.id != company_id)
            .first()
        )
        if existing:
            raise ValueError("Company name already exists")

        # Auto-generate symbol if empty
        symbol = request.symbol
        if not symbol:
            symbol = request.name[:3].upper()

        company.name = request.name
        company.symbol = symbol
        company.country = request.country
        company.state = request.state
        company.city = request.city
        company.zip = request.zip
        company.website = request.website
        company.timezone_id = request.timezone_id

        db.commit()
        db.refresh(company)

        return {
            "id": company.id,
            "name": company.name,
            "symbol": company.symbol,
            "country": company.country,
            "state": company.state,
            "city": company.city,
            "zip": company.zip,
            "timezone": company.timezone.label if company.timezone else None
        }

    # ✅ DELETE
    @staticmethod
    def delete_company(company_id: int, db: Session):
        company = db.query(Company).filter(Company.id == company_id).first()

        if not company:
            raise ValueError("Company not found")

        db.delete(company)
        db.commit()

        return {"message": "Company deleted successfully"}
