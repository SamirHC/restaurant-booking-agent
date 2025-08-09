from datetime import date, time
import json

from agents.utils.state import BookingState, Intent
from ai.langauge_model import LanguageModel
from client.model.customer import Customer
from services.booking_service import BookingService
from services import exceptions


def _extract_json_braces(text: str) -> str:
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in the text")
    return text[start:end+1]


def parse_intent(state: BookingState, llm: LanguageModel) -> BookingState:
    prompt = f"""
        You are a booking assistant. Today is {date.today().strftime("%A %d %B %Y")}.
        Detect the intent and extract fields from this user message:
        
        {state.message}

        Possible intents:
        {"\n".join([intent.name for intent in Intent])}

        Respond in raw JSON for it to be parsed by Python json.loads:
        {{
            "intent": <intent> | null,
            "visit_date": "YYYY-MM-DD" | null,
            "visit_time": "HH:MM:SS" | null,
            "party_size": int | null,
            "special_requests": str | null,
            "is_leave_time_confirmed": bool | null,
            "customer": {{
                "first_name": str | null,
                "surname": str | null,
                "email": str | null,
                "mobile": str | null,
            }} | null,
            "booking_reference": str | null,
            "cancellation_reason": str | null
        }}
    """
    response = llm.chat(prompt)
    extracted_json = _extract_json_braces(response)
    print(extracted_json)
    try:
        parsed = json.loads(extracted_json)
    except json.JSONDecodeError:
        parsed = {}
    for field, value in parsed.items():
        if value is not None and getattr(state, field, None) is None:
            if field == "visit_date":
                value = date.fromisoformat(value)
            elif field == "visit_time":
                value = time.fromisoformat(value)
            elif field == "customer":
                value = Customer(**value)
            elif field == "cancellation_reason":
                value = None  # Replace with enum parsing
            setattr(state, field, value)

    return state


def ask_for_missing_field(state: BookingState) -> BookingState:
    state["missing_fields"] = []
    return state


def check_availability(state: BookingState, booking_service: BookingService) -> BookingState:
    try:
        response = booking_service.check_availability(state.visit_date, state.party_size)
    except:
        response = None
    print(response)
    state.response = str(response)
    return state


def make_booking(state: BookingState, booking_service: BookingService) -> BookingState:
    response = booking_service.make_booking(
        visit_date=state.visit_date,
        visit_time=state.visit_time,
        party_size=state.party_size,
    )
    print(response)
    state.response = str(response)
    return state


def get_booking_details(state: BookingState, booking_service: BookingService) -> BookingState:    
    try:
        response = booking_service.get_booking_details(state.booking_reference)
    except exceptions.BookingNotFoundError:
        response = "The booking reference was not found."
    print(response)
    state.response = str(response)
    return state


def update_booking(state: BookingState, booking_service: BookingService) -> BookingState:
    try:
        response = booking_service.update_booking(state.booking_reference)
    except exceptions.BookingNotFoundError:
        response = "The booking reference was not found."
    print(response)
    state.response = str(response)
    return state


def cancel_booking(state: BookingState, booking_service: BookingService) -> BookingState:
    try:
        response = booking_service.cancel_booking(state.booking_reference, None)
    except exceptions.BookingNotFoundError:
        response = "The booking reference was not found."
    print(response)
    state.response = str(response)
    return state
