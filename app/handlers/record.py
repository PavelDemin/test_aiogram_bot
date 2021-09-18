from aiogram import types
from loguru import logger
from aiogram.dispatcher.filters import Text
from app.misc import dp, i18n
from app.utils import keyboard
from app.utils.simple_calendar import SimpleCalendar, calendar_callback
from app.models import record, user
from aiogram.utils.callback_data import CallbackData


_ = i18n.gettext
add_record_filter = Text(equals=keyboard.BUTTONS[3], ignore_case=True)


@dp.message_handler(add_record_filter)
@dp.edited_message_handler(add_record_filter)
async def add_record_handler(message: types.Message):
    logger.info("User {user} add record.", user=message.from_user.id)
    await message.answer(_("Choose date, please:"), reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(query: types.CallbackQuery, callback_data: CallbackData):
    selected, selected_date = await SimpleCalendar().process_selection(query, callback_data)
    if selected:
        u = await user.get_user(query.message.chat.id)
        if selected_date in [i.record_date for i in await record.get_records_by_user(u.id)]:
            await query.message.answer(_("Sorry, but you are already signed up for this date!"))
            return
        await record.create_record(u.id, selected_date)
        await query.message.answer(
            _("You have successfully signed up for {record_date}. Our manager will contact you.").format(
                record_date=selected_date.strftime("%d.%m.%Y")),
            reply_markup=keyboard.main_menu_markup(query.message.chat.id))
    await query.answer()
