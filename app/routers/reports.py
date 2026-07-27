from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Camp, Victim, Resource, Volunteer
from app.dependencies import coordinator_required

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/search/camps")
def search_camps(
    district: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    camps = (
        db.query(Camp)
        .filter(Camp.district.ilike(f"%{district}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return camps


@router.get("/filter/victims")
def filter_victims(
    camp_id: int,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    victims = (
        db.query(Victim)
        .filter(Victim.camp_id == camp_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return victims


@router.get("/history/resources")
def resource_distribution_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    resources = (
        db.query(Resource)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return resources


@router.get("/volunteer-assignments")
def volunteer_assignments(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    volunteers = (
        db.query(Volunteer)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return volunteers