import asyncio
import websockets
import json


async def test():
    async with websockets.connect("ws://localhost:8000/ws/travel") as ws:
        await ws.send(json.dumps({
  "query": "Plan a 3 day trip to Goa for 2 people, budget 20000, interested in beaches and nightlife",
  "session_id": "sanity-check-2"
}))

        while True:
            message = await ws.recv()
            data = json.loads(message)
            print(json.dumps(data, indent=2))
            if data.get("type") == "done":
                break


asyncio.run(test())