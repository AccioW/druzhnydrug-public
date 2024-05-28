# 3rd party
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Custom
from utils import get_and_save, c_vars


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.

    This function sends a help message with inline keyboard options to the user, allowing them to choose between different
    commands and functionalities.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await help_command(update, context)
    ---
    The function performs the following steps:
    1. Retrieves and saves user information.
    2. Constructs an inline keyboard with options for capabilities, future plans, about the bot, and starting message.
    3. Sends the help message with the inline keyboard options to the user.
    """
    print("Help command triggered")
    user, chat, _, _ = c_vars(update)
    get_and_save(user)

    caps_text = "🔍 Возможности"
    future_text = "🚀 Планы"
    about_text = "👋 Что я и зачем я"
    start_text = "🚀 На начало"

    keyboard = [
        [
            InlineKeyboardButton(caps_text, callback_data="/capabilities"),
            InlineKeyboardButton(future_text, callback_data="/future"),
        ],
        [
            InlineKeyboardButton(about_text, callback_data="/about_me"),
            InlineKeyboardButton(start_text, callback_data="/start_message"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    prompt = "Выбери одну из опций:"
    await context.bot.send_message(
        chat_id=chat.id, text=prompt, reply_markup=reply_markup
    )
