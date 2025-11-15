"""
Flight search tool for travel planning using Aviation Stack API.

This tool provides flight information between airports. Due to free tier
limitations, it uses real API for current flights and mock data for future dates.
"""

import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

AVIATION_STACK_API_KEY = os.getenv('AVIATION_STACK_API_KEY')
AVIATION_STACK_BASE_URL = "https://api.aviationstack.com/v1"


# IATA code mapping for major airports
AIRPORT_DATABASE = {
    "jfk": {"name": "John F. Kennedy International", "city": "New York", "country": "USA"},
    "lax": {"name": "Los Angeles International", "city": "Los Angeles", "country": "USA"},
    "lhr": {"name": "London Heathrow", "city": "London", "country": "UK"},
    "cdg": {"name": "Charles de Gaulle", "city": "Paris", "country": "France"},
    "nrt": {"name": "Narita International", "city": "Tokyo", "country": "Japan"},
    "dxb": {"name": "Dubai International", "city": "Dubai", "country": "UAE"},
    "del": {"name": "Indira Gandhi International", "city": "Delhi", "country": "India"},
    "bom": {"name": "Chhatrapati Shivaji Maharaj International", "city": "Mumbai", "country": "India"},
    "sfo": {"name": "San Francisco International", "city": "San Francisco", "country": "USA"},
    "ord": {"name": "O'Hare International", "city": "Chicago", "country": "USA"},
    "fra": {"name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany"},
    "ams": {"name": "Amsterdam Airport Schiphol", "city": "Amsterdam", "country": "Netherlands"},
    "hnd": {"name": "Tokyo Haneda", "city": "Tokyo", "country": "Japan"},
    "sin": {"name": "Singapore Changi", "city": "Singapore", "country": "Singapore"},
    "syd": {"name": "Sydney Kingsford Smith", "city": "Sydney", "country": "Australia"},
}


def validate_airport_code(code: str) -> dict:
    """
    Validate and get airport information.
    
    Args:
        code: IATA airport code (3 letters)
    
    Returns:
        Dictionary with airport info or error
    """
    code_lower = code.lower().strip()
    
    if len(code) != 3:
        return {
            "status": "error",
            "error_message": f"Invalid airport code '{code}'. Airport codes must be 3 letters (e.g., JFK, LAX, LHR)."
        }
    
    if code_lower not in AIRPORT_DATABASE:
        return {
            "status": "error",
            "error_message": f"Airport code '{code.upper()}' not found in database. Please use common airport codes like JFK, LAX, LHR, CDG, NRT, DEL, BOM, etc."
        }
    
    return {
        "status": "success",
        "code": code.upper(),
        "info": AIRPORT_DATABASE[code_lower]
    }


def generate_mock_flights(origin: str, destination: str, departure_date: str) -> list:
    """
    Generate mock flight data for future dates (Aviation Stack free tier limitation).
    
    Args:
        origin: Origin airport IATA code
        destination: Destination airport IATA code
        departure_date: Departure date
    
    Returns:
        List of mock flight dictionaries
    """
    # Mock airlines and their typical routes
    airlines = [
        {"name": "Delta Air Lines", "iata": "DL"},
        {"name": "American Airlines", "iata": "AA"},
        {"name": "United Airlines", "iata": "UA"},
        {"name": "Emirates", "iata": "EK"},
        {"name": "Lufthansa", "iata": "LH"},
        {"name": "British Airways", "iata": "BA"},
        {"name": "Air France", "iata": "AF"},
    ]
    
    # Generate 3-5 mock flights
    import random
    num_flights = random.randint(3, 5)
    flights = []
    
    origin_info = AIRPORT_DATABASE[origin.lower()]
    dest_info = AIRPORT_DATABASE[destination.lower()]
    
    # Calculate approximate flight duration based on common routes
    base_durations = {
        ("jfk", "lax"): 6, ("jfk", "lhr"): 7, ("jfk", "cdg"): 7,
        ("lax", "nrt"): 11, ("lhr", "cdg"): 1.5, ("lhr", "dxb"): 7,
        ("del", "bom"): 2, ("jfk", "del"): 14, ("lax", "del"): 16,
    }
    
    route_key = (origin.lower(), destination.lower())
    reverse_key = (destination.lower(), origin.lower())
    duration_hours = base_durations.get(route_key) or base_durations.get(reverse_key, 8)
    
    for i in range(num_flights):
        airline = random.choice(airlines)
        flight_num = random.randint(100, 999)
        
        # Stagger departure times throughout the day
        hour = 6 + (i * 3) + random.randint(0, 2)
        minute = random.choice([0, 15, 30, 45])
        
        departure_time = f"{hour:02d}:{minute:02d}"
        arrival_hour = (hour + int(duration_hours)) % 24
        arrival_minute = (minute + int((duration_hours % 1) * 60)) % 60
        arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
        
        # Generate price (mock)
        base_price = 300
        distance_factor = duration_hours * 50
        price = int(base_price + distance_factor + random.randint(-100, 200))
        
        flights.append({
            "flight_date": departure_date,
            "airline": airline,
            "flight_number": f"{airline['iata']}{flight_num}",
            "departure": {
                "airport": origin_info["name"],
                "iata": origin.upper(),
                "city": origin_info["city"],
                "scheduled_time": departure_time,
            },
            "arrival": {
                "airport": dest_info["name"],
                "iata": destination.upper(),
                "city": dest_info["city"],
                "scheduled_time": arrival_time,
            },
            "duration_hours": round(duration_hours, 1),
            "price_usd": price,
            "aircraft_type": random.choice(["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A350"]),
            "stops": 0 if duration_hours < 10 else random.choice([0, 1]),
        })
    
    # Sort by departure time
    flights.sort(key=lambda x: x["departure"]["scheduled_time"])
    
    return flights


def search_flights(origin: str, destination: str, departure_date: str) -> dict:
    """
    Search for flights between two airports.
    
    Due to Aviation Stack API free tier limitations (only current flights),
    this function uses mock data for future dates and real data for current date.
    
    Args:
        origin: Origin airport IATA code (e.g., "JFK", "LAX", "LHR")
        destination: Destination airport IATA code
        departure_date: Departure date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - flights: List of flight options
        - route: Origin and destination info
        - data_source: Where the data came from
        - error_message: Only present if status is "error"
    """
    
    # Check API key
    if not AVIATION_STACK_API_KEY:
        return {
            "status": "error",
            "error_message": "AVIATION_STACK_API_KEY not found in environment variables. Please check your .env file."
        }
    
    # Validate origin airport
    origin_validation = validate_airport_code(origin)
    if origin_validation["status"] == "error":
        return origin_validation
    
    # Validate destination airport
    dest_validation = validate_airport_code(destination)
    if dest_validation["status"] == "error":
        return dest_validation
    
    origin_code = origin_validation["code"]
    dest_code = dest_validation["code"]
    origin_info = origin_validation["info"]
    dest_info = dest_validation["info"]
    
    # Parse and validate date
    try:
        flight_date = datetime.strptime(departure_date, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format '{departure_date}'. Please use YYYY-MM-DD format (e.g., '2025-06-15')."
        }
    
    # Check if date is in the past
    today = datetime.now().date()
    if flight_date.date() < today:
        return {
            "status": "error",
            "error_message": f"Cannot search flights for past date '{departure_date}'. Please provide a current or future date."
        }
    
    # Try real API first for all dates
    # Will fall back to mock data only if API fails or returns no results
    flights_data = []
    data_source = ""
    use_real_api = True
    
    if use_real_api:
        # Try to get real flight data from Aviation Stack API
        try:
            url = f"{AVIATION_STACK_BASE_URL}/flights"
            params = {
                "access_key": AVIATION_STACK_API_KEY,
                "dep_iata": origin_code,
                "arr_iata": dest_code,
                "flight_date": departure_date,  # Add the date parameter!
                "limit": 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 401:
                return {
                    "status": "error",
                    "error_message": "Invalid Aviation Stack API key. Please check your AVIATION_STACK_API_KEY in .env file."
                }
            elif response.status_code != 200:
                # Fallback to mock data if API fails
                use_real_api = False
            else:
                api_data = response.json()
                
                if api_data.get("data"):
                    # Process real API data
                    for flight in api_data["data"][:5]:  # Limit to 5 flights
                        flights_data.append({
                            "flight_date": flight.get("flight_date"),
                            "airline": {
                                "name": flight.get("airline", {}).get("name", "Unknown"),
                                "iata": flight.get("airline", {}).get("iata", "")
                            },
                            "flight_number": flight.get("flight", {}).get("iata", ""),
                            "departure": {
                                "airport": flight.get("departure", {}).get("airport", ""),
                                "iata": flight.get("departure", {}).get("iata", origin_code),
                                "city": origin_info["city"],
                                "scheduled_time": flight.get("departure", {}).get("scheduled", "").split("T")[1][:5] if flight.get("departure", {}).get("scheduled") else "",
                            },
                            "arrival": {
                                "airport": flight.get("arrival", {}).get("airport", ""),
                                "iata": flight.get("arrival", {}).get("iata", dest_code),
                                "city": dest_info["city"],
                                "scheduled_time": flight.get("arrival", {}).get("scheduled", "").split("T")[1][:5] if flight.get("arrival", {}).get("scheduled") else "",
                            },
                            "status": flight.get("flight_status", "scheduled")
                        })
                    data_source = "Aviation Stack API (Real-time)"
                else:
                    # No flights found, use mock data
                    use_real_api = False
                    
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error_message": "Aviation Stack API request timed out. Please check your internet connection and try again."
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "error_message": "Could not connect to Aviation Stack API. Please check your internet connection."
            }
        except Exception as e:
            # Fallback to mock data on any error
            use_real_api = False
    
    # Use mock data if not using real API (fallback)
    if not use_real_api:
        flights_data = generate_mock_flights(origin_code, dest_code, departure_date)
        data_source = "Mock Data (Real API did not return results)"
    
    # Check if we have any flights
    if not flights_data:
        return {
            "status": "success",
            "flights": [],
            "route": {
                "origin": {
                    "code": origin_code,
                    "name": origin_info["name"],
                    "city": origin_info["city"],
                    "country": origin_info["country"]
                },
                "destination": {
                    "code": dest_code,
                    "name": dest_info["name"],
                    "city": dest_info["city"],
                    "country": dest_info["country"]
                }
            },
            "departure_date": departure_date,
            "message": f"No flights found between {origin_code} and {dest_code} for {departure_date}.",
            "data_source": data_source
        }
    
    # Build successful response
    return {
        "status": "success",
        "route": {
            "origin": {
                "code": origin_code,
                "name": origin_info["name"],
                "city": origin_info["city"],
                "country": origin_info["country"]
            },
            "destination": {
                "code": dest_code,
                "name": dest_info["name"],
                "city": dest_info["city"],
                "country": dest_info["country"]
            }
        },
        "departure_date": departure_date,
        "flights_found": len(flights_data),
        "flights": flights_data,
        "data_source": data_source
    }


# Example usage for testing
if __name__ == "__main__":
    print("=" * 70)
    print("Flight Search Tool - Test Suite")
    print("=" * 70)
    
    # Check if API key is loaded
    if not AVIATION_STACK_API_KEY:
        print("\n❌ ERROR: AVIATION_STACK_API_KEY not found!")
        print("Please create a .env file in the travel_mcp_server directory with:")
        print("AVIATION_STACK_API_KEY=your_api_key_here")
    else:
        print(f"\n✅ API Key loaded: {AVIATION_STACK_API_KEY[:10]}...{AVIATION_STACK_API_KEY[-5:]}")
    
    print("\n" + "-" * 70)
    print("Test 1: Valid route (JFK to LAX) - Future date")
    print("-" * 70)
    result = search_flights("JFK", "LAX", "2025-12-25")
    
    if result["status"] == "success":
        print(f"✅ Success!")
        print(f"   Route: {result['route']['origin']['city']} → {result['route']['destination']['city']}")
        print(f"   Flights Found: {result['flights_found']}")
        print(f"   Data Source: {result['data_source']}")
        if result['flights']:
            print(f"\n   Sample Flight:")
            flight = result['flights'][0]
            print(f"     {flight['airline']['name']} {flight['flight_number']}")
            print(f"     Departs: {flight['departure']['scheduled_time']}")
            print(f"     Arrives: {flight['arrival']['scheduled_time']}")
            print(f"     Duration: {flight.get('duration_hours', 'N/A')} hours")
            if 'price_usd' in flight:
                print(f"     Price: ${flight['price_usd']}")
    else:
        print(f"❌ Error: {result['error_message']}")
    
    print("\n" + "-" * 70)
    print("Test 2: Invalid airport code")
    print("-" * 70)
    result = search_flights("XYZ", "LAX", "2025-12-25")
    
    if result["status"] == "error":
        print(f"✅ Error handling works correctly")
        print(f"   Error message: {result['error_message']}")
    else:
        print(f"⚠️  Expected error but got success")
    
    print("\n" + "-" * 70)
    print("Test 3: International route (LHR to DXB)")
    print("-" * 70)
    result = search_flights("LHR", "DXB", "2025-06-15")
    
    if result["status"] == "success":
        print(f"✅ Success!")
        print(f"   Route: {result['route']['origin']['city']}, {result['route']['origin']['country']} → {result['route']['destination']['city']}, {result['route']['destination']['country']}")
        print(f"   Flights Found: {result['flights_found']}")
    else:
        print(f"❌ Error: {result['error_message']}")
    
    print("\n" + "=" * 70)
