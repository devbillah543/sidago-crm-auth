from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from database.db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), unique=True, nullable=False, index=True)
    symbol = Column(String(20), index=True)

    # Foreign Keys
    timezone_id = Column(
        Integer,
        ForeignKey("timezones.id", ondelete="CASCADE"),
        index=True,
    )
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

    # Symbol Change Tracking
    previous_company_symbol = Column(String(20))
    backup_company_symbol = Column(String(20))
    last_modified_time_symbol = Column(DateTime(timezone=True))
    last_modified_by_symbol = Column(String(150))

    # Name Change Tracking
    previous_company_name = Column(String(255))
    backup_company_name = Column(String(255))
    last_modified_time_name = Column(DateTime(timezone=True))
    last_modified_by_name = Column(String(150))

    # Relationships
    timezone = relationship("Timezone", lazy="joined")
