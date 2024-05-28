# 3rd party
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


# Custom
from utils import get_user_info, save_user_info, StateManager, c_vars
from ..math import math_command


async def math_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle math-related responses.

    This function processes responses to math-related questions asked by the bot. It checks if the user's response is correct,
    updates the user's score accordingly, and provides feedback if the response is incorrect.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Raises:
        ValueError: If the user's response cannot be converted to an integer.

    Example:
        >>> await handle_math_response(update, context)
    ---
    The function performs the following steps:
    1. Checks if the user is in the correct state to answer a math question.
    2. Validates the user's response as an integer.
    3. Compares the user's response with the correct answer.
    4. Updates the user's score if the response is correct.
    5. Notifies the user of the correct answer and provides an option to retry if the response is incorrect.
    6. Saves user information and removes their state from the state manager if needed.
    """
    user, chat, mention, user_input = c_vars(update)
    user_info = get_user_info(user)
    goal = 20

    state_manager = StateManager()
    math_state = await state_manager.get_state("math", user.id)

    # Check if bot is awaiting response
    if math_state or math_state["action"] != "answering":
        return

    try:
        # Convert user's answer to an integer
        user_input = int(user_input)
    except ValueError:
        # If answer is NOT an integer, send a warning message
        prompt = "Введи целое число, пожалуйста."
        await context.bot.send_message(chat.id, prompt)
        return

    # Get the correct answer to the equation
    result = math_state["result"]

    if user_input == result:
        # Correct answer
        math_state["score"] += 1
        math_state["action"] = "done"

        # Update the state with the current score from math_game
        # math_state = await state_manager.get_state("math", user.id)

        # IF USER SUCCEDED SET HIGH SCORE
        if math_state["score"] > user_info[str(user.id)]["math_score"]:
            if math_state["score"] <= goal:
                user_info[str(user.id)]["math_score"] = math_state["score"]
                save_user_info(user_info)

        # IF REACHED THE GOAL
        if math_state["score"] >= goal:
            prompt = f"Поздравляю, {mention}! Ты достиг цели: {goal}! 🏅"
            await context.bot.send_message(chat.id, prompt)
            await state_manager.remove_state("math", user.id)
            return

        # Update state and proceed to the next question
        await state_manager.set_state("math", user.id, math_state)

        # Cancel the existing timer task and create a new one
        if math_state["timer"]:
            math_state["timer"].cancel()
        await math_command(update, context)
    else:
        # Incorrect answer
        retry_text = "Попробовать еще раз..."
        keyboard = [
            [InlineKeyboardButton(retry_text, callback_data="/math")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        prompt = (
            f"Ответ неверен, {mention} 🥺\n"
            f"Правильный ответ: {result}\n"
            f"\nТвой финальный счёт: {math_state['score']} из {goal}"
        )

        # Cancel the existing timer task
        if math_state["timer"]:
            math_state["timer"].cancel()

        await context.bot.send_message(
            chat_id=chat.id,
            text=prompt,
            reply_markup=reply_markup,
        )

        # Save user information and delete their data
        save_user_info(user_info)
        await state_manager.remove_state("math", user.id)
