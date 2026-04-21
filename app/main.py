import os

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import calculations, users

app = FastAPI(title="Module 12 Backend")

app.include_router(users.router)
app.include_router(calculations.router)


@app.on_event("startup")
def on_startup() -> None:
    if os.getenv("TESTING") == "1":
        return
    create_db_and_tables()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Module 12 backend is running"}
