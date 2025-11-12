"""
Utility functions for the task management system.
"""

from datetime import datetime
from typing import Optional


def validate_date(date_string: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD).
    
    Args:
        date_string: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def format_date(date_string: Optional[str]) -> str:
    """
    Format date string for display.
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        
    Returns:
        Formatted date string or "N/A"
    """
    if not date_string:
        return "N/A"
    
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return date_string


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def parse_priority(priority_string: str) -> Optional[str]:
    """
    Parse and validate priority string.
    
    Args:
        priority_string: Priority string (low, medium, high)
        
    Returns:
        Valid priority string or None
    """
    valid_priorities = ["low", "medium", "high"]
    priority_lower = priority_string.lower()
    if priority_lower in valid_priorities:
        return priority_lower
    return None

