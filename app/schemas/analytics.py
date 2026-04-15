from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_leads: int
    new_leads: int
    contacted: int
    clients: int
    lost: int
    conversion_rate: float
