from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# -------------------------
# Authentication
# -------------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# -------------------------
# Camp
# -------------------------

class CampBase(BaseModel):
    camp_name: str
    location: str
    district: str
    capacity: int = Field(gt=0)
    available_capacity: int = Field(gt=0)
    status: str = "Active"


class CampCreate(CampBase):
    pass


class CampUpdate(BaseModel):
    camp_name: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    available_capacity: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = None


class CampResponse(CampBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Victim
# -------------------------

class VictimBase(BaseModel):
    name: str
    age: int = Field(gt=0)
    gender: str
    contact_number: str
    family_members: int = Field(ge=0)
    camp_id: int


class VictimCreate(VictimBase):
    pass


class VictimUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    family_members: Optional[int] = Field(default=None, ge=0)
    camp_id: Optional[int] = None


class VictimResponse(VictimBase):
    id: int
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Resource
# -------------------------

class ResourceBase(BaseModel):
    camp_id: int
    resource_type: str
    stock: int = Field(gt=0)
    quantity: int = Field(gt=0)
    distributed_by: str


class ResourceCreate(ResourceBase):
    pass


class ResourceResponse(ResourceBase):
    id: int
    distribution_date: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Volunteer
# -------------------------

class VolunteerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class VolunteerCreate(VolunteerBase):
    pass


class VolunteerResponse(VolunteerBase):
    id: int
    assigned_camp: Optional[int]
    availability_status: str

    model_config = ConfigDict(from_attributes=True)
