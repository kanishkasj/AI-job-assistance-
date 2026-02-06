from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    skills = Column(Text)
    education = Column(Text)
    work_history = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    company_name = Column(String(255))
    job_title = Column(String(255))
    jd_url = Column(Text)
    status = Column(String(100), default="Not Submitted")
    score = Column(Integer, nullable=True)
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
