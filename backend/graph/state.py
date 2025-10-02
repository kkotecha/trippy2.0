from typing import TypedDict, List, Dict, Optional, Annotated
import operator

class TripPlannerState(TypedDict):
    """State that flows through all agents in the workflow"""

    # User inputs (immutable)
    country: str
    total_duration: int
    interests: List[str]
    budget_tier: str  # "budget" | "moderate" | "luxury"
    num_cities: Optional[int]
    starting_city: Optional[str]
    travel_pace: str  # "relaxed" | "moderate" | "fast"

    # Agent outputs (accumulated)
    messages: Annotated[List, operator.add]  # For LLM message history

    # Agent 1: Country Research
    country_overview: str
    best_months_to_visit: str
    visa_info: str
    safety_info: str

    # Agent 2: Route Planning
    recommended_cities: List[str]
    city_route: List[str]  # Optimized order
    nights_per_city: Dict[str, int]
    route_rationale: str

    # Agent 3: Inter-City Transport
    transport_legs: List[Dict]  # [{from, to, method, cost, duration}]

    # Agents 4-6: Per-City Processing (accumulated from subgraph)
    city_plans: Annotated[List[Dict], operator.add]

    # Agent 7: Budget
    total_budget_estimate: float
    budget_breakdown: Dict
    money_saving_tips: List[str]

    # Agent 8: Logistics
    packing_list: List[str]
    travel_logistics: Dict

    # Agent 9: Final Compiler
    final_response: Dict


class CityState(TypedDict):
    """State for processing a single city in the subgraph"""
    city_name: str
    nights: int
    interests: List[str]
    budget_tier: str

    # Outputs
    accommodation_options: List[Dict]
    daily_itinerary: List[Dict]
    local_transport_info: Dict
