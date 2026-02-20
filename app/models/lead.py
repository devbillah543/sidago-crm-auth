from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    Text,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from database.db import Base


class Lead(Base):
    __tablename__ = "leads"

    # ======================
    # Primary Key
    # ======================
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        index=True,
    )

    contact_type_id = Column(
        Integer,
        ForeignKey("contact_type_options.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    lead_type_id = Column(
        Integer,
        ForeignKey("lead_type_options.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ======================
    # Identity
    # ======================
    full_name = Column(String(255), index=True)
    role = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(50))
    phone_extension = Column(String(20))
    tool_free_phone = Column(String(50))
    timezone = Column(String(50))
    follow_up_date = Column(Date)
    assigned_to = Column(String(150))
    date_become_hot = Column(String(50))
    others_contacts = Column(Text)

    # ======================
    # Classification
    # ======================
    contact_type_modify_by = Column(String(150))
    not_work_anymore = Column(Boolean, default=False, index=True)
    not_work_modify_by = Column(String(150))
    blocked_email = Column(Boolean, default=False)
    missing_dead_email = Column(Boolean, default=False)

    # ======================
    # Fix Tracking
    # ======================
    old_phones = Column(Text)
    fix_button = Column(String(50))
    fix_button_status = Column(String(50))
    last_fixed_date = Column(Date)
    set_fix_date = Column(Date)

    # ======================
    # Connected Contacts
    # ======================
    connected_contacts = Column(Text)
    connected_contacts_names = Column(Text)
    other_contacts = Column(Text)
    has_other_contacts = Column(Boolean, default=False)
    additional_contacts = Column(Text)
    additional_contact_emails = Column(Text)

    # ======================
    # Counters
    # ======================
    counter_b = Column(Integer, default=0)
    counter_f = Column(Integer, default=0)
    counter_fixes = Column(Integer, default=0)

    # ======================
    # Skip Tracking
    # ======================
    lead_skip_by = Column(String(150))
    lead_skip_notes = Column(Text)

    # ======================
    # Filters & Formulas
    # ======================
    lead_id_end_with = Column(String(10))
    timezone_priority = Column(Integer)
    contacts_filter_formula = Column(Text)
    contacts_filter = Column(Text)
    exclude_canada_filter = Column(Boolean, default=False)
    formula_other_contact = Column(Text)
    filter_value = Column(Text)

    # ======================
    # Metadata
    # ======================
    manual_sort = Column(Integer)
    manual_update = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(150))
    last_modified = Column(DateTime(timezone=True))
    all_leads = Column(Text)
    old_db_calls_code = Column(String(50))
    phone_call = Column(Text)
    test_field = Column(Text)

    # ======================
    # Company Called Today
    # ======================
    company_called_today = Column(Boolean, default=False)
    last_modified_company_called = Column(DateTime(timezone=True))
    last_modified_time_called_today = Column(DateTime(timezone=True))

    # ======================
    # Relationships
    # ======================
    company = relationship("Company", lazy="joined")
    contact_type = relationship("ContactTypeOption", lazy="joined")
    lead_type = relationship("LeadTypeOption", lazy="joined")
    agent = relationship("User", lazy="joined")
