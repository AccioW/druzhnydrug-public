# 3rd party
from telegram import Update
from pytz import timezone

# Built-in
import asyncio
from datetime import datetime 

# Custom
from ..data_manager import get_user_info


async def announce_birthday(update: Update):
    try:
        while True:
            druzhba: int = -1001545165176
            user = update.
            
            mention = f"@{user.username}"
            days = []
            
            current = datetime.now(timezone("CET"))
            if current.day == 
            
            
            prompt = f"Сегодня у {mention} день рождения!! Поздравим его!🥳🎂"
            
            
            await asyncio.sleep(86400)
    except asyncio.CancelledError:
        # Cancel the task if it's cancelled
        pass