from pydantic import BaseModel


class ActivityCreate(BaseModel):
    lead_id: int
    type: str
    note: str


class ActivityResponse(BaseModel):
    id: int
    lead_id: int
    type: str
    note: str

    class Config:
        from_attributes = True
