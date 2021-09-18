from aiogram import types
from loguru import logger
from aiogram.dispatcher.filters import Text
from app.misc import dp, i18n
from app.utils import keyboard

_ = i18n.gettext
settings_filter = Text(equals=keyboard.BUTTONS[0], ignore_case=True)
change_language_filter = Text(equals=keyboard.BUTTONS[1], ignore_case=True)


@dp.message_handler(settings_filter)
@dp.edited_message_handler(settings_filter)
async def settings_handler(message: types.Message):
    logger.info("User {user} get settings", user=message.from_user.id)
    await message.answer(_("Choose an action:"), reply_markup=keyboard.settings_markup())


@dp.message_handler(change_language_filter)
@dp.edited_message_handler(change_language_filter)
async def change_language_handler(message: types.Message):
    logger.info("User {user} get change language menu", user=message.from_user.id)
    await message.answer(_("Choose your language please:"), reply_markup=keyboard.choose_language_markup())