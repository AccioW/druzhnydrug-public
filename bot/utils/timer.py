from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from dataclasses import dataclass
from typing import Callable
import asyncio

from utils import StateManager


@dataclass
class TimerConfig:
    """
    Configuration for setting a timer for a user.

    Attributes:
        - user_id (int): The ID of the user for whom the timer is being set.
        - state_name (str): The name of the state associated with the timer.
        - context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the timer.
        - chat_id (int): The ID of the chat where the timer prompt will be sent.
        - mention (str): The mention of the user in the prompt message.
        - prompt (str): The prompt message to be sent when the timer expires.
        - timeout (int): The duration of the timer in seconds.
        - callback_data (str): The data to be sent back when the user interacts with the prompt.
        - is_active (Callable[[dict], bool]): A function to determine if the timer is still active based on
            the current state.
    """
    user_id: int
    state_name: str
    context: ContextTypes.DEFAULT_TYPE
    chat_id: int
    mention: str
    prompt: str
    timeout: int
    callback_data: str
    is_active: Callable[[dict], bool]


async def set_timer(config: TimerConfig):
    """
    Sets a timer for a specific user with the provided configuration.

    This function sets a timer for a user based on the provided configuration. When the timer expires,
    it sends a prompt message to the user with an option to retry.

    Args:
        config (TimerConfig): Configuration for the timer, including user ID, state name, context, chat ID,
            mention, prompt message, timeout duration, callback data, and a function to determine if the timer
            should still be active.

    Raises:
        This function doesn't raise any exceptions.

    Example:
        >>> timer_config = TimerConfig(
        >>>     user_id=123,
        >>>     state_name="timer_state",
        >>>     context=context,
        >>>     chat_id=456,
        >>>     mention="@username",
        >>>     prompt="Your time is up! Would you like to try again?",
        >>>     timeout=60,
        >>>     callback_data="retry",
        >>>     is_active=lambda state: state.get('is_active', False)
        >>> )
        >>> await set_timer(timer_config)
    """
    state_manager = StateManager()

    async def timeout_handler() -> None:
        await asyncio.sleep(config.timeout)

        state = await state_manager.get_state(config.state_name, config.user_id)
        if state and config.is_active(state):
            retry_text = "Попробовать еще раз..."
            keyboard = [
                [InlineKeyboardButton(retry_text, callback_data=config.callback_data)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await config.context.bot.send_message(
                chat_id=config.chat_id, text=config.prompt, reply_markup=reply_markup
            )
            await state_manager.remove_state(config.state_name, config.user_id)

    await state_manager.set_state(
        config.state_name,
        config.user_id,
        {"timer": asyncio.create_task(timeout_handler())},
    )
