import json

from mcp.server.fastmcp import FastMCP
from src.utils import get_location_and_weather_context

mcp = FastMCP()

@mcp.tool("get_location_and_weather_context")
def get_location_and_weather_context(prompt: str) -> dict:
    """
    Extracts location and weather information from the given prompt.

    This tool analyzes the input text to identify location references and retrieves
    corresponding weather data for that location. The extracted context is returned
    as a formatted JSON string.
    """
    try:
        result = get_location_and_weather_context(prompt)
        return json.dumps(result, indent=2)
    except Exception as e:
        return {"error": "Failed to extract additional context"}
    
def main():
    mcp.run()

if __name__ == "__main__":
    mcp.run()

