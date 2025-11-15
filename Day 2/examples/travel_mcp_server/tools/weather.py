import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
# Look for .env in the parent directory (travel_mcp_server/)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key
ACCUWEATHER_API_KEY = os.getenv('ACCUWEATHER_API_KEY')

# AccuWeather API base URL
ACCUWEATHER_BASE_URL = "http://dataservice.accuweather.com"


def get_location_key(city_name: str) -> dict:
    """
    Get AccuWeather location key for a city.
    
    Args:
        city_name: Name of the city to search for
    
    Returns:
        Dictionary with status and either location data or error message
    """
    if not ACCUWEATHER_API_KEY:
        return {
            "status": "error",
            "error_message": "ACCUWEATHER_API_KEY not found in environment variables. Please check your .env file."
        }
    
    try:
        url = f"{ACCUWEATHER_BASE_URL}/locations/v1/cities/search"
        params = {
            "apikey": ACCUWEATHER_API_KEY,
            "q": city_name
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        # Check for API errors
        if response.status_code == 401:
            return {
                "status": "error",
                "error_message": "Invalid AccuWeather API key. Please check your ACCUWEATHER_API_KEY in .env file."
            }
        elif response.status_code == 503:
            return {
                "status": "error",
                "error_message": "AccuWeather API is temporarily unavailable. Please try again in a few moments."
            }
        elif response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"AccuWeather API error: {response.status_code}. Please try again later."
            }
        
        locations = response.json()
        
        if not locations or len(locations) == 0:
            return {
                "status": "error",
                "error_message": f"Location '{city_name}' not found. Please check the city name and try again with a more specific name (e.g., 'Paris, France')."
            }
        
        # Return the first (most relevant) location
        location = locations[0]
        return {
            "status": "success",
            "location_key": location["Key"],
            "city_name": location["LocalizedName"],
            "country": location["Country"]["LocalizedName"],
            "administrative_area": location.get("AdministrativeArea", {}).get("LocalizedName", "")
        }
        
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_message": "AccuWeather API request timed out. Please check your internet connection and try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error_message": "Could not connect to AccuWeather API. Please check your internet connection."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error while looking up location: {str(e)}"
        }


def get_forecast(location_key: str) -> dict:
    """
    Get 5-day weather forecast from AccuWeather.
    
    Args:
        location_key: AccuWeather location key
    
    Returns:
        Dictionary with status and either forecast data or error message
    """
    if not ACCUWEATHER_API_KEY:
        return {
            "status": "error",
            "error_message": "ACCUWEATHER_API_KEY not found in environment variables."
        }
    
    try:
        url = f"{ACCUWEATHER_BASE_URL}/forecasts/v1/daily/5day/{location_key}"
        params = {
            "apikey": ACCUWEATHER_API_KEY,
            "details": "true",
            "metric": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 401:
            return {
                "status": "error",
                "error_message": "Invalid AccuWeather API key."
            }
        elif response.status_code == 503:
            return {
                "status": "error",
                "error_message": "AccuWeather API is temporarily unavailable. Please try again later."
            }
        elif response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"AccuWeather API error: {response.status_code}"
            }
        
        forecast_data = response.json()
        return {
            "status": "success",
            "forecast": forecast_data
        }
        
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_message": "AccuWeather API request timed out. Please try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error_message": "Could not connect to AccuWeather API. Please check your internet connection."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error fetching forecast: {str(e)}"
        }


def generate_packing_suggestions(temp_min: float, temp_max: float, conditions: str) -> list:
    """
    Generate packing suggestions based on weather conditions.
    
    Args:
        temp_min: Minimum temperature in Celsius
        temp_max: Maximum temperature in Celsius
        conditions: Weather condition description
    
    Returns:
        List of packing suggestions
    """
    suggestions = []
    
    # Temperature-based suggestions
    if temp_max >= 30:
        suggestions.extend(["Light, breathable clothing", "Sunscreen", "Hat", "Sunglasses", "Water bottle"])
    elif temp_max >= 20:
        suggestions.extend(["Light clothing", "Sunglasses", "Light jacket for evenings"])
    elif temp_max >= 10:
        suggestions.extend(["Layers", "Medium jacket", "Comfortable walking shoes"])
    else:
        suggestions.extend(["Warm coat", "Gloves", "Scarf", "Warm layers"])
    
    # Add cold weather items if minimum is low
    if temp_min <= 0:
        suggestions.extend(["Heavy winter coat", "Thermal underwear", "Warm boots"])
    elif temp_min <= 10:
        suggestions.append("Warm jacket")
    
    # Condition-based suggestions
    conditions_lower = conditions.lower()
    if any(word in conditions_lower for word in ["rain", "shower", "storm"]):
        suggestions.extend(["Umbrella", "Waterproof jacket", "Waterproof shoes"])
    
    if "snow" in conditions_lower:
        suggestions.extend(["Snow boots", "Waterproof gloves", "Winter accessories"])
    
    if any(word in conditions_lower for word in ["sun", "clear", "hot"]):
        if "Sunscreen" not in suggestions:
            suggestions.append("Sunscreen")
        if "Sunglasses" not in suggestions:
            suggestions.append("Sunglasses")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for item in suggestions:
        if item not in seen:
            seen.add(item)
            unique_suggestions.append(item)
    
    return unique_suggestions


def get_weather_forecast(destination: str, travel_dates: str) -> dict:
    """
    Get weather forecast for a travel destination using AccuWeather API.
    
    This function fetches real weather data from AccuWeather and provides
    detailed forecasts along with packing suggestions.
    
    Args:
        destination: City name (e.g., "Paris", "Tokyo, Japan", "New York, USA")
        travel_dates: Date range in format "YYYY-MM-DD to YYYY-MM-DD"
    
    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - destination: Full city name
        - country: Country name
        - dates: Travel dates
        - forecast: Daily forecast details
        - temperature_summary: Overall temperature range
        - conditions_summary: Summary of conditions
        - packing_suggestions: List of items to pack
        - error_message: Only present if status is "error"
    """
    
    # Step 1: Get location key for the destination
    location_result = get_location_key(destination)
    
    if location_result["status"] == "error":
        return location_result
    
    location_key = location_result["location_key"]
    city_name = location_result["city_name"]
    country = location_result["country"]
    
    # Step 2: Get weather forecast
    forecast_result = get_forecast(location_key)
    
    if forecast_result["status"] == "error":
        return forecast_result
    
    forecast_data = forecast_result["forecast"]
    
    # Step 3: Process forecast data
    daily_forecasts = []
    all_temps_min = []
    all_temps_max = []
    all_conditions = []
    
    for day in forecast_data.get("DailyForecasts", []):
        date = day.get("Date", "").split("T")[0]  # Extract date part
        
        temp_min = day.get("Temperature", {}).get("Minimum", {}).get("Value", 0)
        temp_max = day.get("Temperature", {}).get("Maximum", {}).get("Value", 0)
        
        day_condition = day.get("Day", {}).get("IconPhrase", "Unknown")
        night_condition = day.get("Night", {}).get("IconPhrase", "Unknown")
        
        # Collect overall stats
        all_temps_min.append(temp_min)
        all_temps_max.append(temp_max)
        all_conditions.append(day_condition)
        
        daily_forecasts.append({
            "date": date,
            "temperature_min_celsius": temp_min,
            "temperature_max_celsius": temp_max,
            "temperature_min_fahrenheit": round(temp_min * 9/5 + 32),
            "temperature_max_fahrenheit": round(temp_max * 9/5 + 32),
            "day_condition": day_condition,
            "night_condition": night_condition,
            "precipitation_probability_day": day.get("Day", {}).get("PrecipitationProbability", 0),
            "precipitation_probability_night": day.get("Night", {}).get("PrecipitationProbability", 0)
        })
    
    # Calculate overall temperature range
    overall_min = min(all_temps_min) if all_temps_min else 0
    overall_max = max(all_temps_max) if all_temps_max else 0
    
    # Get most common condition for summary
    conditions_summary = ", ".join(set(all_conditions[:3]))  # First 3 unique conditions
    
    # Generate packing suggestions
    packing_suggestions = generate_packing_suggestions(
        overall_min,
        overall_max,
        conditions_summary
    )
    
    # Build response
    return {
        "status": "success",
        "destination": city_name,
        "country": country,
        "dates": travel_dates,
        "forecast_period": f"{len(daily_forecasts)}-day forecast",
        "temperature_summary": {
            "overall_min_celsius": overall_min,
            "overall_max_celsius": overall_max,
            "overall_min_fahrenheit": round(overall_min * 9/5 + 32),
            "overall_max_fahrenheit": round(overall_max * 9/5 + 32)
        },
        "conditions_summary": conditions_summary,
        "daily_forecasts": daily_forecasts,
        "packing_suggestions": packing_suggestions,
        "data_source": "AccuWeather API"
    }


# Example usage for testing
if __name__ == "__main__":
    print("=" * 70)
    print("AccuWeather API Integration Test")
    print("=" * 70)
    
    # Check if API key is loaded
    if not ACCUWEATHER_API_KEY:
        print("\n❌ ERROR: ACCUWEATHER_API_KEY not found!")
        print("Please create a .env file in the travel_mcp_server directory with:")
        print("ACCUWEATHER_API_KEY=your_api_key_here")
    else:
        print(f"\n✅ API Key loaded: {ACCUWEATHER_API_KEY[:10]}...{ACCUWEATHER_API_KEY[-5:]}")
    
    print("\n" + "-" * 70)
    print("Test 1: Valid destination (Paris)")
    print("-" * 70)
    result = get_weather_forecast("Paris", "2025-06-15 to 2025-06-22")
    
    if result["status"] == "success":
        print(f"✅ Success!")
        print(f"   Destination: {result['destination']}, {result['country']}")
        print(f"   Temperature Range: {result['temperature_summary']['overall_min_celsius']}°C - {result['temperature_summary']['overall_max_celsius']}°C")
        print(f"   Conditions: {result['conditions_summary']}")
        print(f"   Packing Suggestions: {', '.join(result['packing_suggestions'][:5])}")
        print(f"\n   Daily Forecasts:")
        for forecast in result['daily_forecasts'][:3]:  # Show first 3 days
            print(f"     {forecast['date']}: {forecast['temperature_min_celsius']}°C - {forecast['temperature_max_celsius']}°C, {forecast['day_condition']}")
    else:
        print(f"❌ Error: {result['error_message']}")
    
    print("\n" + "-" * 70)
    print("Test 2: Invalid destination")
    print("-" * 70)
    result = get_weather_forecast("XYZ12345", "2025-06-15 to 2025-06-22")
    
    if result["status"] == "error":
        print(f"✅ Error handling works correctly")
        print(f"   Error message: {result['error_message']}")
    else:
        print(f"⚠️  Expected error but got success")
    
    print("\n" + "=" * 70)
