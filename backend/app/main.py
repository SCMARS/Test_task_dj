from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import cats_router, missions_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Cat Agency API",
    description="Management system for spy cats, missions, and targets",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cats_router)
app.include_router(missions_router)


@app.get("/")
def root():
    return {"message": "Welcome to Spy Cat Agency API", "docs": "/docs"}
