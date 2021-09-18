from typing import Union
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger
from app.misc import dp, i18n
from app.utils.keyboard import (
    cb_property,
    main_menu_markup,
    BUTTONS
)

_ = i18n.gettext


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
    return True


menu_filter = Text(equals=BUTTONS[2], ignore_case=True)


@dp.callback_query_handler(cb_property.filter(property="cancel"), state="*")
@dp.message_handler(menu_filter)
@dp.edited_message_handler(menu_filter)
async def menu_handler(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    logger.info("User {user} get main menu", user=message.chat.id)
    await state.finish()
    await message.answer(_("Choose menu item:"), reply_markup=main_menu_markup(message.chat.id))
