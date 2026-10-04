from typing import Optional
from pydantic import BaseModel


class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    temperature_c: float
    windspeed_kmh: float
    weathercode: int
    condition: str
    summary: str