from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class EventStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class EventBase(SQLModel):
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    capacity: int = Field(gt=0)
    organizer: str = Field(min_length=1)
    status: EventStatus


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class ReservationBase(SQLModel):
    event_id: int
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    email: EmailStr


class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ReservationCreate(SQLModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    email: EmailStr