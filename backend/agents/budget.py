from graph.state import TripPlannerState

def budget_compilation_node(state: TripPlannerState) -> dict:
    """
    Agent 7: Compile budget breakdown
    Role: Financial Synthesizer
    """
    city_plans = state["city_plans"]
    transport_legs = state["transport_legs"]
    budget_tier = state["budget_tier"]

    # Calculate accommodation costs
    total_accommodation = 0
    for city in city_plans:
        nights = city["nights"]
        # Use first hotel option for budget estimate
        if city["accommodation"]:
            price_str = city["accommodation"][0]["price_per_night"].replace("$", "")
            price = int(price_str)
            total_accommodation += price * nights

    # Calculate transport costs
    total_transport = 0
    for leg in transport_legs:
        cost_str = leg["cost"].replace("$", "").split("-")[0]
        total_transport += int(cost_str)

    # Estimate food costs
    food_per_day = {"budget": 30, "moderate": 60, "luxury": 120}[budget_tier]
    total_food = food_per_day * state["total_duration"]

    # Estimate activities
    activities_per_day = {"budget": 20, "moderate": 40, "luxury": 80}[budget_tier]
    total_activities = activities_per_day * state["total_duration"]

    # Local transport
    local_transport_per_day = 10
    total_local_transport = local_transport_per_day * state["total_duration"]

    grand_total = (
        total_accommodation +
        total_transport +
        total_food +
        total_activities +
        total_local_transport
    )

    return {
        "total_budget_estimate": grand_total,
        "budget_breakdown": {
            "accommodation": total_accommodation,
            "inter_city_transport": total_transport,
            "food": total_food,
            "activities": total_activities,
            "local_transport": total_local_transport,
            "total": grand_total
        },
        "money_saving_tips": [
            "Book accommodations 3+ months in advance for best rates",
            "Eat breakfast at convenience stores to save $10/day",
            "Use public transport instead of taxis",
            "Look for multi-day attraction passes"
        ]
    }
