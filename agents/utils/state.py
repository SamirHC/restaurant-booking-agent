from datetime import date, time
from enum import Enum

from pydantic import BaseModel

from client.model.customer import Customer
from client.model.cancallation_reason import CancellationReason


class Intent(Enum):
    CHECK_AVAILABILITY = "CHECK_AVAILABILITY"
    MAKE_BOOKING = "MAKE_BOOKING"
    GET_BOOKING_DETAILS = "GET_BOOKING_DETAILS"
    UPDATE_BOOKING = "UPDATE_BOOKING"
    CANCEL_BOOKING = "CANCEL_BOOKING"


class BookingState(BaseModel):
    intent: Intent | None = None

    visit_date: date | None = None
    visit_time: time | None = None
    party_size: int | None = None
    special_requests: str | None = None
    is_leave_time_confirmed: bool | None = None
    customer: Customer | None = None
    booking_reference: str | None = None

    missing_fields: list[str] = []
    message: str | None = None
    response: str | None = None
