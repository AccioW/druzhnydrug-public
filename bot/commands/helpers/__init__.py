"""
The helpers package contains modules for handling various responses in the Telegram bot.

Modules:
- birthday_response: Contains functions to handle the response to the /birthday command.
- math_response: Contains functions to handle the response to the /math command.
---
Usage:
Import specific responses:
    from commands.helpers import handle_birthday_response, handle_math_response

Or import all responses:
    from commands.helpers import *
"""

from .birthdayres import birthday_response
from .mathres import math_response

__all__ = [
    "birthday_response",
    "math_response",
]
