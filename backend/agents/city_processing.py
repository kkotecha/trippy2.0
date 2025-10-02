from graph.state import CityState, TripPlannerState
from tools import search_hotels, search_attractions
from langgraph.graph import StateGraph, END

def accommodation_node(state: CityState) -> dict:
    """Find accommodations for the city"""
    hotels = search_hotels.invoke({
        "city": state["city_name"],
        "nights": state["nights"],
        "budget_tier": state["budget_tier"]
    })
    return {"accommodation_options": hotels}

def itinerary_node(state: CityState) -> dict:
    """Create daily itinerary for the city"""
    attractions = search_attractions.invoke({
        "city": state["city_name"],
        "interests": state["interests"],
        "max_results": state["nights"] * 3
    })

    # Create simple day-by-day plan
    daily_itinerary = []
    for day in range(1, state["nights"] + 1):
        start_idx = (day - 1) * 3
        day_attractions = attractions[start_idx:start_idx + 3]

        daily_itinerary.append({
            "day": day,
            "title": f"Day {day} in {state['city_name']}",
            "activities": [
                {
                    "time": "09:00" if i == 0 else "13:00" if i == 1 else "17:00",
                    "activity": attr["name"],
                    "location": attr["address"],
                    "duration": attr["duration_recommended"],
                    "cost": attr["cost"],
                    "tips": attr.get("description", "")
                }
                for i, attr in enumerate(day_attractions)
            ],
            "meals": {
                "breakfast": "Local cafe ($10)",
                "lunch": "Restaurant near attractions ($20)",
                "dinner": "Traditional local cuisine ($30)"
            },
            "daily_cost": "$100"
        })

    return {"daily_itinerary": daily_itinerary}

def local_transport_node(state: CityState) -> dict:
    """Get local transportation info for the city"""
    transport_info = {
        "metro_system": f"{state['city_name']} Metro/Subway",
        "day_pass_cost": "$10",
        "taxi_apps": ["Uber", "Local Taxi App"],
        "bike_rentals": "Available in city center",
        "walking_friendly": True,
        "notes": "Public transport recommended"
    }
    return {"local_transport_info": transport_info}

def create_city_subgraph():
    """Create subgraph for processing one city"""
    city_graph = StateGraph(CityState)

    city_graph.add_node("accommodation", accommodation_node)
    city_graph.add_node("itinerary", itinerary_node)
    city_graph.add_node("local_transport", local_transport_node)

    city_graph.set_entry_point("accommodation")
    city_graph.add_edge("accommodation", "itinerary")
    city_graph.add_edge("itinerary", "local_transport")
    city_graph.add_edge("local_transport", END)

    return city_graph.compile()

def process_cities_node(state: TripPlannerState) -> dict:
    """Process all cities (can be parallelized later)"""
    city_subgraph = create_city_subgraph()
    city_plans = []

    for city in state["city_route"]:
        city_state = {
            "city_name": city,
            "nights": state["nights_per_city"][city],
            "interests": state["interests"],
            "budget_tier": state["budget_tier"]
        }

        result = city_subgraph.invoke(city_state)

        city_plans.append({
            "city_name": city,
            "nights": result["nights"],
            "accommodation": result["accommodation_options"],
            "itinerary": result["daily_itinerary"],
            "local_transport": result["local_transport_info"]
        })

    return {"city_plans": city_plans}
