from langgraph.graph import StateGraph, END
from graph.nodes import (
    nlu_node, plan_trip_node, weather_node,
    hotel_search_node, flight_search_node, general_node
)
from schemas.state import TravelState

def route_by_intent(state: TravelState) -> str:
    if state.error:
        return "end"
    valid_intents = {"plan_trip", "weather", "hotel_search", "flight_search", "general"}
    return state.nlu.intent if state.nlu.intent in valid_intents else "general"


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("nlu", nlu_node)
    graph.add_node("plan_trip", plan_trip_node)
    graph.add_node("weather", weather_node)
    graph.add_node("hotel_search", hotel_search_node)
    graph.add_node("flight_search", flight_search_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("nlu")

    graph.add_conditional_edges(
        "nlu",
        route_by_intent,
        {
            "plan_trip": "plan_trip",
            "weather": "weather",
            "hotel_search": "hotel_search",
            "flight_search": "flight_search",
            "general": "general",
            "end": END,
        }
    )

    for node in ["plan_trip", "weather", "hotel_search", "flight_search", "general"]:
        graph.add_edge(node, END)

    return graph.compile()


travel_graph = build_travel_graph()