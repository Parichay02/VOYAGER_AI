from pydantic import BaseModel

from schemas.nlu_schema import NLUResponse


class TravelState(BaseModel):
    user_query: str
    session_id: str
    nlu: NLUResponse | None = None
    planner_tasks: list[str] = []
    agent_outputs: dict = {}
    final_response: str | None = None
    error: str | None = None
    current_step: str = "start"