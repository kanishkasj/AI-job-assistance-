from pydantic import BaseModel
from typing import List


class ResumeScore(BaseModel):
    score: int
    missing_skills: List[str]
    suggestions: List[str]
