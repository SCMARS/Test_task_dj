from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.database import engine, Base
from app.api import cats_router, missions_router
from app.core.config import settings
from app.core.logger import setup_logging, logger
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Lifecycle Management (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Management system for spy cats, missions, and targets",
    version="1.0.0",
    lifespan=lifespan
)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s"
    )
    return response

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for demo purposes or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cats_router)
app.include_router(missions_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Spy Cat Agency API", "docs": "/docs"}
