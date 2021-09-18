import re
import asyncio
from app.misc import bot
from aiogram.utils import exceptions
from aiogram.types import InlineKeyboardMarkup
from loguru import logger


def check_name(name: str) -> bool:
    regex = re.compile(r"^[a-zA-ZА-Яа-я\'\-\ ]{2,16}$")
    if regex.findall(name):
        return True
    else:
        return False


def parse_phone(text: str) -> int:
    phone = re.sub(r"|\+|\-|\(|\)| |$", "", text)
    regex = re.compile(r"^([+]?\d{1,2}[-\s]?|)\d{3}[-\s]?\d{3}[-\s]?\d{4}$")
    if regex.match(phone):
        return int(phone)


def show_status(int_st: int):
    if int_st == 0:
        return "❔"
    if int_st == 1:
        return "✅"
    if int_st == 2:
        return "❌"


async def send_message(user_id: int,
                       text: str,
                       disable_notification: bool = False,
                       disable_web_page_preview: bool = True,
                       reply_markup: InlineKeyboardMarkup = None) -> bool:
    try:
        await bot.send_message(chat_id=user_id,
                               text=text,
                               disable_notification=disable_notification,
                               disable_web_page_preview=disable_web_page_preview,
                               reply_markup=reply_markup)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False
