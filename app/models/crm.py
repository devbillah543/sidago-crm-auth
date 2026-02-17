from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Index,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


# ============================================================
# REFERENCE TABLES
# ============================================================

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    team_code = Column(String(20), unique=True, nullable=False)
    team_name = Column(String(100))

    callers = relationship("Caller", back_populates="team", cascade="all, delete-orphan")
    email_senders = relationship("EmailSender", back_populates="team", cascade="all, delete-orphan")


class Caller(Base):
    __tablename__ = "callers"

    caller_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"))

    full_name = Column(String(150))
    name = Column(String(100))
    email = Column(String(255))

    team = relationship("Team", back_populates="callers")


class EmailSender(Base):
    __tablename__ = "email_senders"

    sender_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"))

    sender_name = Column(String(100), nullable=False)
    email = Column(String(255))

    team = relationship("Team", back_populates="email_senders")


class LeadTypeOption(Base):
    __tablename__ = "lead_type_options"

    lead_type_id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False)


class CallResultOption(Base):
    __tablename__ = "call_result_options"

    result_id = Column(Integer, primary_key=True, index=True)
    result_code = Column(String(20), unique=True, nullable=False)
    description = Column(String(255))


class ContactTypeOption(Base):
    __tablename__ = "contact_type_options"

    contact_type_id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False)


# ============================================================
# COMPANIES
# ============================================================

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String(50), unique=True)

    company_symbol = Column(String(20), index=True)
    company_name = Column(String(255), index=True)

    timezone = Column(String(50))
    country = Column(String(100))
    cusip = Column(String(20))
    cik = Column(String(20))
    primary_venue = Column(String(100))
    city = Column(String(100))
    state = Column(String(50))
    zip = Column(String(20))
    website = Column(String(500))
    twitter = Column(String(255))
    description = Column(Text)
    estimated_marketcap = Column(Numeric(18, 2))
    is_otc = Column(Boolean, default=False, index=True)

    # symbol/name change tracking
    previous_company_symbol = Column(String(20))
    backup_company_symbol = Column(String(20))
    last_modified_time_symbol = Column(DateTime(timezone=True))
    last_modified_by_symbol = Column(String(150))

    previous_company_name = Column(String(255))
    backup_company_name = Column(String(255))
    last_modified_time_name = Column(DateTime(timezone=True))
    last_modified_by_name = Column(String(150))

    # metadata
    manual_sort = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(150))
    history_logs = Column(Text)
    five_char_company = Column(String(5))
    only_company_lead = Column(Text)

    # relationships
    leads = relationship("Lead", back_populates="company", cascade="all, delete-orphan")
    additional_contacts = relationship(
        "CompanyAdditionalContact",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    change_history = relationship(
        "CompanyChangeHistory",
        back_populates="company",
        cascade="all, delete-orphan",
    )


# ============================================================
# LEADS
# ============================================================

class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String(50), unique=True)

    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), index=True)
    company_symbol = Column(String(20), index=True)

    # identity
    full_name = Column(String(255), index=True)
    role = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(50))
    phone_extension = Column(String(20))
    tool_free_phone = Column(String(50))
    timezone = Column(String(50))

    # classification
    contact_type_id = Column(Integer, ForeignKey("contact_type_options.contact_type_id"))
    contact_type_modify_by = Column(String(150))
    not_work_anymore = Column(Boolean, default=False, index=True)
    not_work_modify_by = Column(String(150))
    blocked_email = Column(Boolean, default=False)
    missing_dead_email = Column(Boolean, default=False)

    # fix tracking
    old_phones = Column(Text)
    fix_button = Column(String(50))
    fix_button_status = Column(String(50))
    last_fixed_date = Column(Date)
    set_fix_date = Column(Date)

    # connected contacts
    connected_contacts = Column(Text)
    connected_contacts_names = Column(Text)
    other_contacts = Column(Text)
    has_other_contacts = Column(Boolean, default=False)
    additional_contacts = Column(Text)
    additional_contact_emails = Column(Text)

    # counters
    counter_b = Column(Integer, default=0)
    counter_f = Column(Integer, default=0)
    counter_fixes = Column(Integer, default=0)

    # skip tracking
    lead_skip_by = Column(String(150))
    lead_skip_notes = Column(Text)

    # filters & formulas
    lead_id_end_with = Column(String(10))
    timezone_priority = Column(Integer)
    contacts_filter_formula = Column(Text)
    contacts_filter = Column(Text)
    exclude_canada_filter = Column(Boolean, default=False)
    formula_other_contact = Column(Text)
    filter_value = Column(Text)

    # metadata
    manual_sort = Column(Integer)
    manual_update = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(150))
    last_modified = Column(DateTime(timezone=True))
    all_leads = Column(Text)
    old_db_calls_code = Column(String(50))
    phone_call = Column(Text)
    test_field = Column(Text)

    # company called today
    company_called_today = Column(Boolean, default=False)
    last_modified_company_called = Column(DateTime(timezone=True))
    last_modified_time_called_today = Column(DateTime(timezone=True))

    # relationships
    company = relationship("Company", back_populates="leads")
    contact_type = relationship("ContactTypeOption")

    team_tracking = relationship(
        "LeadTeamTracking",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    email_tracking = relationship(
        "LeadEmailTracking",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    call_logs = relationship(
        "CallLog",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    email_logs = relationship(
        "EmailLog",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    sms_logs = relationship(
        "SmsLog",
        back_populates="lead",
        cascade="all, delete-orphan",
    )


# ============================================================
# LEAD TEAM TRACKING
# ============================================================

class LeadTeamTracking(Base):
    __tablename__ = "lead_team_tracking"
    __table_args__ = (
        UniqueConstraint("lead_id", "team_id", name="uq_lead_team"),
        Index("ix_lead_team_tracking_lead_id", "lead_id"),
        Index("ix_lead_team_tracking_team_id", "team_id"),
        Index("ix_lead_team_tracking_lead_type_id", "lead_type_id"),
        Index("ix_lead_team_tracking_follow_up_date", "follow_up_date"),
        Index("ix_lead_team_tracking_date_became_hot", "date_became_hot"),
    )

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)

    # lead classification per team
    lead_type_id = Column(Integer, ForeignKey("lead_type_options.lead_type_id"))
    previous_lead_type_id = Column(Integer, ForeignKey("lead_type_options.lead_type_id"))
    last_modified_time_type = Column(DateTime(timezone=True))
    last_modified_by_type = Column(String(150))

    # call assignment
    to_be_called_by = Column(Integer, ForeignKey("callers.caller_id"))
    last_updated_called_by = Column(DateTime(timezone=True))

    # call tracking
    call_result_id = Column(Integer, ForeignKey("call_result_options.result_id"))
    call_result_code = Column(String(20))
    last_called_date = Column(Date)
    last_called_by = Column(String(150))
    last_called_by_dashboard = Column(String(150))
    follow_up_date = Column(Date)
    next_follow_up_date = Column(Date)
    call_notes = Column(Text)
    history_call_notes = Column(Text)
    history_calls = Column(Text)

    # logging
    to_be_logged = Column(Boolean, default=False)
    good_result_log = Column(Text)

    # hot/ignore tracking
    date_became_hot = Column(Date)
    days_hot = Column(Integer, default=0)
    date_became_ignore = Column(Date)
    days_ignore = Column(Integer, default=0)
    set_cant_locate_date = Column(Date)

    # email tracking
    to_be_sent_email = Column(Boolean, default=False)
    to_be_logged_email = Column(Boolean, default=False)
    checkbox_logged_email = Column(Boolean, default=False)

    # SMS
    sms_log = Column(Text)
    sms_status = Column(String(50))

    # auto-dial
    auto_dial_mighty_call = Column(Text)

    # action tracking
    last_action_date = Column(Date)

    # relationships
    lead = relationship("Lead", back_populates="team_tracking")
    team = relationship("Team")
    lead_type = relationship("LeadTypeOption", foreign_keys=[lead_type_id])
    previous_lead_type = relationship("LeadTypeOption", foreign_keys=[previous_lead_type_id])
    call_result = relationship("CallResultOption")
    assigned_caller = relationship("Caller", foreign_keys=[to_be_called_by])


# ============================================================
# LEAD EMAIL TRACKING
# ============================================================

class LeadEmailTracking(Base):
    __tablename__ = "lead_email_tracking"
    __table_args__ = (
        UniqueConstraint("lead_id", "sender_id", name="uq_lead_sender"),
    )

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("email_senders.sender_id", ondelete="CASCADE"), nullable=False)

    email_status = Column(String(50))
    history_email = Column(Text)

    lead = relationship("Lead", back_populates="email_tracking")
    sender = relationship("EmailSender")


# ============================================================
# COMPANY <-> LEAD ASSOCIATION
# ============================================================

company_leads = Table(
    "company_leads",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), primary_key=True),
    Column("lead_id", Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), primary_key=True),
    Column("is_primary", Boolean, default=False),
)


# ============================================================
# CALL HISTORY LOG
# ============================================================

class CallLog(Base):
    __tablename__ = "call_logs"

    call_log_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False, index=True)
    caller_id = Column(Integer, ForeignKey("callers.caller_id"))
    call_date = Column(DateTime(timezone=True), nullable=False, index=True)
    result_id = Column(Integer, ForeignKey("call_result_options.result_id"))
    result_code = Column(String(20))
    notes = Column(Text)
    logged = Column(Boolean, default=False)

    lead = relationship("Lead", back_populates="call_logs")
    team = relationship("Team")
    caller = relationship("Caller")
    call_result = relationship("CallResultOption")


# ============================================================
# EMAIL SEND LOG
# ============================================================

class EmailLog(Base):
    __tablename__ = "email_logs"

    email_log_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("email_senders.sender_id", ondelete="CASCADE"), nullable=False, index=True)
    sent_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50))
    notes = Column(Text)

    lead = relationship("Lead", back_populates="email_logs")
    sender = relationship("EmailSender")


# ============================================================
# SMS LOG
# ============================================================

class SmsLog(Base):
    __tablename__ = "sms_logs"

    sms_log_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50))
    message = Column(Text)

    lead = relationship("Lead", back_populates="sms_logs")
    team = relationship("Team")


# ============================================================
# COMPANY ADDITIONAL CONTACTS
# ============================================================

class CompanyAdditionalContact(Base):
    __tablename__ = "company_additional_contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), index=True)

    contact_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    role = Column(String(255))
    notes = Column(Text)

    company = relationship("Company", back_populates="additional_contacts")


# ============================================================
# COMPANY CHANGE HISTORY
# ============================================================

class CompanyChangeHistory(Base):
    __tablename__ = "company_change_history"

    change_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False, index=True)
    field_changed = Column(String(50), nullable=False)
    old_value = Column(String(255))
    new_value = Column(String(255))
    changed_by = Column(String(150))
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="change_history")


# ============================================================
# AUTOMATION / REDISTRIBUTION LOG
# ============================================================

class AutomationLog(Base):
    __tablename__ = "automation_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"))
    automation_text = Column(Text)
    trigger_type = Column(String(100))
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(Text)

    lead = relationship("Lead")