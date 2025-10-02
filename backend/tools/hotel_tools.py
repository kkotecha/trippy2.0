from langchain_core.tools import tool
from typing import List, Dict

@tool
def search_hotels(
    city: str,
    nights: int,
    budget_tier: str
) -> List[Dict]:
    """
    Search for hotel accommodations in a city.

    Args:
        city: City name
        nights: Number of nights
        budget_tier: "budget", "moderate", or "luxury"

    Returns:
        List of 3 hotel recommendations with details

    Example:
        search_hotels("Tokyo", 4, "moderate")
    """
    # Price ranges per night
    price_ranges = {
        "budget": (30, 70),
        "moderate": (70, 150),
        "luxury": (150, 400)
    }

    min_price, max_price = price_ranges.get(budget_tier, (70, 150))
    mid_price = (min_price + max_price) // 2

    # Mock data (in production, use Booking.com API)
    hotels = [
        {
            "name": f"{city} Central Hotel",
            "type": "Hotel",
            "neighborhood": "City Center",
            "price_per_night": f"${mid_price}",
            "total_cost": f"${mid_price * nights}",
            "rating": 4.3,
            "amenities": ["WiFi", "Breakfast", "Gym"],
            "booking_link": f"https://booking.com/{city.lower()}-hotel-1",
            "why_recommended": "Central location, excellent transport links"
        },
        {
            "name": f"{city} Budget Inn",
            "type": "Hostel" if budget_tier == "budget" else "Hotel",
            "neighborhood": "Downtown",
            "price_per_night": f"${min_price + 10}",
            "total_cost": f"${(min_price + 10) * nights}",
            "rating": 4.1,
            "amenities": ["WiFi", "Shared kitchen"],
            "booking_link": f"https://hostelworld.com/{city.lower()}",
            "why_recommended": "Great value, social atmosphere"
        },
        {
            "name": f"{city} Boutique Stay",
            "type": "Boutique Hotel",
            "neighborhood": "Arts District",
            "price_per_night": f"${max_price - 20}",
            "total_cost": f"${(max_price - 20) * nights}",
            "rating": 4.7,
            "amenities": ["WiFi", "Rooftop bar", "Concierge"],
            "booking_link": f"https://booking.com/{city.lower()}-boutique",
            "why_recommended": "Unique character, local experience"
        }
    ]

    return hotels
