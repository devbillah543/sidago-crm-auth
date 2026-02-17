from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class Timezone(Base):
    __tablename__ = "timezones"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False, index=True)
