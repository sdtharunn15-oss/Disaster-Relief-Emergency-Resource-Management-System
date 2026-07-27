from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resource, Camp
from app.schemas import ResourceCreate, ResourceResponse
from app.dependencies import coordinator_required

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    camp = db.query(Camp).filter(Camp.id == resource.camp_id).first()

    if not camp:
        raise HTTPException(
            status_code=404,
            detail="Camp not found."
        )

    if resource.quantity > resource.stock:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock."
        )

    new_resource = Resource(**resource.model_dump())

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get("", response_model=list[ResourceResponse])
def get_resources(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    skip = (page - 1) * limit

    return db.query(Resource).offset(skip).limit(limit).all()


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(coordinator_required)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found."
        )

    return resource