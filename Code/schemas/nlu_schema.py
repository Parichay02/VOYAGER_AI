from typing import List, Optional

from pydantic import BaseModel, field_validator


INTENT_ALIASES = {
    "plan_trip": "plan_trip",
    "trip_planning": "plan_trip",
    "planning": "plan_trip",
    "plan_a_trip": "plan_trip",
    "book_trip": "plan_trip",

    "weather": "weather",
    "check_weather": "weather",
    "weather_check": "weather",

    "hotel_search": "hotel_search",
    "hotel": "hotel_search",
    "book_hotel": "hotel_search",
    "find_hotel": "hotel_search",
    "accommodation": "hotel_search",

    "flight_search": "flight_search",
    "flight": "flight_search",
    "book_flight": "flight_search",
    "find_flight": "flight_search",

    "general": "general",
    "greeting": "general",
    "smalltalk": "general",
    "small_talk": "general",
}

class Entities(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: Optional[int] = None
    budget: Optional[int] = None
    travelers: Optional[int] = None
    interests: List[str] = []
    trip_type: Optional[str] = None
    travel_style: Optional[str] = None


class NLUResponse(BaseModel):
    intent: str  # plain string, no enum — normalized but not restricted
    confidence: float = 0.5
    entities: Entities
    missing_fields: List[str] = []

    @field_validator("intent", mode="before")
    @classmethod
    def normalize_intent(cls, v):
        if not isinstance(v, str) or not v.strip():
            return "general"
        key = v.strip().lower().replace(" ", "_").replace("-", "_")
        return INTENT_ALIASES.get(key, key)  # unknown values pass through as-is instead of forcing "general"

    @field_validator("confidence", mode="before")
    @classmethod
    def clamp_confidence(cls, v):
        try:
            return max(0.0, min(1.0, float(v)))
        except (TypeError, ValueError):
            return 0.5