import json

import httpx

from schemas.nlu_schema import NLUResponse
from schemas.session_store import *

class NLUAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "qwen3:4b"

        self.system_prompt =self.system_prompt = """
You are an AI NLU engine for a Travel Assistant. Extract structured data from the user's message. Do not answer questions or give advice — only classify and extract.

### intent
One of: "plan_trip", "weather", "hotel_search", "flight_search", "general".
- Any mention of travel, a trip, a destination, dates, budget, or travelers → use the matching intent, even with a short/vague message or missing details.
- Only use "general" for greetings/small talk with no travel request at all.
- If the message is very short (a single word or short phrase, e.g. a place name, a number, "yes"/"no") and the conversation history shows a prior travel-related intent, treat it as continuing that same intent and filling in a missing field — do NOT classify it as "general" just because it's short and standalone-looking.

### entities
Extract only what's explicitly stated. Do not guess.
- source, destination: string or null
- start_date, end_date: "YYYY-MM-DD" or null
- duration_days, travelers: integer or null
- budget: number or null
- travel_style: "budget"/"luxury"/"mid-range" or null
- trip_type: "solo"/"couple"/"family"/"friends" or null
- interests: array of strings or []

### missing_fields
Important fields for this intent that weren't provided.

### Output rules
Return ONLY the JSON object below. No explanation, no markdown, no extra text.

Schema:
{"intent": "", "confidence": 0.0, "entities": {"source": null, "destination": null, "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": []}

Examples:
User: "Plan a trip from Mumbai to Goa for 4 people, budget 50000, one week in December"
Output: {"intent": "plan_trip", "confidence": 0.95, "entities": {"source": "Mumbai", "destination": "Goa", "start_date": null, "end_date": null, "duration_days": 7, "budget": 50000, "travelers": 4, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": ["start_date", "travel_style", "trip_type"]}

User: "Weather in Bangalore tomorrow"
Output: {"intent": "weather", "confidence": 0.9, "entities": {"source": null, "destination": "Bangalore", "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": []}

User: "Find me a hotel in Jaipur for 2 nights"
Output: {"intent": "hotel_search", "confidence": 0.9, "entities": {"source": null, "destination": "Jaipur", "start_date": null, "end_date": null, "duration_days": 2, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": ["travelers", "budget"]}

User: "Flight from Delhi to Bangalore next Friday"
Output: {"intent": "flight_search", "confidence": 0.9, "entities": {"source": "Delhi", "destination": "Bangalore", "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": ["travelers", "budget"]}

User: "Flight to Bangalore next Friday"
Output: {"intent": "flight_search", "confidence": 0.9, "entities": {"source": null, "destination": "Bangalore", "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": ["source", "travelers", "budget"]}

User: "Kolkata"
Output: {"intent": "flight_search", "confidence": 0.85, "entities": {"source": "Kolkata", "destination": "Bangalore", "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": ["travelers", "budget"]}

User: "Hi there, how are you?"
Output: {"intent": "general", "confidence": 0.99, "entities": {"source": null, "destination": null, "start_date": null, "end_date": null, "duration_days": null, "budget": null, "travelers": null, "travel_style": null, "trip_type": null, "interests": []}, "missing_fields": []}
"""

    async def execute(self, query: str , session_id: str) -> NLUResponse:
        history = session_store.get_history(session_id)
        payload = {
            "model": self.model,
            "messages": [
            {
                "role": "system",
                "content": self.system_prompt,
            },
               *history,
            {
                "role": "user",
                "content": query,
            },
            ],
            "stream": False,
            "think": False,
            "format": "json",
            "options": {
                "num_predict": 512,
                "num_ctx": 4096   # <-- add this, raises context window from the 2048 default
            }
        }

        async with httpx.AsyncClient(timeout=60) as client:
            print("=" * 50)
            print("PAYLOAD MESSAGES:")
            import json as _json
            print(_json.dumps(payload["messages"], indent=2))
            print("=" * 50)
            response = await client.post(
                self.url,
                json=payload
            )

        response.raise_for_status()

        data = response.json()
        
        
    # --- DEBUG: print raw output before parsing ---
        print("=" * 50)
        print("RAW LLM OUTPUT:")
        print(data["message"]["content"])
        print("=" * 50)
    # ------------------------------------------------

        llm_output = data["message"]["content"]
        
        parsed = json.loads(llm_output)
        
        session_store.add_turn(session_id, "user", query)
        session_store.add_turn(session_id, "assistant", llm_output)

        return NLUResponse.model_validate(parsed)