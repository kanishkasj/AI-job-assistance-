from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: str
    education: str
    work_history: str


class ResumeRequest(BaseModel):
    resume: str
    jd_url: str


class AnswerRequest(BaseModel):
    profile: str
    jd_url: str
    question: str


class JobApplicationCreate(BaseModel):
    user_id: int
    company_name: str
    job_title: str
    jd_url: str
    status: Optional[str] = "Not Submitted"
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    score: Optional[int] = None
    notes: Optional[str] = None


class JobSearchRequest(BaseModel):
    resume: str
    job_query: str
    location: Optional[str] = ""
    min_match_score: Optional[int] = 60
