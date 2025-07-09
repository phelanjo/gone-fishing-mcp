import httpx
from src.core.config import TOMORROW_IO_API_KEY

def get_weather_at_location(location: str) -> dict:
    """Fetches real-time weather data for a given location using Tomorrow.io API.
    
    Args:
        location (str): The location for which to fetch weather data. This should
                        be a string representing a city, state, or specific body
                        of water.
    
    Returns:
        dict: A dictionary containing the weather data for the specified location.
                The structure of the returned data will depend on the Tomorrow.io API
                response format.
    
    """
    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {
        "location": location,
        "units": "imperial"
    }
    headers = {
        "Accept": "application/json",
        "apikey": TOMORROW_IO_API_KEY,
        "accept-encoding": "deflate, gzip, br"
    }

    resp = httpx.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
