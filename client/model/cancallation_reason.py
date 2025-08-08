from enum import Enum


class CancellationReason(Enum):
    CUSTOMER_REQUEST = 1, "Customer requested cancellation"
    RESTAURANT_CLOSURE = 2, "Restaurant temporarily closed"
    WEATHER = 3, "Cancelled due to weather conditions"
    EMERGENCY = 4, "Emergency Cancellation"
    NO_SHOW = 5, "Customer did not show up"

    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    @classmethod
    def from_code(cls, code):
        return next((r for r in cls if r.code == code), None)
