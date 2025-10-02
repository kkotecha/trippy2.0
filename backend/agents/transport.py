from graph.state import TripPlannerState
from tools import search_trains

def transport_planning_node(state: TripPlannerState) -> dict:
    """
    Agent 3: Plan inter-city transportation
    Role: Transportation Coordinator
    Tools: search_trains (in production: + search_flights, search_buses)
    """
    city_route = state["city_route"]
    country = state["country"]

    transport_legs = []

    for i in range(len(city_route) - 1):
        from_city = city_route[i]
        to_city = city_route[i + 1]

        # Search for trains
        train_info = search_trains.invoke({
            "from_city": from_city,
            "to_city": to_city,
            "country": country
        })

        transport_legs.append({
            "from": from_city,
            "to": to_city,
            "method": train_info["method"],
            "duration": train_info["duration"],
            "cost": train_info["cost"],
            "booking_info": train_info["booking_info"],
            "notes": train_info.get("notes", "")
        })

    return {"transport_legs": transport_legs}
