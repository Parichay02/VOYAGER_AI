from typing import List, Optional
from pydantic import BaseModel


class HotelOption(BaseModel):
    name: str
    area: str
    price_per_night: Optional[int] = None
    rating: Optional[float] = None
    highlights: List[str] = []


class HotelSearchResponse(BaseModel):
    destination: str
    hotels: List[HotelOption] = []
    notes: Optional[str] = None