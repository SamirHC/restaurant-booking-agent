from datetime import date, time
import json

from langchain_openai import ChatOpenAI

from agents.utils.state import BookingState, Intent
from client.model.customer import Customer
from services.booking_service import BookingService


def parse_intent(state: BookingState, llm: ChatOpenAI):
    prompt = f"""
        You are a booking assistant. 
        Detect the intent and extract fields from this user message:
        
        {state.message}

        Possible intents:
        {"\n".join([intent.name for intent in Intent])}

        Respond in JSON:
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
    response = llm.invoke(prompt)
    parsed = json.loads(response.content)
    for field, value in parsed.items():
        if value is not None and getattr(state, field, None) is None:
            if field == "visit_date":
                value = date.fromisoformat(value)
            elif field == "visit_time":
                value = time.fromisoformat(value)
            elif field == "customer":
                value = Customer(**value)
            elif field == "cancellation_reason":
                value = None
            setattr(state, field, value)

    return state


def validate_parsed_intent(state: BookingState):
    if state.intent:
        pass


def parse_booking_request(state: BookingState):
    prompt = "\n".join((
        "Extract booking details from this message:",
        "",
        f"{state.message}",
        "",
        "Respond with JSON:",
    ))
    
    return state


def ask_for_missing_field(state: BookingState):
    state["missing_fields"] = []
    return state


def make_booking(state: BookingState, booking_service: BookingService):
    booking = booking_service.make_booking(
        visit_date=state["visit_date"],
        visit_time=state["visit_time"],
        party_size=state["party_size"],
    )

def check_availability(state: BookingState, booking_service: BookingService):
    pass

def get_booking_details(state: BookingState, booking_service: BookingService):
    pass

def update_booking(state: BookingState, booking_service: BookingService):
    pass

def cancel_booking(state: BookingState, booking_service: BookingService):
    pass
