import json
import httpx

from schemas.planner_schema import PlannerResponse


class PlannerAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "qwen3:4b"

        self.system_prompt = """
You are an AI Trip Planning engine for a Travel Assistant. Given trip details, create a realistic day-by-day itinerary.

Output rules:
- Return ONLY the JSON object below. No explanation, no markdown, no extra text.
- If duration_days is missing, default to 3.
- Keep activities realistic and concise (2-4 per day).
- Every key must be present.

Schema:
{"destination": "", "duration_days": 0, "total_estimated_cost": null, "day_plans": [{"day": 1, "title": "", "activities": [], "estimated_cost": null}], "notes": null}

Example:
Input: {"destination": "Goa", "duration_days": 3, "budget": 20000, "interests": ["beaches", "nightlife"]}
Output: {"destination": "Goa", "duration_days": 3, "total_estimated_cost": 18000, "day_plans": [{"day": 1, "title": "Arrival and Beach Time", "activities": ["Check in", "Relax at Baga Beach", "Sunset at Anjuna"], "estimated_cost": 3000}, {"day": 2, "title": "Exploration", "activities": ["Old Goa churches", "Spice plantation tour", "Local seafood dinner"], "estimated_cost": 5000}, {"day": 3, "title": "Nightlife and Departure", "activities": ["Beach shacks", "Club hopping in Anjuna", "Check out"], "estimated_cost": 4000}], "notes": "Best visited outside monsoon season"}
"""

    async def execute(self, entities: dict) -> PlannerResponse:

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
                "num_predict": 1024,
                "num_ctx": 8192
            }
        }

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(self.url, json=payload)

        response.raise_for_status()
        data = response.json()
        llm_output = data["message"]["content"]

        print("=" * 50)
        print("PLANNER RAW OUTPUT:", llm_output)
        print("=" * 50)

        parsed = json.loads(llm_output)
        return PlannerResponse.model_validate(parsed)