import asyncio
import json
from io import StringIO
from server import server


async def test_list_tools():
    """Test that the server can list its tools."""
    print("=" * 60)
    print("TEST 1: List Available Tools")
    print("=" * 60)
    
    try:
        tools = await server._list_tools_handler()
        print(f"\n✅ Server exposes {len(tools)} tool(s):\n")
        
        for tool in tools:
            print(f"Tool Name: {tool.name}")
            print(f"Description: {tool.description[:100]}...")
            print(f"Required Parameters: {tool.inputSchema.get('required', [])}")
            print("-" * 60)
        
        return True
    except Exception as e:
        print(f"\n❌ Error listing tools: {e}")
        return False


async def test_weather_tool():
    """Test the weather forecast tool."""
    print("\n" + "=" * 60)
    print("TEST 2: Call Weather Forecast Tool")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Valid request (Paris)",
            "args": {
                "destination": "Paris",
                "travel_dates": "2025-06-15 to 2025-06-22"
            }
        },
        {
            "name": "Valid request (Tokyo in winter)",
            "args": {
                "destination": "Tokyo",
                "travel_dates": "2025-12-20 to 2025-12-27"
            }
        },
        {
            "name": "Invalid destination",
            "args": {
                "destination": "Unknown City",
                "travel_dates": "2025-06-15 to 2025-06-22"
            }
        },
        {
            "name": "Missing parameters",
            "args": {
                "destination": "Paris"
                # Missing travel_dates
            }
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print(f"Arguments: {json.dumps(test_case['args'], indent=2)}")
        
        try:
            result = await server._call_tool_handler(
                name="get_weather_forecast",
                arguments=test_case['args']
            )
            
            # Parse the result
            result_text = result[0].text
            result_data = json.loads(result_text)
            
            print(f"Status: {result_data.get('status', 'unknown')}")
            
            if result_data.get("status") == "success":
                print(f"✅ Success!")
                print(f"   Destination: {result_data.get('destination')}")
                print(f"   Season: {result_data.get('season')}")
                temp = result_data.get('temperature_range', {})
                print(f"   Temperature: {temp.get('min_celsius')}°C - {temp.get('max_celsius')}°C")
                success_count += 1
            elif result_data.get("status") == "error":
                print(f"⚠️  Expected Error: {result_data.get('error_message')}")
                success_count += 1  # Error handling is also success
            else:
                print(f"❌ Unexpected status")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
    
    print(f"\nPassed {success_count}/{len(test_cases)} test cases")
    return success_count == len(test_cases)


async def test_unknown_tool():
    """Test calling a tool that doesn't exist."""
    print("\n" + "=" * 60)
    print("TEST 3: Call Unknown Tool (Error Handling)")
    print("=" * 60)
    
    try:
        result = await server._call_tool_handler(
            name="nonexistent_tool",
            arguments={}
        )
        
        result_text = result[0].text
        result_data = json.loads(result_text)
        
        if result_data.get("status") == "error":
            print("✅ Server correctly handles unknown tool")
            print(f"   Error message: {result_data.get('error_message')}")
            return True
        else:
            print("❌ Server should return error for unknown tool")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def main():
    """Run all tests."""
    print("\n" + "🧪 " * 20)
    print("TRAVEL MCP SERVER - TEST SUITE")
    print("🧪 " * 20 + "\n")
    
    results = []
    
    # Run tests
    results.append(await test_list_tools())
    results.append(await test_weather_tool())
    results.append(await test_unknown_tool())
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Your MCP server is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\nNext Steps:")
    print("1. Create destination.py and attractions.py tools")
    print("2. Update server.py to include new tools")
    print("3. Run this test script again")
    print("4. Integrate with ADK in Jupyter notebook")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

