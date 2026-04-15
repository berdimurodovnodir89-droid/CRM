from pydantic import BaseModel


class PipelineCreate(BaseModel):
    name: str
    order: int


class PipelineResponse(BaseModel):
    id: int
    name: str
    order: int

    class Config:
        from_attributes = True
