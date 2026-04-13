from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.tasks import router as tasks_router
from app.api.tags import router as tags_router

app = FastAPI(title="CRM API")

app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(tasks_router)
app.include_router(tags_router)


@app.get("/")
def root():
    return {"message": "CRM backend working"}
