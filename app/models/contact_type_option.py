from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class ContactTypeOption(Base):
    __tablename__ = "contact_type_options"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False, index=True)