# 3rd party
from telegram import Update
from telegram.ext import ContextTypes

# Custom
from utils import StateManager, generate_equation, TimerConfig, set_timer, c_vars


async def math_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /math command.

    This function initiates a math game for the user by generating a mathematical equation and prompting the user to solve it.
    It tracks the user's score and provides feedback on each answer. Additionally, it sets a timer for each question and handles
    the timeout scenario.
    ---
    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the update.

    Example:
        >>> await math_command(update, context)
    ---
    The function performs the following steps:
    1. Checks if the user is already playing the game. If so, it forbids starting a new game.
    2. Generates a new mathematical equation and updates the user's state with the equation and the correct answer.
    3. Sends a prompt to the user with the equation.
    4. Sets a timer for the question and handles the timeout scenario.
    """
    print("Math command triggered")
    user, chat, mention, _ = c_vars(update)
    state_manager = StateManager()
    goal = 20

    math_state = await state_manager.get_state("math", user.id)

    # Check if the user is already playing (has the "answering" flag)
    if math_state and math_state["action"] == "answering":
        # If YES - forbid to call the /math command
        prompt = f"{mention}, ты уже играешь! Сначала ответь на задание!"
        await context.bot.send_message(chat.id, prompt)
        return
    else:
        # If NO - generate a new equation
        num1, num2, operator, result = await generate_equation()
        # Declaring a new dictionary (setting all the defaults)
        await state_manager.set_state(
            "math",
            user.id,
            {
                "action": "answering",
                "score": math_state.get(user.id, {}).get("score", 0),
                "result": result,
                "timer": None,
            },
        )

    # Reload the state to get the updated information
    math_state = await state_manager.get_state("math", user.id)

    # Check if user achieved the max result
    if math_state["score"] == goal:
        math_state["score"] = 0

    # Generate prompt and send
    equation = f"Сколько будет {num1} {operator} {num2}?"
    prompt = (
        f"Проверим твои знания математики, {mention}.\n\n{equation}"
        if math_state["score"] == 0
        else f"Правильно, {mention}!\nТекущий счет: {math_state['score']}.\nСледующий вопрос:\n\n{equation}"
    )
    await context.bot.send_message(chat.id, prompt)

    # Setting the timer (using TimerConfig)
    config = TimerConfig(
        user_id=user.id,
        state_name="math",
        context=context,
        chat_id=chat.id,
        mention=mention,
        prompt=(
            f"Время истекло, {mention}.⌛\n"
            f"\nТвой финальный счёт: {math_state['score']} из {goal}"
        ),
        timeout=10,
        callback_data="/math",
        is_active=lambda state: state["action"] == "answering",
    )
    await set_timer(config)
