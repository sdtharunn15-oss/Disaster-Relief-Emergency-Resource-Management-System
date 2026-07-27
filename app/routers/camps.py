from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Camp
from app.schemas import CampCreate, CampUpdate, CampResponse
from app.dependencies import coordinator_required

router = APIRouter(
    prefix="/camps",
    tags=["Relief Camps"]
)


@router.post(
    "",
    response_model=CampResponse,
    status_code=status.HTTP_201_CREATED
)
def create_camp(
    camp: CampCreate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    new_camp = Camp(**camp.model_dump())

    db.add(new_camp)
    db.commit()
    db.refresh(new_camp)

    return new_camp


@router.get("", response_model=list[CampResponse])
def get_camps(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    return (
        db.query(Camp)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{camp_id}", response_model=CampResponse)
def get_camp(
    camp_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()

    if not camp:
        raise HTTPException(
            status_code=404,
            detail="Camp not found."
        )

    return camp


@router.put("/{camp_id}", response_model=CampResponse)
def update_camp(
    camp_id: int,
    camp_update: CampUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()

    if not camp:
        raise HTTPException(
            status_code=404,
            detail="Camp not found."
        )

    update_data = camp_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(camp, key, value)

    db.commit()
    db.refresh(camp)

    return camp


@router.delete("/{camp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camp(
    camp_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()

    if not camp:
        raise HTTPException(
            status_code=404,
            detail="Camp not found."
        )

    db.delete(camp)
    db.commit()

    return