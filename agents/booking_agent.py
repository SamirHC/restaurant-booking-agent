from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from agents.utils import nodes
from agents.utils.state import BookingState
from services.booking_service import BookingService


class BookingAgent:
    def __init__(self, booking_service: BookingService, llm: ChatOpenAI):
        graph_builder = StateGraph(BookingState)

        graph_builder.add_node("parse_intent", lambda s: nodes.parse_intent(s, llm))
        graph_builder.add_node("validate_intent", lambda s: nodes.validate_parsed_intent(s, llm))
        graph_builder.add_node("missing_field", nodes.ask_for_missing_field)

        graph_builder.add_node("make_booking", nodes.make_booking)
        graph_builder.add_node("check_availability", nodes.check_availability)
        graph_builder.add_node("get_booking_details", nodes.get_booking_details)
        graph_builder.add_node("update_booking", nodes.update_booking)
        graph_builder.add_node("cancel_booking", nodes.cancel_booking)

        graph_builder.add_edge(START, "parse_intent")
        graph_builder.add_edge("parse", END)


        self.graph = graph_builder.compile()
