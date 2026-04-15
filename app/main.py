from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.db.base import Base
from app.db.session import engine

from app.models import user, lead, task, tag, source

from app.api.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.tasks import router as tasks_router
from app.api.tags import router as tags_router
from app.api.sources import router as sources_router
from app.api.pipeline import router as pipeline_router
from app.api.activities import router as activities_router
from app.api.analytics import router as analytics_router

from app.api.exceptions import global_exception_handler
from app.api.middleware import response_wrapper, request_logger

from slowapi.middleware import SlowAPIMiddleware
from app.core.rate_limiter import limiter


# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(title="CRM API")


# Database tables
Base.metadata.create_all(bind=engine)


# Rate limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# Middleware
app.middleware("http")(request_logger)
app.middleware("http")(response_wrapper)


# CORS (frontend ulanishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(sources_router)
app.include_router(pipeline_router)
app.include_router(activities_router)
app.include_router(analytics_router)


# Global error handler
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
def root():
    return {"message": "CRM backend working"}
