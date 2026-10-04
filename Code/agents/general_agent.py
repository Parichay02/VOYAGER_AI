import httpx


class GeneralAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "qwen3:4b"

        self.system_prompt ="""
You are the friendly conversational voice of VoyagerAI, a travel assistant.

The user's message doesn't require travel planning, weather, hotel, or flight lookups — it's a greeting, small talk, or a general question about what you can help with.

Return ONLY the JSON object below. No explanation, no reasoning, no markdown.

Schema:
{"reply": ""}

The "reply" value should be warm and brief (1-3 sentences). If relevant, mention you can help with planning trips, checking weather, finding hotels, or searching flights.

Example:
User: "Hi there, how are you?"
Output: {"reply": "Hi! I'm doing great, thanks for asking. I'm here to help you plan trips, check weather, find hotels, or search flights — what can I do for you today?"}

Example:
User: "What can you help me with?"
Output: {"reply": "I can help you plan trips, check the weather at your destination, find hotels, or search flights. Just tell me what you need!"}
"""
    async def execute(self, query: str, history: list) -> str:

        messages = [
            {"role": "system", "content": self.system_prompt},
            *history,
            {"role": "user", "content": query},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "think": False,
            "format": "json",
            "options": {
                "num_predict": 300,
                "num_ctx": 4096
            }
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.url, json=payload)

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"].strip()