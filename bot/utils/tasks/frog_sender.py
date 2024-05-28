# 3rd party
from pytz import timezone

# Built-in
import os
import random
import asyncio
from pathlib import Path
from datetime import datetime


async def send_frog(bot):
    """
    Send an image every Wednesday at 9:00 AM CET.

    This task runs indefinitely and sends a random image from the 'img' folder
    to the Druzhba chat every Wednesday at 9:00 AM CET.

    Args:
        bot: The Telegram bot instance.

    Example:
        >>> await task_manager.frog_sender(bot)
    """
    try:
        while True:
            druzhba: int = -1001545165176
            test_chat: int = -4198289287
            current = datetime.now(timezone("CET"))

            # Send the image
            if current.weekday() == 2 and current.hour == 9:
                print("Looking for a pic")
                image_folder = os.path.join(os.getcwd(), "img")
                image_files = [
                    f
                    for f in Path(image_folder).iterdir()
                    if f.is_file() and f.suffix.lower() in [".jpg", ".png", ".gif"]
                ]
                if image_files:
                    random_image = random.choice(image_files)
                    image_path = str(random_image)
                    try:
                        with open(image_path, "rb") as photo:
                            await bot.send_photo(chat_id=druzhba, photo=photo)
                        print(f"Image '{random_image}' sent to the Druzhba")
                    except Exception as e:
                        print(f"An error occurred while sending the photo: {e}")
                else:
                    print("No image found in the folder:", image_folder)
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        # Cancel the task if it's cancelled
        pass
