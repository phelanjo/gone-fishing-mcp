import json

import spacy
from .services.weather_service import weather_service

nlp = spacy.load("en_core_web_sm")

# Conversion Utils
def wind_degree_to_direction(degree: int) -> str:
    """Converts wind degree to a cardinal direction."""
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]
    
    # Round to nearest compass point, make sure it wraps around a full
    # circle (0-360 degrees) and then divide by 22.5 (360 degrees/16 directions)
    index = int((degree + 11.25) % 360 // 22.5)
    
    return directions[index]


# NLP Utils
def extract_location_entities_from_prompt(prompt):
    """Extracts location entities from a question using spaCy.

    spaCy uses Named Entity Recognition (NER) to identify geopolitical 
    entities (GPE. Think cities and states) and locations (LOC. Think Lakes, 
    Rivers, etc.), in the prompt text.

    Args:
        prompt (str): The input question or text from which to extract location
                      entities.

    Returns:
        dict: A dictionary containing the extracted location and hydro feature
        (if any). The dictionary has the following structure:
        
        {
            "location": value | value1, value2 | None,
            "hydro_feature": value | None
        }

    TODO:
        - Handle multiple hydro features if needed.
        - Handle other bodies of water (seas, oceans, etc.)

    """
    doc = nlp(prompt)
    states = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    hydro_features = [ent.text.removeprefix("the ") for ent in doc.ents if ent.label_ == "LOC"]

    # Sometimes hydro features are labeled as a GPEs instead of LOCs
    for state in states:
        if "lake" in state.lower():
            hydro_features.append(state)
            states.remove(state)

    return states[0], hydro_features[0]


# LLM Utils
def get_location_and_weather_context(prompt: str) -> dict:
    """Fetches weather data for a specific location based on a user prompt.

    This method extracts location entities from the provided prompt using
    Named Entity Recognition (NER) and retrieves weather data for the identified
    location.

    Args
        prompt (str): The question or prompt about fishing conditions at a body
                      of water in a specific state from the LLM.

    Returns
        dict: A dictionary containing the weather data for the specified location.
              The structure of the returned data will reflect the structure the MCP
              server is expecting.
    
        Example:
            {
                "state": "Arizona",
                "hydro_feature": "Patagonia Lake",
                "temperature": 94.2,
                "cloud_cover": 1,
                "humidity": 29,
                "precipitation_chance": 0,
                "wind_speed": 3.3,
                "wind_gust": 11,
                "wind_direction": "NNE",
                "uv_index": 11
            }
    """
    state, hydro_feature = extract_location_entities_from_prompt(prompt)
    
    weather_data = weather_service.get_weather_at_location(f"{hydro_feature} {state}")
    weather_data_values = weather_data.get("data", {}).get("values", {})

    wind_direction_degree = weather_data_values.get("windDirection", None)
    wind_direction_cardinal = wind_degree_to_direction(wind_direction_degree)

    # USGS water data is unreliable, commenting this out for now.
    # lat = weather_data.get("location", {}).get("lat", None)
    # lon = weather_data.get("location", {}).get("lon", None)
    # water_data = usgs_service.get_usgs_data(lat, lon)

    context = {
        "location": {
            "state": state,
            "hydro_feature": hydro_feature
        },
        "weather_conditions": {
            "temperature": weather_data_values.get("temperature", None),
            "cloud_cover": weather_data_values.get("cloudCover", None),
            "humidity": weather_data_values.get("humidity", None),
            "precipitation_chance": weather_data_values.get("precipitationProbability", None),
            "wind_speed": weather_data_values.get("windSpeed", None),
            "wind_gust": weather_data_values.get("windGust", None),
            "wind_direction": wind_direction_cardinal,
            "uv_index": weather_data_values.get("uvIndex", None),
        }
    }

    return context

def build_role_prompts(user_prompt: str, additional_context: dict):
    """Builds role prompts for the LLM based on user input and additional context.
    
    Args:
        user_prompt (str): The user's question or prompt about fishing conditions.
        additional_context (dict): A dictionary containing weather and location data.
        
    Returns:
        list: A list of dictionaries representing the role prompts for the LLM.
    """
    system_prompt = (
        "Context (Units are in imperial - Fahrenheit, mph, etc.):\n"
        f"{json.dumps(additional_context, indent=2)}\n\n"
        "You are a fishing expert.\n\n"
        "Based on the provided context, answer the user's question about "
        "fishing conditions at a body of water in a specific state. "
        "Include recommendations for lures to use and areas to fish based on "
        "the weather conditions.\n\n"
        "Answer in a friendly tone, as if you were talking to a fellow fisherman."
    )

    role_prompts = [
        {
            "role": "user",
            "content": user_prompt
        },
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    return role_prompts
