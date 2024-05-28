"""
The handlers package contains modules for handling various types of updates from the Telegram bot.

Modules:
- callback_query: Contains functions to handle callback queries from inline keyboards.
- message: Contains functions to handle various types of messages, including new messages and edited messages.
- math_response: Contains functions to handle math-related responses.
- birthday_response: Contains functions to handle responses related to setting a user's birthday.
- error: Contains functions to handle errors.
`
Usage:
Import specific handlers:
    from handlers import handle_callback_query, handle_message

Or import all handlers:
    from handlers import *
"""

from .callback_query import handle_callback_query
from .message import handle_message, handle_new_message, handle_edited_message
from .error import handle_error

__all__ = [
    "handle_callback_query",
    "handle_message",
    "handle_new_message",
    "handle_edited_message",
    "handle_error",
]
