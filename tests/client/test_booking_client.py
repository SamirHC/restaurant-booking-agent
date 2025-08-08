import pytest

from client.booking_client import BookingClient
from client.model.cancallation_reason import CancellationReason
from client.model.customer import Customer


@pytest.fixture(scope="module")
def fake_client() -> BookingClient:
    return BookingClient(
        base_url="fake-url",
        bearer_token="fake-bearer-token",
        restaurant_name="fake-restaurant",
    )


def test_check_availability(mocker, fake_client: BookingClient):
    mock_post = mocker.patch("requests.Session.post")

    visit_date = "2025-08-06"
    party_size = 2
    expected_response = {
        "restaurant": fake_client.restaurant_name,
        "restaurant_id": 1,
        "visit_date": visit_date,
        "party_size": party_size,
        "channel_code": "ONLINE",
        "available_slots": [
            {
            "time": "12:00:00",
            "available": True,
            "max_party_size": 8,
            "current_bookings": 0
            }
        ],
        "total_slots": 8
    }

    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = fake_client.check_availability(visit_date, party_size)

    assert result == expected_response
    mock_post.assert_called_once()

    called_url = mock_post.call_args[0][0]
    assert "AvailabilitySearch" in called_url
    assert fake_client.restaurant_name in called_url

    called_data = mock_post.call_args[1]["data"]
    assert called_data["VisitDate"] == visit_date
    assert called_data["PartySize"] == 2
    assert called_data["ChannelCode"] == "ONLINE"


def test_make_booking(mocker, fake_client: BookingClient):
    mock_post = mocker.patch("requests.Session.post")

    visit_date = "2025-08-06"
    visit_time = "12:30"
    party_size = 2
    customer = Customer(
        first_name="John",
        surname="Smith",
        email="john@example.com"
    )

    expected_response = {
        "booking_reference": "ABC1234",
        "booking_id": 1,
        "restaurant": fake_client.restaurant_name,
        "visit_date": visit_date,
        "visit_time": visit_time,
        "party_size": party_size,
        "status": "confirmed",
        "customer": {
            "id": 1,
            "first_name": customer.first_name,
            "surname": customer.surname,
            "email": customer.email
        },
        "created_at": "2025-08-06T10:30:00.123456"
    }
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = fake_client.make_booking(
        visit_date,
        visit_time,
        party_size,
        customer=customer
    )

    assert result == expected_response
    mock_post.assert_called_once()

    called_url = mock_post.call_args[0][0]
    assert "BookingWithStripeToken" in called_url
    assert fake_client.restaurant_name in called_url

    called_data = mock_post.call_args[1]["data"]
    assert called_data["VisitDate"] == visit_date
    assert called_data["VisitTime"] == visit_time
    assert called_data["PartySize"] == party_size
    assert called_data["ChannelCode"] == "ONLINE"
    assert called_data["Customer[FirstName]"] == customer.first_name
    assert called_data["Customer[Surname]"] == customer.surname
    assert called_data["Customer[Email]"] == customer.email


def test_get_booking_details(mocker, fake_client: BookingClient):
    mock_get = mocker.patch("requests.Session.get")

    booking_reference = "ABC1234"

    expected_response = {
        "booking_reference": booking_reference,
        "booking_id": 1,
        "restaurant": fake_client.restaurant_name,
        "visit_date": "2025-08-06",
        "visit_time": "12:30:00",
        "party_size": 4,
        "status": "confirmed",
        "special_requests": "Window table please",
        "customer": {
            "id": 1,
            "first_name": "John",
            "surname": "Smith",
            "email": "john@example.com",
            "mobile": "1234567890"
        },
        "created_at": "2025-08-06T10:30:00.123456",
        "updated_at": "2025-08-06T10:30:00.123456"
    }
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fake_client.get_booking_details(booking_reference)

    assert result == expected_response
    mock_get.assert_called_once()

    called_url = mock_get.call_args[0][0]
    assert "Booking" in called_url
    assert fake_client.restaurant_name in called_url
    assert booking_reference in called_url


def test_update_booking(mocker, fake_client: BookingClient):
    mock_patch = mocker.patch("requests.Session.patch")

    booking_reference = "ABC1234"
    party_size = 6
    special_requests = "Updated request"

    expected_response = {
        "booking_reference": booking_reference,
        "booking_id": 1,
        "restaurant": fake_client.restaurant_name,
        "updates": {
            "party_size": party_size,
            "special_requests": special_requests
        },
        "status": "updated",
        "updated_at": "2025-08-06T11:30:00.123456",
        "message": "Booking ABC1234 has been successfully updated"
    }
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status.return_value = None
    mock_patch.return_value = mock_response

    result = fake_client.update_booking(
        booking_reference,
        party_size=party_size,
        special_requests=special_requests
    )

    assert result == expected_response
    mock_patch.assert_called_once()

    called_url = mock_patch.call_args[0][0]
    assert "Booking" in called_url
    assert fake_client.restaurant_name in called_url
    assert booking_reference in called_url

    called_data = mock_patch.call_args[1]["data"]
    assert called_data["PartySize"] == party_size
    assert called_data["SpecialRequests"] == special_requests


def test_cancel_booking(mocker, fake_client: BookingClient):
    mock_post = mocker.patch("requests.Session.post")

    booking_reference = "ABC1234"
    cancellation_reason = CancellationReason.CUSTOMER_REQUEST

    expected_response = {
        "booking_reference": booking_reference,
        "booking_id": 1,
        "restaurant": fake_client.restaurant_name,
        "cancellation_reason_id": cancellation_reason.code,
        "cancellation_reason": cancellation_reason.description,
        "status": "cancelled",
        "cancelled_at": "2025-08-06T12:30:00.123456",
        "message": f"Booking {booking_reference} has been successfully cancelled"
    }
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = fake_client.cancel_booking(booking_reference, cancellation_reason)

    assert result == expected_response
    mock_post.assert_called_once()

    called_url = mock_post.call_args[0][0]
    assert "Booking" in called_url
    assert fake_client.restaurant_name in called_url
    assert booking_reference in called_url

    called_data = mock_post.call_args[1]["data"]
    assert called_data["micrositeName"] == fake_client.restaurant_name
    assert called_data["bookingReference"] == booking_reference
    assert called_data["cancellationReasonId"] == cancellation_reason.code


if __name__ == "__main__":        
    """
    response = BookingClient.update_booking(
        "32P21VR",
        party_size=6,
        special_requests="Updated request"
    )
    """

    response = BookingClient.cancel_booking("32P21VR", CancellationReason.CUSTOMER_REQUEST)
    
    print(response)
