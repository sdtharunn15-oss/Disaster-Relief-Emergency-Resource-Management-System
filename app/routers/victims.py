from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Victim, Camp
from app.schemas import VictimCreate, VictimUpdate, VictimResponse
from app.dependencies import coordinator_required

router = APIRouter(
    prefix="/victims",
    tags=["Victims"]
)


@router.post(
    "",
    response_model=VictimResponse,
    status_code=status.HTTP_201_CREATED
)
def register_victim(
    victim: VictimCreate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    camp = db.query(Camp).filter(Camp.id == victim.camp_id).first()

    if not camp:
        raise HTTPException(
            status_code=404,
            detail="Camp not found."
        )

    if camp.available_capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Camp is full."
        )

    new_victim = Victim(**victim.model_dump())

    db.add(new_victim)

    camp.available_capacity -= 1

    if camp.available_capacity == 0:
        camp.status = "Full"

    db.commit()
    db.refresh(new_victim)

    return new_victim


@router.get("", response_model=list[VictimResponse])
def get_victims(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    return db.query(Victim).offset(skip).limit(limit).all()


@router.get("/{victim_id}", response_model=VictimResponse)
def get_victim(
    victim_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(
            status_code=404,
            detail="Victim not found."
        )

    return victim


@router.put("/{victim_id}", response_model=VictimResponse)
def update_victim(
    victim_id: int,
    victim_update: VictimUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(
            status_code=404,
            detail="Victim not found."
        )

    update_data = victim_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(victim, key, value)

    db.commit()
    db.refresh(victim)

    return victim