#!/usr/bin/env python3
"""
Main entry point for the Simple Calculator application.
"""

from calculator import Calculator


def main():
    """Main function to run the calculator application."""
    calc = Calculator()
    
    print("=" * 50)
    print("Welcome to Simple Calculator!")
    print("=" * 50)
    
    try:
        # Get user input
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Perform addition
        result = calc.add(num1, num2)
        
        # Display result
        print(f"\nResult: {num1} + {num2} = {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

