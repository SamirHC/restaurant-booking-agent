import requests

from client.model.cancallation_reason import CancellationReason
from client.model.customer import Customer


class BookingClient:
    def __init__(self, base_url: str, bearer_token: str, restaurant_name: str):
        self.restaurant_name = restaurant_name
        self.base_url = base_url
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.session = requests.Session()
        self.session.headers.update(headers)


    def check_availability(self, visit_date: str, party_size: int):
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{self.restaurant_name}/AvailabilitySearch"
        response = self.session.post(
            url,
            data={
                "VisitDate": visit_date,
                "PartySize": party_size,
                "ChannelCode": "ONLINE",
            },
        )
        response.raise_for_status()
        return response.json()


    def make_booking(
            self,
            visit_date: str,
            visit_time: str,
            party_size: int,
            special_requests: str | None = None,
            is_leave_time_confirmed: bool = None,
            customer: Customer | None = None,
        ):
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{self.restaurant_name}/BookingWithStripeToken"
        data = {
            "VisitDate": visit_date,
            "VisitTime": visit_time,
            "PartySize": party_size,
            "ChannelCode": "ONLINE",
        }
        if special_requests is not None:
            data["SpecialRequests"] = special_requests
        if is_leave_time_confirmed is not None:
            data["IsLeaveTimeConfirmed"] = is_leave_time_confirmed
        if customer is not None:
            data |= self._customer_to_dict(customer)
        response = self.session.post(
            url,
            data=data,
        )
        response.raise_for_status()
        return response.json()


    def get_booking_details(self, booking_reference: str):
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{self.restaurant_name}/Booking/{booking_reference}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


    def update_booking(
        self,
        booking_reference: str,
        visit_date: str | None = None,
        visit_time: str | None = None,
        party_size: int | None = None,
        special_requests: str | None = None,
        is_leave_time_confirmed: bool | None = None,
    ):
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{self.restaurant_name}/Booking/{booking_reference}"
        data = {}
        if visit_date is not None:
            data["VisitDate"] = visit_date
        if visit_time is not None:
            data["VisitTime"] = visit_time
        if party_size is not None:
            data["PartySize"] = party_size
        if special_requests is not None:
            data["SpecialRequests"] = special_requests
        if is_leave_time_confirmed is not None:
            data["IsLeaveTimeConfirmed"] = is_leave_time_confirmed
        response = self.session.patch(
            url,
            data=data,
        )
        response.raise_for_status()
        return response.json()


    def cancel_booking(self, booking_reference: str, cancellation_reason: CancellationReason):
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{self.restaurant_name}/Booking/{booking_reference}/Cancel"
        response = self.session.post(
            url,
            data={
                "micrositeName": self.restaurant_name,
                "bookingReference": booking_reference,
                "cancellationReasonId": cancellation_reason.code,
                },
            )
        response.raise_for_status()
        return response.json()


    # Helper Functions
    def _customer_to_dict(self, customer: Customer):
        data = {}
        if customer.title is not None:
            data["Customer[Title]"] = customer.title
        if customer.first_name is not None:
            data["Customer[FirstName]"] = customer.first_name
        if customer.surname is not None:
            data["Customer[Surname]"] = customer.surname
        if customer.email is not None:
            data["Customer[Email]"] = customer.email
        if customer.mobile is not None:
            data["Customer[Mobile]"] = customer.mobile
        if customer.phone is not None:
            data["Customer[Phone]"] = customer.phone
        if customer.mobile_country_code is not None:
            data["Customer[MobileCountryCode]"] = customer.mobile_country_code
        if customer.phone_country_code is not None:
            data["Customer[PhoneCountryCode]"] = customer.phone_country_code
        if customer.receive_email_marketing is not None:
            data["Customer[ReceiveEmailMarketing]"] = customer.receive_email_marketing
        if customer.receive_sms_marketing is not None:
            data["Customer[ReceiveSmsMarketing]"] = customer.receive_sms_marketing
        return data
