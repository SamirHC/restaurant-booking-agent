from langgraph.graph import StateGraph, START, END

from agents.utils import nodes
from agents.utils.state import BookingState
from ai.langauge_model import LanguageModel
from services.booking_service import BookingService


class BookingAgent:
    def __init__(self, booking_service: BookingService, llm: LanguageModel):
        graph_builder = StateGraph(BookingState)

        # Nodes
        graph_builder.add_node("parse_intent", lambda s: nodes.parse_intent(s, llm))
        graph_builder.add_node("validate_intent", lambda s: nodes.validate_parsed_intent(s, llm))
        graph_builder.add_node("missing_field", nodes.ask_for_missing_field)

        graph_builder.add_node("make_booking", nodes.make_booking)
        graph_builder.add_node("check_availability", nodes.check_availability)
        graph_builder.add_node("get_booking_details", nodes.get_booking_details)
        graph_builder.add_node("update_booking", nodes.update_booking)
        graph_builder.add_node("cancel_booking", nodes.cancel_booking)

        # Edges
        graph_builder.add_edge(START, "parse_intent")
        # graph_builder.add_edge("parse_intent", "validate_intent")

        graph_builder.add_edge("parse_intent", END)

        # Compile
        self.graph = graph_builder.compile()


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

    state = BookingState(message="Book me a table for 4 tomorrow at 7pm")
    result_state = agent.graph.invoke(state)
    print(result_state)
