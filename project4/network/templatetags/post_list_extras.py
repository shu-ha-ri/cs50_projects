from django import template
from ..models import Post

register = template.Library()

def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()
