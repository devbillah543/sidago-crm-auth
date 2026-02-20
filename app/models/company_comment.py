from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class CompanyComment(Base):
    __tablename__ = "company_comments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="comments")
    user = relationship("User", lazy="joined")
