import httpx
from ..core.config import TOMORROW_IO_API_KEY

class WeatherService:
    """Service to fetch weather data for lakes using the Tomorrow.io API.

    Attributes:
        api_key (str): The API key for Tomorrow.io.

    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client()

    def get_weather_at_location(self, location: str) -> dict:
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
            "apikey": self.api_key,
            "accept-encoding": "deflate, gzip, br"
        }

        resp = self.client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
        
try:
    weather_service = WeatherService(TOMORROW_IO_API_KEY)
except Exception:
    weather_service = None
