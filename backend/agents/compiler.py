from graph.state import TripPlannerState

def compiler_node(state: TripPlannerState) -> dict:
    """
    Agent 9: Compile final response
    Role: Output Formatter
    """
    final_response = {
        "country": state["country"],
        "total_duration": state["total_duration"],
        "cities_count": len(state["city_route"]),
        "journey_overview": {
            "route": state["city_route"],
            "nights_per_city": state["nights_per_city"],
            "total_budget_estimate": f"${state['total_budget_estimate']}",
            "travel_pace": state["travel_pace"],
            "route_rationale": state.get("route_rationale", "Optimized for minimal travel time")
        },
        "city_plans": state["city_plans"],
        "transport_legs": state["transport_legs"],
        "budget_summary": {
            "breakdown": state["budget_breakdown"],
            "money_saving_tips": state["money_saving_tips"]
        },
        "logistics": {
            "packing_list": state["packing_list"],
            "travel_info": state["travel_logistics"]
        },
        "country_overview": state.get("country_overview", ""),
        "best_time_to_visit": state.get("best_months_to_visit", "")
    }

    return {"final_response": final_response}
