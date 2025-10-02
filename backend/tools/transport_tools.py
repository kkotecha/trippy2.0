from langchain_core.tools import tool
from typing import Dict

@tool
def search_trains(
    from_city: str,
    to_city: str,
    country: str
) -> Dict:
    """
    Search for train routes between cities.

    Args:
        from_city: Departure city
        to_city: Arrival city
        country: Country name

    Returns:
        Train options with method, duration, cost, booking info

    Example:
        search_trains("Tokyo", "Kyoto", "Japan")
    """
    # Mock database (in production, use Rome2Rio or national rail APIs)
    routes = {
        ("Tokyo", "Kyoto", "Japan"): {
            "method": "Shinkansen (bullet train)",
            "duration": "2h 15min",
            "cost": "$130",
            "booking_info": "Book via JR Pass or at station",
            "frequency": "Every 10-20 minutes",
            "notes": "Covered by JR Pass"
        },
        ("Kyoto", "Osaka", "Japan"): {
            "method": "JR Special Rapid",
            "duration": "30 minutes",
            "cost": "$8",
            "booking_info": "No reservation needed",
            "frequency": "Every 10 minutes",
            "notes": "Very frequent service"
        },
        ("Paris", "Lyon", "France"): {
            "method": "TGV",
            "duration": "2 hours",
            "cost": "$70",
            "booking_info": "Book via SNCF or Trainline",
            "frequency": "Hourly",
            "notes": "Book early for discounts"
        }
    }

    key = (from_city, to_city, country)
    if key in routes:
        return routes[key]

    # Fallback
    return {
        "method": "Train (check local schedules)",
        "duration": "3-5 hours",
        "cost": "$50-100",
        "booking_info": f"Check {country} national railway website",
        "frequency": "Varies",
        "notes": "Exact schedules available closer to travel date"
    }
