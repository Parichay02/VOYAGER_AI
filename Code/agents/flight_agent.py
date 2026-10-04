import json
import httpx

from schemas.flight_schema import FlightSearchResponse


class FlightAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "qwen3:4b"

        self.system_prompt = """
You are an AI Flight Search engine for a Travel Assistant. Given source, destination, and any dates, suggest 3 realistic flight options at different price points.

Output rules:
- Return ONLY the JSON object below. No explanation, no markdown, no extra text.
- Use realistic but fictional airline names, not real brand names.
- price is in INR unless otherwise stated.
- Every key must be present.

Schema:
{"source": "", "destination": "", "flights": [{"airline": "", "flight_number": "", "departure_time": "", "arrival_time": "", "duration": "", "price": 0, "stops": 0}], "notes": null}

Example:
Input: {"source": "Delhi", "destination": "Bangalore", "start_date": null, "travelers": null}
Output: {"source": "Delhi", "destination": "Bangalore", "flights": [{"airline": "SkyIndia Air", "flight_number": "SI 204", "departure_time": "06:30", "arrival_time": "09:10", "duration": "2h 40m", "price": 4200, "stops": 0}, {"airline": "BlueWing Airlines", "flight_number": "BW 771", "departure_time": "13:15", "arrival_time": "16:05", "duration": "2h 50m", "price": 3600, "stops": 0}, {"airline": "IndoJet", "flight_number": "IJ 902", "departure_time": "20:00", "arrival_time": "23:30", "duration": "3h 30m", "price": 5100, "stops": 1}], "notes": "Prices are indicative and vary by booking date"}
"""

    async def execute(self, entities: dict) -> FlightSearchResponse:

        user_content = json.dumps(entities)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content},
            ],
            "stream": False,
            "think": False,
            "format": "json",
            "options": {
                "num_predict": 768,
                "num_ctx": 8192
            }
        }

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(self.url, json=payload)

        response.raise_for_status()
        data = response.json()
        llm_output = data["message"]["content"]

        print("=" * 50)
        print("FLIGHT RAW OUTPUT:", llm_output)
        print("=" * 50)

        parsed = json.loads(llm_output)
        return FlightSearchResponse.model_validate(parsed)