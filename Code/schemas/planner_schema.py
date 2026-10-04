from typing import List, Optional
from pydantic import BaseModel


class DayPlan(BaseModel):
    day: int
    title: str
    activities: List[str] = []
    estimated_cost: Optional[int] = None


class PlannerResponse(BaseModel):
    destination: str
    duration_days: int
    total_estimated_cost: Optional[int] = None
    day_plans: List[DayPlan] = []
    notes: Optional[str] = None