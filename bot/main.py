"""
Main script for running the Telegram bot.

This script initializes the bot application, sets up command and message handlers,
and starts the bot. It also manages tasks and handles errors.

Modules:
- dotenv: Loads environment variables from a .env file.
- telegram.ext: Provides the Application class for building the bot application,
  CommandHandler, MessageHandler, filters, and CallbackQueryHandler for handling
  different types of Telegram updates.
- os: Provides functions for interacting with the operating system.
- asyncio: Provides infrastructure for writing single-threaded concurrent code
  using coroutines.
- commands: Contains command handling functions.
- handlers: Contains functions for handling callback queries, messages, and errors.
- utils: Contains utility classes and functions.

Usage:
Run the script to start the Telegram bot.
"""

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

# Built-in
import os
import asyncio

# Custom
from commands import *
from handlers import handle_callback_query, handle_message, handle_error
from utils import TaskManager

load_dotenv()


async def main():
    print("Preparing...")
    app = Application.builder().token(os.getenv("API_KEY")).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("friend", friend_command))
    app.add_handler(CommandHandler("birthday", birthday_command))
    app.add_handler(CommandHandler("math", math_command))

    app.add_handler(CallbackQueryHandler(handle_callback_query))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(handle_error)

    task_manager = TaskManager()
    await task_manager.run_tasks(app.bot)

    print("Initializing...")
    await app.initialize()

    print("Starting...")
    await app.start()

    print("Polling...")
    await app.updater.start_polling(poll_interval=0.5)

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Stopping... it may take a while...")
    finally:
        task_manager.stop_tasks()
        await app.stop()
        await app.updater.stop()


if __name__ == "__main__":
    asyncio.run(main())
