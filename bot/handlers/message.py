# 3rd party
from telegram import Update
from telegram.ext import ContextTypes

# Custom
from commands import birthday_response, math_response
from utils import DialogManager, StateManager

bot_id: int = 7137203126
bot_username: str = "@DruzhnyDrugBot"


async def handle_new_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handle new incoming messages.

    This function determines the type of incoming message and delegates the handling to appropriate functions
    based on the user's state and message type.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await handle_new_message(update, context)
    ---
    The function performs the following steps:
    1. Identifies the type of message (group, supergroup, or private).
    2. Checks if the user is in the process of answering a math question or setting their birthday.
    3. Passes the message to the appropriate handler:
        1. If the user is answering a math question, delegates to handle_math_response().
        2. If the user is setting their birthday, delegates to handle_birthday_response().
        3. Otherwise, passes the message to DialogManager for processing.
    4. Prints debug information.
    """
    try:
        message_type: str = update.message.chat.type
        user_id: int = update.message.from_user.id
        text: str = update.message.text

        print(f'User: {user_id} in {message_type}: "{text}"')

        state_manager = StateManager()
        dm = DialogManager()

        math_state = await state_manager.get_math_state()
        bd_state = await state_manager.get_bd_state()

        # math-related responses
        if user_id in math_state:
            await math_response(update, context)
            return

        # Birthday-related responses
        if user_id in bd_state:
            await birthday_response(update, context)
            return

        # Normal responses
        if message_type in {"group", "supergroup"}:
            if (
                update.message.reply_to_message
                and update.message.reply_to_message.from_user.id == bot_id
            ):
                prompt = dm.handle_response(text.strip(), user_id)
            elif bot_username in text:
                new_text = text.replace(bot_username, "").strip()
                prompt = dm.handle_response(new_text, user_id)
            else:
                return
        else:
            prompt: str = dm.handle_response(text, user_id)

        print(f'DruzhnyDrug: "{prompt}"')
        await update.message.reply_text(prompt)
    except Exception as e:
        print(f"Error handling message: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming user messages.

    This function distinguishes between regular incoming messages and edited messages,
    and calls the corresponding handling functions.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.

    Example:
        >>> await handle_message(update, context)
    ---
    The function performs the following steps:
    1. Checks if the message has been edited.
    2. If the message is edited, calls handle_edited_message().
    3. If the message is not edited, calls handle_new_message().
    """
    if update.edited_message:
        await handle_edited_message(update)
    else:
        await handle_new_message(update, context)


async def handle_edited_message(update: Update) -> None:
    """
    Handle edited messages.

    This function handles edited messages and prints debug information.
    
    Args:
        update (telegram.Update): The incoming update from Telegram.

    Example:
        >>> await handle_edited_message(update)
    ---
    The function performs the following steps:
    1. Retrieves information about the edited message.
    2. Prints debug information about the edit.
    """
    edited_message = update.edited_message
    user_id = edited_message.from_user.id
    chat_id = edited_message.chat_id
    text = edited_message.text

    print(f'Message edited by user ID {user_id} in chat ID {chat_id}: "{text}"')
