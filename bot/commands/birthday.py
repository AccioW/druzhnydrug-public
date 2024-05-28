# 3rd party
from telegram import Update
from telegram.ext import ContextTypes

# Built-in
from datetime import datetime

# Custom-made
from utils import get_user_info, StateManager, TimerConfig, set_timer, c_vars


async def birthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /birthday command.

    This function retrieves the user's birthday information, calculates the number of days until the next birthday,
    and sends a message with the remaining days. If the birthday is not set, it prompts the user to enter it.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await birthday_command(update, context)
    ---
    The function performs the following steps:
    1. Retrieves the user's information.
    2. Checks if the user's birthday is set.
    3. Calculates the number of days until the next birthday.
    4. Sends a message with the remaining days until the birthday.
    5. If the birthday is not set, prompts the user to enter it.
    """
    print("Birthday command triggered")
    user, chat, mention, _ = c_vars(update)

    user_info = get_user_info(user)
    state_manager = StateManager()

    # Check if the user is already setting their birthday
    bd_state = await state_manager.get_state("birthday", user.id)

    if bd_state and bd_state["action"]["setting"]:
        prompt = f"{mention}, сначала закончи менять свою дату рождения!"
        await context.bot.send_message(chat.id, prompt)
        return

    birthday = user_info[str(user.id)]["credentials"]["birthday"]
    if birthday:
        if isinstance(birthday, str):
            birthday = datetime.strptime(birthday, "%d.%m.%Y")

        today = datetime.today()
        next_bd = birthday.replace(year=today.year)
        if next_bd <= today:
            next_bd = next_bd.replace(year=today.year + 1)

        days_until_birthday = (next_bd - today).days
        days_word = (
            "дней"
            if days_until_birthday % 10 in {5, 6, 7, 8, 9, 0}
            else "дня" if days_until_birthday % 10 in {2, 3, 4} else "день"
        )

        if days_until_birthday in [0, 364]:
            prompt = f"С днем рождения, {mention}! 🥳🎂"
        else:
            prompt = f"{mention}, до твоего дня рождения осталось {days_until_birthday} {days_word}! 🎉"
        await context.bot.send_message(chat.id, prompt)
    else:
        prompt = f"{mention}, твоя дата дня рождения не установлена. Пожалуйста, введи ее в формате 'дд.мм.гггг', и я сохраню ее 🙂"
        await state_manager.set_state("birthday", user.id, {"action": "setting"})
        await context.bot.send_message(chat.id, prompt)

        # Setting the timer (using TimerConfig)
        config = TimerConfig(
            user_id=user.id,
            state_name="birthday",
            context=context,
            chat_id=chat.id,
            mention=mention,
            prompt=f"{mention}, установка дня рождения не закончена. Время истекло.",
            timeout=30,
            callback_data="/birthday",
            is_active=lambda state: state["action"] == "setting",
        )
        await set_timer(config)
