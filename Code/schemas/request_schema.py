from pydantic import BaseModel, Field


class UserQueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Natural language travel query"
    )
    session_id: str