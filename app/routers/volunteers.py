from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Volunteer, Camp
from app.schemas import VolunteerCreate, VolunteerResponse
from app.dependencies import coordinator_required, volunteer_required

router = APIRouter(
    prefix="/volunteers",
    tags=["Volunteers"]
)


@router.post(
    "",
    response_model=VolunteerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_volunteer(
    volunteer: VolunteerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    existing = db.query(Volunteer).filter(
        Volunteer.email == volunteer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteer email already exists."
        )

    new_volunteer = Volunteer(
        name=volunteer.name,
        email=volunteer.email,
        phone=volunteer.phone,
        availability_status="Available"
    )

    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)

    return new_volunteer


@router.get(
    "",
    response_model=list[VolunteerResponse]
)
def get_volunteers(
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


@router.post("/{volunteer_id}/assign/{camp_id}")
def assign_volunteer(
    volunteer_id: int,
    camp_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    volunteer = db.query(Volunteer).filter(
        Volunteer.id == volunteer_id
    ).first()

    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer not found."
        )

    camp = db.query(Camp).filter(
        Camp.id == camp_id
    ).first()

    if not camp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camp not found."
        )

    if (
        volunteer.assigned_camp is not None
        and volunteer.availability_status == "Assigned"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteer already assigned to another active camp."
        )

    volunteer.assigned_camp = camp.id
    volunteer.availability_status = "Assigned"

    db.commit()
    db.refresh(volunteer)

    return {
        "message": "Volunteer assigned successfully."
    }


@router.get("/my-camp")
def my_assigned_camp(
    db: Session = Depends(get_db),
    current_user=Depends(volunteer_required)
):
    volunteer = (
        db.query(Volunteer)
        .filter(Volunteer.user_id == current_user.id)
        .first()
    )

    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer profile not found."
        )

    if volunteer.assigned_camp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No camp assigned."
        )

    camp = (
        db.query(Camp)
        .filter(Camp.id == volunteer.assigned_camp)
        .first()
    )

    if not camp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned camp not found."
        )

    return camp