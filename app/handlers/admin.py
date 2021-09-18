from aiogram import types
from loguru import logger
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import hbold
from app.misc import dp, i18n
from app.utils import keyboard
from app.config import config
from app.models import record, user
from app.utils import helpers


class Admin(StatesGroup):
    comment = State()


_ = i18n.gettext
record_list_filter = Text(equals=keyboard.BUTTONS[4], ignore_case=True)


@dp.message_handler(Command("admin"), user_id=config.ADMIN, state="*")
async def admin_handler(message: types.Message, state: FSMContext):
    await state.reset_state()
    logger.info("User {user} get admin menu", user=message.from_user.id)
    await message.answer(_("Choose menu item:"), reply_markup=keyboard.admin_markup())


@dp.message_handler(record_list_filter)
@dp.edited_message_handler(record_list_filter)
async def record_list_handler(message: types.Message):
    records = await get_record_list()
    if len(records) != 0:
        msg = _("Look the record list bellow:")
        logger.info("User {user} get record list", user=message.from_user.id)
        await message.answer(msg, reply_markup=keyboard.generate_list_markup(records))
    else:
        await message.answer(_("Records not found :("), reply_markup=keyboard.main_menu_markup(message.chat.id))


@dp.callback_query_handler(keyboard.cb_property.filter(property="show_record"))
async def show_record_admin_handler(query: types.CallbackQuery, callback_data: dict):
    record_data = await record.get_records_by_id(callback_data["value"])
    msg = _("Name: {}\n").format(hbold(record_data.parent.name))
    msg += _("Record date: {}\n").format(hbold(record_data.record_date.strftime("%d.%m.%Y")))
    if record_data.comment is not None:
        msg += _("Comment: {}").format(hbold(record_data.comment))
    await query.message.edit_text(_("Record info:\n\n") + msg, reply_markup=keyboard.confirm_markup(callback_data["value"]))
    await query.answer()


@dp.callback_query_handler(keyboard.cb_property.filter(property="show_more"))
async def show_more_records_handler(query: types.CallbackQuery, callback_data: dict):
    logger.info("User {user} show more records.", user=query.message.chat.id)
    records = await get_record_list()
    msg = _("Look the record list bellow:")
    await query.message.edit_text(msg, reply_markup=keyboard.generate_list_markup(records[int(callback_data["value"]):]))


@dp.callback_query_handler(keyboard.cb_property.filter(property="confirm"))
async def confirm_record_admin_handler(query: types.CallbackQuery, callback_data: dict):
    await record.update_status(callback_data["value"], 1)
    logger.info("User {user} set status 'Confirmed' in record id: {record_id}",
                user=query.message.chat.id,
                record_id=callback_data["value"])
    msg = _("Look the record list bellow:")
    records = await get_record_list()
    await query.message.edit_text(msg, reply_markup=keyboard.generate_list_markup(records))
    await query.answer()


@dp.callback_query_handler(keyboard.cb_property.filter(property="decline"))
async def decline_record_admin_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await record.update_status(callback_data["value"], 2)
    logger.info("User {user} set status 'Decline' in record id: {record_id}",
                user=query.message.chat.id,
                record_id=callback_data["value"])
    await query.message.answer(_("Add comment, please:"))
    await Admin.comment.set()
    async with state.proxy() as data:
        data["record_id"] = callback_data["value"]
    await query.answer()


@dp.message_handler(state=Admin.comment)
async def input_comment_handler(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input comment: '{comment}'",
        user=message.from_user.id,
        comment=message.text
    )
    async with state.proxy() as data:
        await record.update_status(data["record_id"], 2, message.text)
        r = await record.get_records_by_id(data["record_id"])
        u = await user.get_user(r.parent.chat_id)
        i18n.ctx_locale.set(u.language)
        msg = _("Your record has been decline, see message bellow:\n\n {}").format(hbold(message.text))
        await helpers.send_message(r.parent.chat_id, msg)
    msg = _("Look the record list bellow:")
    records = await get_record_list()
    await message.answer(msg, reply_markup=keyboard.generate_list_markup(records))
    await state.finish()


async def get_record_list() -> list:
    records = []
    [records.append([i.id, i.parent.name, i.record_date.strftime("%d.%m.%Y"), helpers.show_status(i.status)]) for i in
     await record.get_all_records()]
    return records
