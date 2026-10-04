import httpx

from schemas.weather_schema import WeatherResponse


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm",
}


class WeatherAgent:

    def __init__(self):
        self.geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"

    async def _geocode(self, location: str, client: httpx.AsyncClient) -> dict:
        response = await client.get(self.geocode_url, params={"name": location, "count": 1})
        response.raise_for_status()
        data = response.json()

        results = data.get("results")
        if not results:
            raise ValueError(f"Could not find location: {location}")

        return results[0]

    async def execute(self, location: str) -> WeatherResponse:
        if not location:
            raise ValueError("No destination provided for weather lookup")

        async with httpx.AsyncClient(timeout=15) as client:
            geo = await self._geocode(location, client)

            forecast_response = await client.get(
                self.forecast_url,
                params={
                    "latitude": geo["latitude"],
                    "longitude": geo["longitude"],
                    "current_weather": True,
                }
            )
            forecast_response.raise_for_status()
            forecast = forecast_response.json()

        current = forecast["current_weather"]
        code = current["weathercode"]
        condition = WEATHER_CODES.get(code, "Unknown conditions")

        return WeatherResponse(
            location=geo.get("name", location),
            latitude=geo["latitude"],
            longitude=geo["longitude"],
            temperature_c=current["temperature"],
            windspeed_kmh=current["windspeed"],
            weathercode=code,
            condition=condition,
            summary=f"{condition}, {current['temperature']}°C, wind {current['windspeed']} km/h in {geo.get('name', location)}"
        )