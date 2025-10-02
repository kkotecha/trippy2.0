from langchain_core.tools import tool
from typing import List, Dict

@tool
def search_attractions(
    city: str,
    interests: List[str],
    max_results: int = 10
) -> List[Dict]:
    """
    Find tourist attractions matching interests.

    Args:
        city: City name
        interests: List of interest categories
        max_results: Maximum attractions to return

    Returns:
        List of attractions with details

    Example:
        search_attractions("Tokyo", ["temples", "food"], 5)
    """
    # Mock data (in production, use Google Places API or TripAdvisor)
    all_attractions = [
        {
            "name": f"{city} Historic Temple",
            "category": "temple",
            "rating": 4.7,
            "cost": "Free (donations welcome)",
            "address": f"123 Temple St, {city}",
            "description": "Ancient temple with beautiful gardens",
            "hours": "6 AM - 6 PM",
            "duration_recommended": "1-2 hours"
        },
        {
            "name": f"{city} Food Market",
            "category": "food",
            "rating": 4.8,
            "cost": "$10-30 for meals",
            "address": f"45 Market Ave, {city}",
            "description": "Local street food and fresh produce",
            "hours": "8 AM - 8 PM",
            "duration_recommended": "2-3 hours"
        },
        {
            "name": f"{city} Art Museum",
            "category": "museum",
            "rating": 4.6,
            "cost": "$15",
            "address": f"78 Museum Rd, {city}",
            "description": "Contemporary and classical art collection",
            "hours": "10 AM - 6 PM, closed Mondays",
            "duration_recommended": "2-3 hours"
        },
        {
            "name": f"{city} Technology Center",
            "category": "technology",
            "rating": 4.5,
            "cost": "$20",
            "address": f"90 Tech Plaza, {city}",
            "description": "Interactive tech exhibits and demos",
            "hours": "9 AM - 7 PM",
            "duration_recommended": "2-4 hours"
        }
    ]

    # Filter by interests
    filtered = []
    for attraction in all_attractions:
        if any(interest.lower() in attraction['category'].lower()
               for interest in interests):
            filtered.append(attraction)

    # If no matches, return general attractions
    if not filtered:
        filtered = all_attractions

    return filtered[:max_results]
