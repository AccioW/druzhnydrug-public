# 3rd party
from pytz import timezone

# Built-in
import asyncio
from datetime import datetime

# Custom
from ..data_manager import get_all_users_info, save_user_info

async def friend_percent_reset():
    """
    Perform the daily reset of the 'used_today' flag at midnight CET.

    This task runs indefinitely and resets the 'used_today' flag for all users
    at midnight CET every day.

    Example:
        >>> await task_manager.friend_percent_reset()
    """
    try:
        while True:
            current = datetime.now(timezone("CET"))

            # Perform the reset if it's midnight CET
            if current.hour == 0:
                users_info = get_all_users_info()
                for user_info in users_info.values():
                    user_info["friend"]["used_today"] = False
                save_user_info(users_info)
                print("'used_today' reset for all users")

            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        # Cancel the task if it's cancelled
        pass