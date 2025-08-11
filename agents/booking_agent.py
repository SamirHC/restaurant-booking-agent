from langgraph.graph import StateGraph, START, END

from agents.utils import nodes
from agents.utils.state import BookingState, Intent
from ai.langauge_model import LanguageModel
from services.booking_service import BookingService


class BookingAgent:
    def __init__(self, booking_service: BookingService, llm: LanguageModel):
        graph_builder = StateGraph(BookingState)

        # Nodes
        graph_builder.add_node("parse_intent", lambda s: nodes.parse_intent(s, llm))
        graph_builder.add_node("ask_again", nodes.ask_again)
        graph_builder.add_node("missing_field", nodes.ask_for_missing_field)

        graph_builder.add_node("make_booking", lambda s: nodes.make_booking(s, booking_service))
        graph_builder.add_node("check_availability", lambda s: nodes.check_availability(s, booking_service))
        graph_builder.add_node("get_booking_details", lambda s: nodes.get_booking_details(s, booking_service))
        graph_builder.add_node("update_booking", lambda s: nodes.update_booking(s, booking_service))
        graph_builder.add_node("cancel_booking", lambda s: nodes.cancel_booking(s, booking_service))

        # Edges
        graph_builder.add_edge(START, "parse_intent")
        graph_builder.add_conditional_edges("parse_intent", self.route_parsed_intent)

        # Compile
        self.graph = graph_builder.compile()


    def route_parsed_intent(self, state: BookingState) -> str:
        match state.intent:
            case Intent.CHECK_AVAILABILITY:
                return "check_availability"
            case Intent.MAKE_BOOKING:
                return "make_booking"
            case Intent.GET_BOOKING_DETAILS:
                return "get_booking_details"
            case Intent.UPDATE_BOOKING:
                return "update_booking"
            case Intent.CANCEL_BOOKING:
                return "cancel_booking"
            case _:
                return "ask_again"


if __name__ == "__main__":
    from client.booking_client import BookingClient
    from dotenv import load_dotenv
    import os

    from ai.openai_llm import OpenAILanguageModel

    load_dotenv()

    booking_client = BookingClient(
        os.environ.get("BOOKING_API_BASE_URL"),
        os.environ.get("BEARER_TOKEN"),
        "TheHungryUnicorn",
    )
    booking_service = BookingService(booking_client)
    llm = OpenAILanguageModel()
    agent = BookingAgent(booking_service, llm)

    state = BookingState()
    while True:
        state.message = input("You: ")
        if state.message == "quit":
            break
        state = BookingState(**agent.graph.invoke(state))
        print(f"State: {state}")
        print(f"Agent: {state.response}")
