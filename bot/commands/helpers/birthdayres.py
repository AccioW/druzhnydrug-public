# 3rd party
from telegram import Update
from telegram.ext import ContextTypes

# Built-in
import re

# Custom
from utils import get_user_info, save_user_info, StateManager, c_vars
from ..birthday import birthday_command


async def birthday_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the response for setting a user's birthday.

    This function checks if the user is in the process of setting their birthday, validates the date format,
    and saves it if valid. If the date format is incorrect, it prompts the user to enter it again.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Raises:
        ValueError: If the user input does not match the date format.

    Example:
        >>> await handle_birthday_response(update, context)
    ---
    The function performs the following steps:
    1. Checks if the user is in the correct state to set their birthday.
    2. Validates the date input format (dd.mm.yyyy).
    3. Saves the date to the user's information.
    4. Sends a confirmation message to the user.
    5. Removes the user's state from the state manager.
    6. Calls the birthday command.
    """
    user, chat, mention, user_input = c_vars(update)

    state_manager = StateManager()
    bd_state = await state_manager.get_state("birthday", user.id)

    # Check if bot is awaiting the birthday setting
    if not bd_state or bd_state["action"] != "setting":
        return

    date_pattern = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")
    if not date_pattern.match(user_input):
        prompt = f"Введи дату в формате 'дд.мм.гггг', {mention}..."
        await context.bot.send_message(chat.id, prompt)
        return

    if bd_state["timer"]:
        bd_state["timer"].cancel()

    user_info = get_user_info(user)
    user_info[str(user.id)]["credentials"]["birthday"] = str(user_input)
    save_user_info(user_info)

    prompt = f"Я сохранил твою дату дня рождения: {user_input}"
    await context.bot.send_message(chat.id, prompt)
    await state_manager.remove_state("birthday", user.id)
    await birthday_command(update, context)

    print("Setting ended")
