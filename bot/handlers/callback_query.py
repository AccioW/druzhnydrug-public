# 3rd party
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Custom
from commands import *


async def handle_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handle callback queries from inline keyboards.

    This function processes callback queries triggered by inline keyboards (telegram buttons),
    and performs different actions based on the received data.

    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Raises:
        ValueError: If the received data does not match any expected callback query.

    Example:
        >>> await handle_callback_query(update, context)

    The function performs the following actions based on the received data:
    - If the data is "/capabilities", it sends a message listing the bot's capabilities.
    - If the data is "/future", it sends a message listing the upcoming updates.
    - If the data is "/about_me", it sends a message explaining the purpose of the bot.
    ---
    - If the data is "/start_message", it triggers the start command.
    - If the data is "/friend", it triggers the friend command.
    - If the data is "/birthday", it triggers the birthday command.
    - If the data is "/math", it triggers the math command.
    - If the data is "/help", it triggers the help command.
    """
    query = update.callback_query
    data = query.data
    
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

    if data == "/capabilities":
        prompt = (
            "🔍 Мои возможности:\n"
            "\n/start - Моё приветствие"
            "\n/friend - Узнать уровень твоей дружбы на сегодня"
            "\n/birthday - Узнать, сколько осталось до твоего дня рождения"
            "\n/math - Проверить твои знания математики\n/help - Рассказать о себе"
        )
        await query.edit_message_text(text=prompt, reply_markup=reply_markup)
    elif data == "/future":
        prompt = (
            "🚀 Будущие обновления:\n\n- Рандомизатор игры на сегодня с последующим опросом"
            "\n- Усовершенствование диалогов (возможно подключение LLM)"
            "\n- Автоматическое отправление жаб в Дружбу каждую среду"
            "\n- Усовершенствование команды /birthday с добавлением автоматического поздравления в день рождения"
            "\n- Малые правки остальных команд"
        )
        await query.edit_message_text(text=prompt, reply_markup=reply_markup)
    elif data == "/about_me":
        prompt = (
            "👋 Что я и зачем я:\n\nЯ дружный Друг. Меня создал Влад с нуля на питоне вместо того, "
            "что бы заниматься более полезными делами. Влад не умеет программировать красиво, поэтому его код лучше не видеть."
            "\n\nСоздан я по большей части для небольшого развлечения Дружбы. "
            "За основные концепты были взяты рандомизатор % и небольшая математическая игра от Евгосика"
        )
        await query.edit_message_text(text=prompt, reply_markup=reply_markup)
    elif data == "/start_message":
        message_id = query.message.message_id
        chat_id = query.message.chat.id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await start_command(update, context)
    elif data == "/friend":
        await friend_command(update, context)
    elif data == "/birthday":
        await birthday_command(update, context)
    elif data == "/math":
        await math_command(update, context)
    elif data == "/help":
        await help_command(update, context)
