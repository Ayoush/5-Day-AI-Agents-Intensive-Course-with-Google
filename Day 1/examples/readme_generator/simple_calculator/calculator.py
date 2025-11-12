"""
Calculator module providing basic arithmetic operations.
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """
        Subtract second number from first number.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Difference of a and b
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """
        Divide first number by second number.
        
        Args:
            a: First number (dividend)
            b: Second number (divisor)
            
        Returns:
            Quotient of a and b
            
        Raises:
            ValueError: If divisor is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def get_history(self) -> list:
        """
        Get calculation history.
        
        Returns:
            List of calculation strings
        """
        return self.history.copy()
    
    def clear_history(self):
        """Clear the calculation history."""
        self.history.clear()

