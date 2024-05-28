import asyncio


class StateManager:
    """
    Singleton class to manage state information for various operations.
    Uses asyncio locks for thread-safe access to state data.
    """

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StateManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.state = {}
        return cls._instance

    @classmethod
    async def get_state(cls, category: str, user_id: str) -> dict:
        """
        Set or update the state for a specific user in a specific category.

        Args:
            category (str): The name of the state category.
            user_id (str): The ID of the user.
            state (dict): The state information to set or update.

        Example:
            >>> await StateManager.set_state('math', 'user1', {'score': 100})
        """
        async with cls._lock:
            return cls._instance.state.get(category, {}).get(user_id, {})

    @classmethod
    async def set_state(cls, category: str, user_id: str, state: dict) -> None:
        """
        Set or update the state for a specific user in a specific category.

        Args:
            category (str): The name of the state category.
            user_id (str): The ID of the user.
            state (dict): The state information to set or update.

        Example:
            >>> await StateManager.set_state('math', 'user1', {'score': 100})
        """
        async with cls._lock:
            if category not in cls._instance.state:
                cls._instance.state[category] = {}
            cls._instance.state[category].setdefault(user_id, {}).update(state)

    @classmethod
    async def remove_state(cls, category: str, user_id: str) -> None:
        """
        Remove the state for a specific user in a specific category.

        Args:
            category (str): The name of the state category.
            user_id (str): The ID of the user.

        Example:
            >>> await StateManager.remove_state('math', 'user1')
        """
        async with cls._lock:
            if category in cls._instance.state:
                cls._instance.state[category].pop(user_id, None)
