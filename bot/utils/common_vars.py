from telegram import Update, User, Chat

from typing import Tuple, Optional


def c_vars(update: Update) -> Tuple[User, Chat, Optional[str], Optional[str]]:
    """
    Extract common variables from the Telegram Update object.

    This function retrieves the effective user, chat, mention string (if username exists),
    and user input text from the provided Update object. The function returns a tuple
    containing these values, with mention and user_input being optional.

    Args:
        update (telegram.Update): The incoming update from Telegram.

    Returns:
        Tuple[telegram.User, telegram.Chat, Optional[str], Optional[str]]: 
        A tuple containing:
        - User: The effective user associated with the update.
        - Chat: The effective chat associated with the update.
        - Optional[str]: The mention string (formatted as @username) if the user has a username, otherwise None.
        - Optional[str]: The stripped text of the user's message if it exists, otherwise None.

    Example:
        >>> user, chat, mention, user_input = c_vars(update)
    """
    user = update.effective_user
    chat = update.effective_chat
    mention = f"@{user.username}" if user.username else None
    user_input = update.message.text.strip() if update.message else None
    return user, chat, mention, user_input
