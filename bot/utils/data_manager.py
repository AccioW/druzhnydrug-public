from typing import Dict, Any
import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_INFO_FILE = os.path.join(CURRENT_DIR, "..", "users_info.json")


def get_user_info(user) -> Dict[str, Any]:
    """
    Retrieve user information from the JSON file or use default values if not found.

    Args:
        user: The Telegram user object.

    Returns:
        dict: A dictionary containing user information with the following keys:
        - username (str): The username of the user.
        - first_name (str): The first name of the user.
        - credentials (dict): A dictionary with user credentials, including:
            - birthday (str): The user's birthday.
        - math_score (int): The math score of the user.
        - friend (dict): A dictionary containing:
            - used_today (bool): Indicates if the friend feature has been used today.
            - percentage (int): The percentage of friendship points used.

    Raises:
        IOError: If there is an error reading the file.
        json.JSONDecodeError: If the file cannot be parsed as JSON.

    Example:
        >>> user_info = get_user_info(user)
    """
    user_id = str(user.id)

    try:
        with open(USER_INFO_FILE, "r") as file:
            file_content = file.read()
            if file_content.strip():
                user_data = json.loads(file_content)
            else:
                user_data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}

    user_birthday = user_data.get(user_id, {}).get("credentials", {}).get("birthday")
    math_score = user_data.get(user_id, {}).get("math_score", 0)

    friend_info = user_data.get(user_id, {}).get("friend", {})
    used_today = friend_info.get("used_today", False)
    percentage = friend_info.get("percentage", 0)

    default_user_info = {
        "username": user.username,
        "first_name": user.first_name,
        "credentials": {"birthday": user_birthday},
        "math_score": math_score,
        "friend": {"used_today": used_today, "percentage": percentage},
    }
    user_info = {user_id: default_user_info}

    return user_info


def get_all_users_info() -> Dict[str, Dict[str, Any]]:
    """
    Retrieve user information for all users from the JSON file.

    Returns:
        dict: A dictionary containing user information with the following keys:
        - username (str): The username of the user.
        - first_name (str): The first name of the user.
        - credentials (dict): A dictionary with user credentials, including:
            - birthday (str): The user's birthday.
        - math_score (int): The math score of the user.
        - friend (dict): A dictionary containing:
            - used_today (bool): Indicates if the friend feature has been used today.
            - percentage (int): The percentage of friendship points used.

    Raises:
        IOError: If there is an error reading the file.
        json.JSONDecodeError: If the file cannot be parsed as JSON.

    Example:
        >>> all_users_info = get_all_users_info()
    """
    try:
        with open(USER_INFO_FILE, "r") as file:
            file_content = file.read()
            if file_content.strip():
                user_data = json.loads(file_content)
            else:
                user_data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}

    return user_data


def save_user_info(user_info: Dict[str, Any]) -> None:
    """
    Save user information to the JSON file.

    Args:
        user_info: A dictionary containing user information to be saved. It should include at least the user's ID
        as the key and other relevant user data such as username, first name, and credentials.

    Raises:
        IOError: If there is an error writing to the file.

    Example:
        >>> save_user_info(user_info)
    """
    existing_user_data = {}

    try:
        with open(USER_INFO_FILE, "r") as file:
            file_content = file.read()
            if file_content.strip():
                existing_user_data = json.loads(file_content)
    except FileNotFoundError:
        print("File not found. Creating a new one.")
    except Exception as e:
        print(f"Error occurred while reading user data: {e}")

    try:
        for user_id, info in user_info.items():
            if user_id in existing_user_data:
                existing_user_data[user_id].update(info)
            else:
                existing_user_data[user_id] = info

        with open(USER_INFO_FILE, "w") as file:
            json.dump(existing_user_data, file, indent=4)
    except IOError as e:
        print(f"Error writing user data: {e}")
    finally:
        file.close()


def get_and_save(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve user information and save it back to the JSON file.

    Args:
        user: The Telegram user object.

    Returns:
        dict: A dictionary containing user information with the following keys:
        - username (str): The username of the user.
        - first_name (str): The first name of the user.
        - credentials (dict): A dictionary with user credentials, including:
            - birthday (str): The user's birthday.
        - math_score (int): The math score of the user.
        - friend (dict): A dictionary containing:
            - used_today (bool): Indicates if the friend feature has been used today.
            - percentage (int): The percentage of friendship points used.

    Example:
        >>> user_info = get_and_save(user)
    """
    user_info = get_user_info(user)
    save_user_info(user_info)
    return user_info
