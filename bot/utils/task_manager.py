# 3rd built
import asyncio

# Custom
from tasks import friend_percent_reset, send_frog


class TaskManager:
    """
    Class responsible for managing background tasks.

    Attributes:
        tasks (list): List to store all running tasks.
        druzhba_id (int): Chat ID for the Druzhba chat.
        test_chat_id (int): Chat ID for the test chat.
    """

    def __init__(self) -> None:
        """
        Initialize the TaskManager with default values.
        """
        self.tasks = []

    async def add_task(self, coroutine, *args) -> asyncio.Task:
        """
        Add a new task to the TaskManager.

        Args:
            coroutine: The coroutine function to run as a task.
            *args: Arguments to pass to the coroutine.

        Returns:
            asyncio.Task: The created asyncio Task.

        Example:
            >>> task = await task_manager.add_task(task_manager.friend_percent_reset)
        """
        task = asyncio.create_task(coroutine(*args))
        self.tasks.append(task)
        print(f"Task added: {coroutine.__name__}")
        return task

    async def run_tasks(self, bot) -> None:
        """
        Run the background tasks managed by the TaskManager.

        Args:
            bot: The Telegram bot instance.

        Example:
            >>> await task_manager.run_tasks(bot)
        """
        await self.add_task(friend_percent_reset)
        await self.add_task(send_frog, bot)
        print("All tasks started.")

    def stop_tasks(self) -> None:
        """
        Stop all running tasks managed by the TaskManager.

        Example:
            >>> task_manager.stop_tasks()
        """
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()
        print("All tasks stopped... one more moment...")
