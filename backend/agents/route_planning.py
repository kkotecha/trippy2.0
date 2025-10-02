from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import List, Dict
from graph.state import TripPlannerState
from tools import optimize_route, calculate_travel_time, web_search
from config import OPENAI_MODEL

class RouteOutput(BaseModel):
    """Structured output for route planning"""
    recommended_cities: List[str]
    route_rationale: str

def route_planning_node(state: TripPlannerState) -> dict:
    """
    Agent 2: Plan optimal city route
    Role: Journey Architect
    Tools: optimize_route, calculate_travel_time, web_search
    """
    country = state["country"]
    duration = state["total_duration"]
    interests = state["interests"]
    starting_city = state.get("starting_city")
    travel_pace = state["travel_pace"]
    num_cities = state.get("num_cities")

    # Determine min nights per city based on pace
    min_nights = {"relaxed": 3, "moderate": 2, "fast": 2}[travel_pace]
    max_cities = duration // min_nights if not num_cities else num_cities

    system_prompt = f"""You are a Journey Architect specialized in multi-city travel planning.

Task: Create an optimal {duration}-day route through {country}.

Interests: {", ".join(interests)}
Travel pace: {travel_pace}
Starting city: {starting_city or "You decide"}
Target cities: {max_cities}

Guidelines:
1. Recommend cities matching interests
2. Ensure minimum {min_nights} nights per city
3. Optimize route to minimize backtracking
4. Balance city importance with travel time
5. Account for travel days

Use web_search to find top cities in {country} for {interests}.
Then use optimize_route to minimize travel distance.

Output cities, route order, nights allocation, and rationale."""

    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.5)
    structured_llm = llm.with_structured_output(RouteOutput)

    # First, get city recommendations
    search_result = web_search.invoke({
        "query": f"top cities to visit in {country} for {' '.join(interests[:3])}"
    })

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Research results:\n{search_result}\n\nNow create the optimal route.")
    ]

    result = structured_llm.invoke(messages)

    # Optimize route order
    optimized_route = optimize_route.invoke({
        "cities": result.recommended_cities[:max_cities],
        "starting_city": starting_city,
        "country": country
    })

    # Calculate nights per city
    num_cities_final = len(optimized_route)
    nights_per_city = {}

    # Allocate nights evenly, giving extra nights to earlier cities
    base_nights = duration // num_cities_final
    extra_nights = duration % num_cities_final

    for i, city in enumerate(optimized_route):
        if i < extra_nights:
            nights_per_city[city] = base_nights + 1
        else:
            nights_per_city[city] = base_nights

    return {
        "recommended_cities": result.recommended_cities[:max_cities],
        "city_route": optimized_route,
        "nights_per_city": nights_per_city,
        "route_rationale": result.route_rationale
    }
