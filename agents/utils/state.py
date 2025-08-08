from datetime import date, time
from enum import Enum

from pydantic import BaseModel

from client.model.customer import Customer
from client.model.cancallation_reason import CancellationReason


class Intent(Enum):
    CHECK_AVAILABILITY = 0
    MAKE_BOOKING = 1
    GET_BOOKING_DETAILS = 2
    UPDATE_BOOKING = 3
    CANCEL_BOOKING = 4


class BookingState(BaseModel):
    intent: Intent | None = None

    visit_date: date | None = None
    visit_time: time | None = None
    party_size: int | None = None
    special_requests: str | None = None
    is_leave_time_confirmed: bool | None = None
    customer: Customer | None = None
    cancellation_reason: CancellationReason | None = None

    missing_fields: list[str] = []
    message: str | None = None
