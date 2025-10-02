from graph.state import TripPlannerState
from tools import get_visa_requirements, get_currency_info

def logistics_node(state: TripPlannerState) -> dict:
    """
    Agent 8: Provide travel logistics
    Role: Travel Preparation Expert
    """
    country = state["country"]
    duration = state["total_duration"]

    visa_info = get_visa_requirements.invoke({"country": country})
    currency_info = get_currency_info.invoke({"country": country})

    packing_list = [
        "Passport (valid 6+ months)",
        "Comfortable walking shoes",
        "Weather-appropriate clothing",
        "Universal power adapter",
        "Portable charger",
        "Medications + prescriptions",
        "Travel insurance documents",
        "Copies of important documents"
    ]

    travel_logistics = {
        "visa_requirements": visa_info,
        "currency": currency_info,
        "health_precautions": "Check CDC travel health notices. No special vaccinations typically required.",
        "emergency_contacts": f"Local emergency number: 112 (EU) or check {country} emergency services",
        "connectivity": "Consider buying local SIM card or portable WiFi at airport",
        "tipping_culture": "Research local tipping customs",
        "best_time_to_visit": state.get("best_months_to_visit", "Spring/Fall generally best"),
        "time_zone": f"Check time zone for {country}",
        "language_tips": "Download Google Translate offline language pack"
    }

    return {
        "packing_list": packing_list,
        "travel_logistics": travel_logistics
    }
