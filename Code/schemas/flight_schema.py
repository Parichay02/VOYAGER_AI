from typing import List, Optional
from pydantic import BaseModel


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration: str
    price: Optional[int] = None
    stops: int = 0


class FlightSearchResponse(BaseModel):
    source: str
    destination: str
    flights: List[FlightOption] = []
    notes: Optional[str] = None