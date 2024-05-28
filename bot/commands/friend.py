# 3rd party
from telegram import Update
from telegram.ext import ContextTypes

# Built-in
import random

# Custom
from utils import get_user_info, save_user_info, c_vars


async def friend_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /friend command.

    This function calculates and sends the user's friendship level for the current day. If the user has already used the command
    on the same day, it notifies them about the cooldown period. Otherwise, it generates a random friendship level.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await friend_command(update, context)
    ---
    The function performs the following steps:
    1. Checks if the user has already used the command today.
    2. If the user has used the command today, notifies them about the cooldown.
    3. If the user has not used the command today, generates a random friendship level.
    4. Sends a message with the friendship level.
    5. Updates the user's information to mark the command as used.
    """
    user, chat, mention, _ = c_vars(update)

    # Check if the user has used the command recently
    user_info = get_user_info(user)
    used_today = user_info[str(user.id)]["friend"]["used_today"]

    if used_today:
        # User HAS used the command recently - notify about the cooldown
        print("Friend command triggered - NOT generating")
        stored_percentage = user_info[str(user.id)]["friend"]["percentage"]
        prompt = f"Прости, {mention}, ты уже узнал свой уровень дружбы на сегодня: {stored_percentage}%"
        await context.bot.send_message(chat.id, prompt)
    else:
        # User CAN use the command - proceed with generating
        print("Friend command triggered - generating")
        random_percentage = random.randint(0, 100)
        prompt = f"Уровень дружбы {mention} сегодня: {random_percentage}% ❤"
        await context.bot.send_message(chat.id, prompt)

        user_info[str(user.id)]["friend"]["used_today"] = True
        user_info[str(user.id)]["friend"]["percentage"] = random_percentage
        save_user_info(user_info)
