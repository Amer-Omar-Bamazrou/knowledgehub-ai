from pydantic import BaseModel, Field


class AIGenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000,
    )


class AISource(BaseModel):
    document_id: int
    document_title: str
    chunk_id: int    


class AIGenerateResponse(BaseModel):
    response: str
    sources: list[AISource] = []
