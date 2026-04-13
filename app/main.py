from fastapi import FastAPI
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.auth import router as auth_router


app = FastAPI()


@app.get("/")
def root():
    return {"message": "CRM backend working"}


app = FastAPI(title="CRM API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "CRM backend working"}
