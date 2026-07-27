from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    volunteer = relationship("Volunteer", back_populates="user", uselist=False)


class Camp(Base):
    __tablename__ = "camps"

    id = Column(Integer, primary_key=True, index=True)
    camp_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    district = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    available_capacity = Column(Integer, nullable=False)
    status = Column(String, default="Active")

    victims = relationship(
        "Victim",
        back_populates="camp",
        cascade="all, delete"
    )

    resources = relationship(
        "Resource",
        back_populates="camp",
        cascade="all, delete"
    )

    volunteers = relationship(
        "Volunteer",
        back_populates="camp"
    )


class Victim(Base):
    __tablename__ = "victims"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    family_members = Column(Integer, nullable=False)

    camp_id = Column(
        Integer,
        ForeignKey("camps.id", ondelete="CASCADE"),
        nullable=False
    )

    registered_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    camp = relationship("Camp", back_populates="victims")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    camp_id = Column(
        Integer,
        ForeignKey("camps.id", ondelete="CASCADE"),
        nullable=False
    )

    resource_type = Column(String, nullable=False)

    stock = Column(Integer, nullable=False)   # <-- Add this line

    quantity = Column(Integer, nullable=False)

    distributed_by = Column(String, nullable=False)

    distribution_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    camp = relationship("Camp", back_populates="resources")

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

    availability_status = Column(
        String,
        default="Available"
    )

    assigned_camp = Column(
        Integer,
        ForeignKey("camps.id"),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    camp = relationship("Camp", back_populates="volunteers")
    user = relationship("User", back_populates="volunteer")