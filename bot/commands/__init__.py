"""
The commands package contains modules for handling various commands in the Telegram bot.

Modules:
- start: Contains functions to handle the /start command.
- help: Contains functions to handle the /help command.
- friend: Contains functions to handle the /friend command.
- birthday: Contains functions to handle the /birthday command.
- math: Contains functions to handle the /math command.
---
- birthday_response: Contains functions to handle the response to the /birthday command
- math_response: Contains functions to handle the response to the /math command
---
Usage:
Import specific commands:
    from commands import start_command, help_command

Or import all commands:
    from commands import *
"""

from .start import start_command
from .help import help_command
from .friend import friend_command
from .birthday import birthday_command
from .math import math_command

from .helpers.birthdayres import birthday_response
from .helpers.mathres import math_response

__all__ = [
    "start_command",
    "help_command",
    "friend_command",
    "birthday_command",
    "math_command",
]
