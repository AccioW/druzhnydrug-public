# 3rd party
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Custom
from utils import get_and_save, c_vars


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.

    This function provides the user with options to interact with the bot, including checking the current level of friendship,
    checking how many days are left until the user's birthday, initiating a math game, and requesting help.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await start_command(update, context)
    ---
    The function performs the following steps:
    1. Retrieves user information and saves it.
    2. Constructs a keyboard with options for the user to choose from.
    3. Sends a welcome message to the user with the available options.
    """
    print("Start command triggered")
    user, chat, _, _ = c_vars(update)
    get_and_save(user)

    friend_text = "🎲 Сегодняшний уровень дружбы"
    birthday_text = "🎉 Через сколько дней у меня ДР"
    math_text = "🧮 Я математик!!!"
    help_text = "🆘 Помощь"

    keyboard = [
        [InlineKeyboardButton(friend_text, callback_data="/friend")],
        [InlineKeyboardButton(birthday_text, callback_data="/birthday")],
        [
            InlineKeyboardButton(math_text, callback_data="/math"),
            InlineKeyboardButton(help_text, callback_data="/help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    prompt = "Привет! Я твой дружный друг! Спасибо, что общаешься со мной. Чем хочешь заняться? 🙂"
    await context.bot.send_message(
        chat_id=chat.id, text=prompt, reply_markup=reply_markup
    )
