from sqlalchemy import Boolean, Column, Date, Integer, String

from app.db.session import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    medical_no = Column(String(50), unique=True, index=True, nullable=True)
    stoma_type = Column(String(30), nullable=False)
    surgery_date = Column(Date, nullable=False)
    privacy_authorized = Column(Boolean, default=False, nullable=False)
