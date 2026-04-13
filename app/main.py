from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.leads import router as leads_router

app = FastAPI(title="CRM API")

app.include_router(auth_router)
app.include_router(leads_router)


@app.get("/")
def root():
    return {"message": "CRM backend working"}
