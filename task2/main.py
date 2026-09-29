from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import (
    Event,
    EventCreate,
    EventStatus,
    EventUpdate,
    Reservation,
    ReservationCreate,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Campus Event Seat Reservation API",
    description="FastAPI application for managing campus events and student reservations.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Campus Event Seat Reservation API is running"}


# -------------------------
# EVENT APIs
# -------------------------

@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    session: Session = Depends(get_session),
):
    event = Event.model_validate(event_data)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@app.get("/events", response_model=list[Event])
def get_events(
    session: Session = Depends(get_session),
):
    events = session.exec(select(Event)).all()
    return events


@app.get("/events/{event_id}", response_model=Event)
def get_event(
    event_id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event


@app.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    event.title = event_data.title
    event.venue = event_data.venue
    event.capacity = event_data.capacity
    event.organizer = event_data.organizer
    event.status = event_data.status

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    session.delete(event)
    session.commit()

    return {"message": "Event deleted successfully"}

# -------------------------
# RESERVATION APIs
# -------------------------

@app.post(
    "/events/{event_id}/reserve",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session),
):
    # Check whether event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Check whether event is open
    if event.status != EventStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is closed",
        )

    # Count existing reservations
    reservations = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()

    booked = len(reservations)

    # Check whether event is full
    if booked >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is full",
        )

    # Create reservation
    reservation = Reservation(
        event_id=event_id,
        student_name=reservation_data.student_name,
        roll_number=reservation_data.roll_number,
        email=reservation_data.email,
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


@app.get(
    "/events/{event_id}/reservations",
    response_model=list[Reservation],
)
def get_event_reservations(
    event_id: int,
    session: Session = Depends(get_session),
):
    # Check whether event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    reservations = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()

    return reservations


@app.delete("/reservations/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    session: Session = Depends(get_session),
):
    reservation = session.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    session.delete(reservation)
    session.commit()

    return {"message": "Reservation cancelled successfully"}


@app.get("/events/{event_id}/availability")
def get_event_availability(
    event_id: int,
    session: Session = Depends(get_session),
):
    # Check whether event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Count reservations
    reservations = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()

    booked = len(reservations)
    remaining = event.capacity - booked

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": remaining,
    }