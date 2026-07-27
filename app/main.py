from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers import (
    auth,
    camps,
    victims,
    resources,
    volunteers,
    reports,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Disaster Relief & Emergency Resource Management System"
)

app.include_router(auth.router)
app.include_router(camps.router)
app.include_router(victims.router)
app.include_router(resources.router)
app.include_router(volunteers.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Disaster Relief & Emergency Resource Management System API"
    }