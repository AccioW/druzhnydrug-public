"""
The utilities(utils) package contains modules for various utility functions used in the bot.

Modules:
- users_info_module: Contains functions to retrieve and save user information.
- gen_equation: Contains a function to generate math equations for the math game.
- dialog_manager: Contains a class to manage dialog interactions.
- task_manager: Contains a class to manage asynchronous tasks.
- state_manager: Contains a class to manage user states.

Usage:
Import specific utilities:
    from utils import get_user_info, generate_equation

Or import all utilities:
    from utils import *
"""

from .data_manager import (
    get_user_info,
    get_all_users_info,
    save_user_info,
    get_and_save,
)
from .gen_equation import generate_equation
from .dialog_manager import DialogManager
from .task_manager import TaskManager
from .state_manager import StateManager
from .timer import TimerConfig, set_timer
from .common_vars import c_vars

from .tasks.percent_resetter import friend_percent_reset
from .tasks.frog_sender import send_frog

__all__ = [
    "get_user_info",
    "get_all_users_info",
    "save_user_info",
    "get_and_save",
    "generate_equation",
    "DialogManager",
    "TaskManager",
    "StateManager",
    "TimerConfig",
    "set_timer",
    "c_vars",
    "friend_percent_reset",
    "send_frog",
]
