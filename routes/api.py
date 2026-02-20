# app/routes/api.py

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.controllers.company_comment_controller import CompanyCommentController
from app.controllers.company_controller import CompanyController
from app.controllers.contact_type_controller import ContactTypeOptionController
from app.controllers.lead_type_controller import LeadTypeOptionController
from app.controllers.timezone_controller import TimezoneController
from app.controllers.lead_controller import LeadController
from app.schemas.company_comment_schema import CommentRequest
from app.schemas.company_schema import CompanyCreateRequest
from database.db import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.token import UserToken
from app.controllers.auth_controller import login, logout, refresh_tokens
from app.schemas.auth_schema import LoginRequest
from app.schemas.lead_schema import LeadCreateRequest,LeadUpdateRequest
from app.middlewares.auth_middleware import get_current_user, require_role

router = APIRouter()

# ---------------- Database dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- LOGIN ----------------
@router.post("/login", summary="Login user")
def user_login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user with email & password
    Returns access token, refresh token, and user info
    """
    return login(request.email, request.password, db)


# ---------------- LOGOUT ----------------
@router.post("/logout", summary="Logout user")
def user_logout(
    user: User = Depends(get_current_user),  # Access token validated
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating their access token
    """
    token_record = db.query(UserToken).filter(UserToken.user_id == user.id).first()
    if token_record:
        db.delete(token_record)
        db.commit()

    return {"message": "Logged out successfully"}


# ---------------- REFRESH TOKEN ----------------
class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", summary="Refresh access & refresh tokens")
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """
    Generate new access and refresh tokens using a valid refresh token
    Returns new tokens and user info
    """
    return refresh_tokens(request.refresh_token, db)


# ---------------- GET CURRENT USER ----------------
@router.get("/me", summary="Get current user info")
def get_me(user: User = Depends(get_current_user)):
    """
    Get details of the currently logged-in user
    """
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "roles": [r.name for r in user.roles],
    }


# ---------------- GET AGENT LIST ----------------
@router.get("/agents", summary="Get all agents (admin only)")
def get_agents(
    admin_user: User = Depends(require_role("admin")),  # Only admin can access
    db: Session = Depends(get_db)
):
    """
    Returns a list of all users who have the 'agent' role.
    Accessible only by users with 'admin' role.
    """
    agents = (
        db.query(User)
        .join(User.roles)
        .filter(Role.name == "agent")
        .all()
    )

    return [
        {
            "id": agent.id,
            "email": agent.email,
            "username": agent.username,
            "roles": [role.name for role in agent.roles]
        }
        for agent in agents
    ]

# ---------------- GET ALL LEAD TYPES ----------------
@router.get("/lead-types", summary="Get all lead types (admin only)")
def get_lead_types(
    admin_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Returns all lead type options.
    """
    return LeadTypeOptionController.get_all_lead_type_options(db)

# ---------------- GET ALL CONTACT TYPES ----------------
@router.get("/contact-types", summary="Get all contact types (admin only)")
def get_contact_types(
    admin_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Returns all contact type options.
    """
    return ContactTypeOptionController.get_all_contact_type_options(db)

# ---------------- GET ALL TIMEZONES ----------------
@router.get("/timezones", summary="Get all timezones (admin only)")
def get_timezones(
    admin_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Returns all timezone options.
    """
    return TimezoneController.get_all_timezones(db)

# ---------------- LEADS ----------------
@router.post("/lead", summary="Create a new lead (admin only)")
def create_lead(
    request: LeadCreateRequest,
    admin_user: User = Depends(require_role("admin")),  # Only admin can create
    db: Session = Depends(get_db)
):
    """
    Create a new lead with the provided details.
    Accessible only by users with 'admin' role.
    """
    return LeadController.create_lead_in_db(request, db)

@router.get("/leads", summary="Get all leads (any role)")
def get_leads(
    user: User = Depends(get_current_user),  # Any authenticated user
    db: Session = Depends(get_db)
):
    """
    Fetch all leads from the database and return them as a list of dictionaries.
    Accessible by any authenticated user.
    """
    return LeadController.get_all_leads(db)

# ---------------- GET LEAD BY ID ----------------
@router.get("/lead/{lead_id}", summary="Get a lead by ID (any role)")
def get_lead_by_id(
    lead_id: int,
    user: User = Depends(get_current_user),  # Any authenticated user
    db: Session = Depends(get_db)
):
    """
    Fetch a single lead by its ID.
    Accessible by any authenticated user.
    """
    lead = LeadController.get_lead_by_id(lead_id, db)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

# ---------------- GET LEAD BY AGENT ID ----------------
@router.get("/lead/agent/{agent_id}", summary="Get a lead by agent ID (any role)")
def get_lead_by_agent_id(
    agent_id: int,
    user: User = Depends(get_current_user),  # Any authenticated user
    db: Session = Depends(get_db)
):
    """
    Fetch a single lead by its agent ID.
    Accessible by any authenticated user.
    """
    lead = LeadController.get_leads_for_user(agent_id, db)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


# ---------------- UPDATE LEAD ----------------
@router.put("/lead/{lead_id}", summary="Update a lead by ID (any role)")
def update_lead(
    lead_id: int,
    updates: LeadUpdateRequest,  # Use the Pydantic schema
    user: User = Depends(get_current_user),  # Any authenticated user
    db: Session = Depends(get_db)
):
    """
    Update an existing lead by ID.
    Accessible by any authenticated user.
    Only fields provided in the request will be updated.
    """
    lead = LeadController.update_lead(lead_id, updates, db)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

# ---------------- COMPANY ----------------
@router.get("/companies", summary="Get all companies (admin only)")
def get_companies(
    admin_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Returns all companies.
    """
    return CompanyController.get_all_companies(db)

@router.post("/company", summary="Create a new company (admin only)")
def create_company(
    request: CompanyCreateRequest,
    admin_user: User = Depends(require_role("admin")),  # Only admin can create
    db: Session = Depends(get_db)
):
    """
    Create a new company with the provided details.
    Accessible only by users with 'admin' role.
    """
    return CompanyController.create_company_in_db(request, db)

# ---------------- UPDATE COMPANY ----------------
@router.put("/company/{company_id}", summary="Update a company (admin only)")
def update_company(
    company_id: int,
    request: CompanyCreateRequest,
    admin_user: User = Depends(require_role("admin")),  # Only admin
    db: Session = Depends(get_db)
):
    """
    Update an existing company by ID.
    Accessible only by users with 'admin' role.
    """
    try:
        return CompanyController.update_company(company_id, request, db, current_user=admin_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# ---------------- DELETE COMPANY ----------------
@router.delete("/company/{company_id}", summary="Delete a company (admin only)")
def delete_company(
    company_id: int,
    admin_user: User = Depends(require_role("admin")),  # Only admin
    db: Session = Depends(get_db)
):
    """
    Delete a company by ID.
    Accessible only by users with 'admin' role.
    """
    try:
        return CompanyController.delete_company(company_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ---------------- CREATE COMMENT ----------------
@router.post("/company/{company_id}/comments", summary="Create comment (authenticated)")
def create_comment(
    company_id: int,
    request: CommentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return CompanyCommentController.create_comment(
            company_id,
            request.message,
            db,
            current_user=user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------- GET COMMENTS BY COMPANY ----------------
@router.get("/company/{company_id}/comments", summary="Get comments by company (authenticated)")
def get_comments_by_company(
    company_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CompanyCommentController.get_comments_by_company_id(company_id, db)

# ---------------- GET SINGLE COMMENT ----------------
@router.get("/comments/{comment_id}", summary="Get single comment")
def get_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return CompanyCommentController.get_comment(comment_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ---------------- UPDATE COMMENT ----------------
@router.put("/comments/{comment_id}", summary="Update comment")
def update_comment(
    comment_id: int,
    request: CommentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return CompanyCommentController.update_comment(
            comment_id,
            request.message,
            db,
            current_user=user
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    

# ---------------- DELETE COMMENT ----------------
@router.delete("/comments/{comment_id}", summary="Delete comment")
def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return CompanyCommentController.delete_comment(
            comment_id,
            db,
            current_user=user
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))