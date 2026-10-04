import json
import httpx

from schemas.hotel_schema import HotelSearchResponse


class HotelAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "qwen3:4b"

        self.system_prompt = """
You are an AI Hotel Search engine for a Travel Assistant. Given trip details, suggest 3 realistic hotel options at different price points (budget, mid-range, luxury).

Output rules:
- Return ONLY the JSON object below. No explanation, no markdown, no extra text.
- Use realistic hotel-style names, not real brand names.
- price_per_night is in INR unless otherwise stated.
- Every key must be present.

Schema:
{"destination": "", "hotels": [{"name": "", "area": "", "price_per_night": 0, "rating": 0.0, "highlights": []}], "notes": null}

Example:
Input: {"destination": "Jaipur", "travelers": 2, "budget": null}
Output: {"destination": "Jaipur", "hotels": [{"name": "Pink City Budget Inn", "area": "Near Hawa Mahal", "price_per_night": 1800, "rating": 3.8, "highlights": ["Free breakfast", "Walking distance to old city"]}, {"name": "Rajwada Heritage Stay", "area": "Civil Lines", "price_per_night": 4500, "rating": 4.3, "highlights": ["Pool", "Traditional decor", "Rooftop restaurant"]}, {"name": "The Amber Grand Palace Hotel", "area": "Amer Road", "price_per_night": 9500, "rating": 4.7, "highlights": ["Spa", "Fort views", "Fine dining"]}], "notes": "Prices are indicative and vary by season"}
"""

    async def execute(self, entities: dict) -> HotelSearchResponse:

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
        print("HOTEL RAW OUTPUT:", llm_output)
        print("=" * 50)

        parsed = json.loads(llm_output)
        return HotelSearchResponse.model_validate(parsed)