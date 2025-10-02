from langchain_core.tools import tool

@tool
def get_visa_requirements(country: str) -> str:
    """
    Get visa requirements for a country.

    Args:
        country: Country name

    Returns:
        Visa information string

    Example:
        get_visa_requirements("Japan")
    """
    # Mock database (in production, use official government APIs)
    visa_info = {
        "Japan": "Visa-free for US/EU/Australian citizens for stays up to 90 days. Passport must be valid for duration of stay.",
        "Italy": "Schengen visa. US/EU citizens visa-free for up to 90 days in 180-day period.",
        "Thailand": "Visa-free for most nationalities for 30-60 days. Confirm based on your nationality.",
        "France": "Schengen visa. US/EU citizens visa-free for up to 90 days in 180-day period.",
    }

    return visa_info.get(
        country,
        f"Check visa requirements for {country} based on your nationality at the embassy website."
    )


@tool
def get_currency_info(country: str) -> dict:
    """
    Get currency information for a country.

    Args:
        country: Country name

    Returns:
        Currency code, symbol, and exchange notes
    """
    currencies = {
        "Japan": {"code": "JPY", "symbol": "¥", "notes": "Cash still important, withdraw from 7-Eleven ATMs"},
        "Italy": {"code": "EUR", "symbol": "€", "notes": "Credit cards widely accepted, some small shops cash-only"},
        "Thailand": {"code": "THB", "symbol": "฿", "notes": "Cash preferred at markets, ATMs everywhere"},
        "France": {"code": "EUR", "symbol": "€", "notes": "Credit cards widely accepted"},
    }

    return currencies.get(
        country,
        {"code": "Unknown", "symbol": "?", "notes": "Check local currency requirements"}
    )
