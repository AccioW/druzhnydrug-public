# 3rd party
from telegram import Update
from telegram.ext import ContextTypes


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors that occur during message processing.

    This function is responsible for handling errors that occur during the processing of Telegram messages.

    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await handle_error(update, context)
    ---
    The function simply prints information about the error that occurred, including the update that triggered the error
    and the type of error that occurred.
    """
    print(f"Update {update} caused error {context.error}")
