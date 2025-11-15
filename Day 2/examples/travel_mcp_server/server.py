"""
Travel MCP Server

Provides travel-related tools via Model Context Protocol (MCP).
"""

import json
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

try:
    from tools.weather import get_weather_forecast
    WEATHER_TOOL_AVAILABLE = True
except ImportError as e:
    WEATHER_TOOL_AVAILABLE = False
    print(f"⚠️  Warning: Could not import weather tool: {e}")

try:
    from tools.flight_details import search_flights
    FLIGHT_TOOL_AVAILABLE = True
except ImportError as e:
    FLIGHT_TOOL_AVAILABLE = False
    print(f"⚠️  Warning: Could not import flight tool: {e}")

server = Server("travel-mcp-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """
    List all available tools.
    Only includes tools that were successfully imported.
    """
    tools = []
    
    # Add weather tool if available
    if WEATHER_TOOL_AVAILABLE:
        tools.append(
            types.Tool(
                name="get_weather_forecast",
                description=(
                    "Get weather forecast for a travel destination to help plan trips and packing. "
                    "Provides temperature ranges, weather conditions, and packing suggestions based on "
                    "the destination and travel dates. Use this tool when users ask about weather, "
                    "what to pack, or climate information for their trip."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": (
                                "City name for the destination (e.g., 'Paris', 'Tokyo', 'New York'). "
                                "Can include country for clarity (e.g., 'Paris, France')."
                            )
                        },
                        "travel_dates": {
                            "type": "string",
                            "description": (
                                "Travel date range in format 'YYYY-MM-DD to YYYY-MM-DD' (e.g., '2025-06-15 to 2025-06-22'). "
                                "Can also be a single date in format 'YYYY-MM-DD'."
                            )
                        }
                    },
                    "required": ["destination", "travel_dates"]
                }
            )
        )
    
    # Add flight search tool if available
    if FLIGHT_TOOL_AVAILABLE:
        tools.append(
            types.Tool(
                name="search_flights",
                description=(
                    "Search for flights between two airports for travel planning. "
                    "Provides flight options with airlines, times, duration, and pricing. "
                    "Use this tool when users ask about flights, flight prices, or how to get to a destination. "
                    "Returns real-time data when available, or mock data for future dates."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": (
                                "Origin airport IATA code (3 letters, e.g., 'JFK', 'LAX', 'LHR', 'CDG'). "
                                "Major airports: JFK (New York), LAX (Los Angeles), LHR (London), CDG (Paris), "
                                "NRT/HND (Tokyo), DEL (Delhi), BOM (Mumbai), DXB (Dubai), SIN (Singapore)."
                            )
                        },
                        "destination": {
                            "type": "string",
                            "description": (
                                "Destination airport IATA code (3 letters, e.g., 'LAX', 'LHR', 'NRT'). "
                                "Use the same format as origin."
                            )
                        },
                        "departure_date": {
                            "type": "string",
                            "description": (
                                "Departure date in YYYY-MM-DD format (e.g., '2025-06-15'). "
                                "Must be current or future date."
                            )
                        }
                    },
                    "required": ["origin", "destination", "departure_date"]
                }
            )
        )
    
    # TODO: Add more tools as you create them
    # if DESTINATION_TOOL_AVAILABLE:
    #     tools.append(types.Tool(...))
    
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """
    Execute a tool call with comprehensive error handling.
    
    Args:
        name: The name of the tool to call
        arguments: Dictionary of parameters for the tool
    
    Returns:
        List of TextContent items with the result or error message
    """
    
    # ============================================================================
    # WEATHER FORECAST TOOL
    # ============================================================================
    if name == "get_weather_forecast":
        # Check if tool is available
        if not WEATHER_TOOL_AVAILABLE:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": "Weather forecast tool is not available. Please check server configuration."
                    }, indent=2)
                )
            ]
        
        # Validate required parameters
        destination = arguments.get("destination")
        travel_dates = arguments.get("travel_dates")
        
        if not destination or not travel_dates:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": "Missing required parameters. Please provide both 'destination' and 'travel_dates'."
                    }, indent=2)
                )
            ]
        
        # Call the tool function with error handling
        try:
            result = get_weather_forecast(destination, travel_dates)
            
            # Verify result is JSON-serializable
            try:
                result_json = json.dumps(result, indent=2)
            except (TypeError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "error",
                            "error_message": f"Tool returned non-serializable data: {str(e)}"
                        }, indent=2)
                    )
                ]
            
            return [
                types.TextContent(
                    type="text",
                    text=result_json
                )
            ]
            
        except Exception as e:
            # Catch any unexpected errors from the tool
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": f"Error executing weather forecast tool: {str(e)}",
                        "error_type": type(e).__name__
                    }, indent=2)
                )
            ]
    
    # ============================================================================
    # FLIGHT SEARCH TOOL
    # ============================================================================
    elif name == "search_flights":
        # Check if tool is available
        if not FLIGHT_TOOL_AVAILABLE:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": "Flight search tool is not available. Please check server configuration."
                    }, indent=2)
                )
            ]
        
        # Validate required parameters
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        departure_date = arguments.get("departure_date")
        
        if not origin or not destination or not departure_date:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": "Missing required parameters. Please provide 'origin', 'destination', and 'departure_date'."
                    }, indent=2)
                )
            ]
        
        # Call the tool function with error handling
        try:
            result = search_flights(origin, destination, departure_date)
            
            # Verify result is JSON-serializable
            try:
                result_json = json.dumps(result, indent=2)
            except (TypeError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "error",
                            "error_message": f"Tool returned non-serializable data: {str(e)}"
                        }, indent=2)
                    )
                ]
            
            return [
                types.TextContent(
                    type="text",
                    text=result_json
                )
            ]
            
        except Exception as e:
            # Catch any unexpected errors from the tool
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_message": f"Error executing flight search tool: {str(e)}",
                        "error_type": type(e).__name__
                    }, indent=2)
                )
            ]
    
    # ============================================================================
    # TODO: ADD MORE TOOLS HERE
    # ============================================================================
    # elif name == "get_destination_info":
    #     if not DESTINATION_TOOL_AVAILABLE:
    #         return [types.TextContent(...)]
    #     
    #     city = arguments.get("city")
    #     if not city:
    #         return [types.TextContent(...)]
    #     
    #     try:
    #         result = get_destination_info(city)
    #         return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    #     except Exception as e:
    #         return [types.TextContent(...)]
    
    # ============================================================================
    # UNKNOWN TOOL ERROR
    # ============================================================================
    else:
        return [
            types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "error_message": f"Unknown tool: '{name}'. Please check the tool name and request an updated list of available tools."
                }, indent=2)
            )
        ]


async def main():
    """
    Main entry point for the MCP server.
    
    Runs the server using stdio transport for communication with MCP clients.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    # Run the server
    asyncio.run(main())

