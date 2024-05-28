import random


async def generate_equation() -> tuple:
    """
    Generate a random arithmetic equation involving addition or subtraction.

    This function generates two random integers between -99 and 99, and randomly chooses
    an operator (either "+" or "-") to create an equation. If the second number is negative,
    the operator is adjusted accordingly to ensure correct arithmetic operations.

    Returns:
        tuple: A tuple containing four elements:
        - num1 (int): The first operand.
        - num2 (int): The second operand (always positive).
        - operator (str): The arithmetic operator ("+" or "-").
        - result (int): The result of the equation (num1 operator num2).
    
    Example:
        >>> await generate_equation()
        (23, 45, '+', 68)
    """
    num1 = random.randint(-99, 99)
    num2 = random.randint(-99, 99)
    operator = random.choice(["+", "-"])

    if num2 < 0:
        operator = "-" if operator == "+" else "+"
        num2 *= -1

    result = num1 + num2 if operator == "+" else num1 - num2

    return num1, num2, operator, result