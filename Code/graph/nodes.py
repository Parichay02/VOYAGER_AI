from agents.nlu_agent import NLUAgent
from schemas.state import TravelState
from agents.planner_agent import PlannerAgent
from agents.weather_agent import WeatherAgent
from agents.hotel_agent import HotelAgent
from agents.general_agent import GeneralAgent
from schemas.session_store import session_store
from agents.flight_agent import FlightAgent

flight_agent = FlightAgent()


general_agent = GeneralAgent()

hotel_agent = HotelAgent()

weather_agent = WeatherAgent()

planner_agent = PlannerAgent()

nlu_agent = NLUAgent()

AGENT_DISPLAY_NAMES = {
    "plan_trip": "Trip Planner Agent",
    "weather": "Weather Forecast Agent",
    "hotel_search": "Hotel Search Agent",
    "flight_search": "Flight Search Agent",
    "general": "General Assistant",
    "nlu": "Understanding Agent",
}


async def nlu_node(state: TravelState) -> dict:
    try:
        result = await nlu_agent.execute(state.user_query, state.session_id)

        display_name = AGENT_DISPLAY_NAMES.get(result.intent, result.intent.replace("_", " ").title())

        summary = None
        if result.intent != "general":
            summary = f"Got it — passing this to the {display_name}"
            if result.entities.destination:
                summary += f" for {result.entities.destination}"
            summary += "..."

        entities_dict = result.entities.model_dump()
        entities_preview = {
            k: v for k, v in entities_dict.items()
            if v is not None and v != [] and v != ""
        }

        return {
            "nlu": result,
            "final_response": summary,
            "entities_preview": entities_preview,
            "agent_display_name": display_name,
            "current_step": "nlu_complete",
        }
    except Exception as e:
        return {"error": f"NLU failed: {e}", "current_step": "nlu_failed"}


async def plan_trip_node(state: TravelState) -> dict:
    try:
        entities = state.nlu.entities.model_dump()
        plan = await planner_agent.execute(entities)
        return {
            "agent_outputs": {"planner": plan.model_dump()},
            "final_response": f"Here's your {plan.duration_days}-day plan for {plan.destination}!",
            "agent_display_name": AGENT_DISPLAY_NAMES["plan_trip"],
            "current_step": "plan_trip_complete",
        }
    except Exception as e:
        return {"error": f"Planner failed: {e}", "current_step": "plan_trip_failed"}


async def weather_node(state: TravelState) -> dict:
    try:
        destination = state.nlu.entities.destination
        weather = await weather_agent.execute(destination)
        return {
            "agent_outputs": {"weather": weather.model_dump()},
            "final_response": weather.summary,
            "agent_display_name": AGENT_DISPLAY_NAMES["weather"],
            "current_step": "weather_complete",
        }
    except Exception as e:
        return {"error": f"Weather lookup failed: {e}", "current_step": "weather_failed"}



async def hotel_search_node(state: TravelState) -> dict:
    try:
        entities = state.nlu.entities.model_dump()
        hotels = await hotel_agent.execute(entities)
        return {
            "agent_outputs": {"hotel_search": hotels.model_dump()},
            "final_response": f"Found {len(hotels.hotels)} hotel options in {hotels.destination}.",
            "agent_display_name": AGENT_DISPLAY_NAMES["hotel_search"],
            "current_step": "hotel_search_complete",
        }
    except Exception as e:
        return {"error": f"Hotel search failed: {e}", "current_step": "hotel_search_failed"}



async def flight_search_node(state: TravelState) -> dict:
    entities = state.nlu.entities

    if not entities.source:
        return {
            "final_response": "Which city are you flying from?",
            "current_step": "flight_search_needs_source",
        }

    try:
        flights = await flight_agent.execute(entities.model_dump())
        return {
            "agent_outputs": {"flight_search": flights.model_dump()},
            "final_response": f"Found {len(flights.flights)} flight options from {flights.source} to {flights.destination}.",
            "agent_display_name": AGENT_DISPLAY_NAMES["flight_search"],
            "current_step": "flight_search_complete",
        }
    except Exception as e:
        return {"error": f"Flight search failed: {e}", "current_step": "flight_search_failed"}





async def general_node(state: TravelState) -> dict:
    try:
        history_key = f"{state.session_id}:general"
        history = session_store.get_history(history_key)
        reply = await general_agent.execute(state.user_query, history)

        session_store.add_turn(history_key, "user", state.user_query)
        session_store.add_turn(history_key, "assistant", reply)

        return {
            "final_response": reply,
            "agent_display_name": AGENT_DISPLAY_NAMES["general"],
            "current_step": "general_complete",
        }
    except Exception as e:
        return {"error": f"General chat failed: {e}", "current_step": "general_failed"}