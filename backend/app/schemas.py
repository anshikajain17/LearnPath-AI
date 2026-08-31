from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class Profile(BaseModel):
    name: str = "Learner"
    goal: str = "Become an AI Engineer in 6 months."
    skills: Dict[str, float] = Field(default_factory=dict)
    interests: List[str] = Field(default_factory=list)
    hours_per_day: float = 2.0
    months: int = 6
    role: Optional[str] = None

class Assessment(BaseModel):
    skill: str
    score: float = Field(ge=0, le=100)

class CoachRequest(BaseModel):
    question: str
    profile: Profile
    roadmap: List[dict] = Field(default_factory=list)

class PlanResponse(BaseModel):
    profile: Profile
    readiness: float
    skill_gaps: List[dict]
    roadmap: List[dict]
    graph: List[dict]
    next_action: dict
    schedule: List[dict]
    projects: List[dict]
    explanation: str
