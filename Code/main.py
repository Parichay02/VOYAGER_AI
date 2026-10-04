import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from schemas.request_schema import UserQueryRequest
from graph.build_graph import travel_graph
from schemas.state import TravelState

app = FastAPI(
    title="VoyagerAI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TravelResponse(BaseModel):
    response: str
    details: Optional[dict] = None


def _serialize(node_output: dict) -> dict:
    result = {}
    for key, value in node_output.items():
        if hasattr(value, "model_dump"):
            result[key] = value.model_dump()
        else:
            result[key] = value
    return result


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/session/new")
async def new_session():
    return {"session_id": str(uuid.uuid4())}


@app.post("/travel")
async def travel(request: UserQueryRequest):
    initial_state = TravelState(
        user_query=request.query,
        session_id=request.session_id,
    )

    final_state = await travel_graph.ainvoke(initial_state)

    if final_state.get("error"):
        raise HTTPException(status_code=500, detail=final_state["error"])

    return {
        "response": final_state["final_response"],
        "details": final_state.get("agent_outputs"),
    }


@app.websocket("/ws/travel")
async def travel_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_json()
            request = UserQueryRequest.model_validate(raw)

            initial_state = TravelState(
                user_query=request.query,
                session_id=request.session_id,
            )

            async for event in travel_graph.astream(initial_state):
                for node_name, node_output in event.items():
                    await websocket.send_json({
                        "type": "node_update",
                        "node": node_name,
                        "output": _serialize(node_output),
                    })

            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        print("Client disconnected")