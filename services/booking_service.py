from datetime import date, time

from requests.exceptions import HTTPError

from client.booking_client import BookingClient
from client.model.customer import Customer
from client.model.cancallation_reason import CancellationReason


class BookingService:
    def __init__(self, client: BookingClient):
        self.client = client
    
    def check_availability(self, visit_date: date, party_size: int):
        return self.client.check_availability(visit_date, party_size)


    def make_booking(
            self,
            visit_date: date,
            visit_time: time,
            party_size: int,
            special_requests: str | None = None,
            is_leave_time_confirmed: bool = None,
            customer: Customer | None = None,
        ):
        return self.client.make_booking(
            visit_date,
            visit_time,
            party_size,
            special_requests,
            is_leave_time_confirmed,
            customer
        )


    def get_booking_details(self, booking_reference: str):
        try:
            return self.client.get_booking_details(booking_reference)
        except HTTPError:
            return {}


    def update_booking(
        self,
        booking_reference: str,
        visit_date: date | None = None,
        visit_time: time | None = None,
        party_size: int | None = None,
        special_requests: str | None = None,
        is_leave_time_confirmed: bool | None = None,
    ):
        return self.client.update_booking(
            booking_reference,
            visit_date,
            visit_time,
            party_size,
            special_requests,
            is_leave_time_confirmed
        )


    def cancel_booking(self, booking_reference: str, cancellation_reason: CancellationReason):
        return self.client.cancel_booking(booking_reference, cancellation_reason)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    client = BookingClient(
        base_url=os.environ.get("BOOKING_API_BASE_URL"),
        bearer_token=os.environ.get("BEARER_TOKEN"),
        restaurant_name="TheHungryUnicorn"
    )
    service = BookingService(client)
    response = service.get_booking_details("32P21VR")
    print(response)
