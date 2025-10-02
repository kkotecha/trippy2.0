from langchain_core.tools import tool
from typing import List, Optional
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@tool
def optimize_route(
    cities: List[str],
    starting_city: Optional[str] = None,
    country: Optional[str] = None
) -> List[str]:
    """
    Optimize city visiting order to minimize travel distance using greedy nearest-neighbor.

    Args:
        cities: List of city names to visit
        starting_city: Optional starting point
        country: Country name for geocoding context

    Returns:
        Optimized list of cities in visiting order

    Example:
        optimize_route(["Tokyo", "Kyoto", "Osaka"], "Tokyo", "Japan")
    """
    if len(cities) <= 2:
        return cities

    try:
        # Get coordinates
        geolocator = Nominatim(user_agent="trip_planner")
        city_coords = {}

        for city in cities:
            query = f"{city}, {country}" if country else city
            location = geolocator.geocode(query, timeout=10)
            if location:
                city_coords[city] = (location.latitude, location.longitude)

        # Greedy nearest-neighbor
        if starting_city and starting_city in city_coords:
            current = starting_city
        else:
            current = cities[0]

        route = [current]
        remaining = [c for c in cities if c != current and c in city_coords]

        while remaining:
            nearest = min(
                remaining,
                key=lambda c: geodesic(city_coords[current], city_coords[c]).km
            )
            route.append(nearest)
            remaining.remove(nearest)
            current = nearest

        return route

    except Exception as e:
        print(f"Route optimization failed: {e}")
        # Fallback: return original order with starting_city first
        if starting_city and starting_city in cities:
            cities_copy = [c for c in cities if c != starting_city]
            return [starting_city] + cities_copy
        return cities


@tool
def calculate_travel_time(
    from_city: str,
    to_city: str,
    country: Optional[str] = None
) -> dict:
    """
    Calculate estimated travel time between two cities.

    Args:
        from_city: Starting city
        to_city: Destination city
        country: Country name for context

    Returns:
        Dict with distance_km and estimated_hours

    Example:
        calculate_travel_time("Tokyo", "Kyoto", "Japan")
    """
    try:
        geolocator = Nominatim(user_agent="trip_planner")

        loc1 = geolocator.geocode(f"{from_city}, {country}" if country else from_city, timeout=10)
        loc2 = geolocator.geocode(f"{to_city}, {country}" if country else to_city, timeout=10)

        if loc1 and loc2:
            coords1 = (loc1.latitude, loc1.longitude)
            coords2 = (loc2.latitude, loc2.longitude)
            distance_km = geodesic(coords1, coords2).km

            # Estimate: 80 km/h average (mix of train/car)
            estimated_hours = distance_km / 80

            return {
                "distance_km": round(distance_km, 1),
                "estimated_hours": round(estimated_hours, 1),
                "from_city": from_city,
                "to_city": to_city
            }
    except Exception as e:
        print(f"Travel time calculation failed: {e}")

    # Fallback
    return {
        "distance_km": 200,
        "estimated_hours": 3,
        "from_city": from_city,
        "to_city": to_city,
        "note": "Estimated (calculation failed)"
    }
