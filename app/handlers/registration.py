from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.filters import OrFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import hbold
from loguru import logger
from app.misc import dp, i18n
from app.models import user
from app.utils import keyboard, helpers


class Registration(StatesGroup):
    name = State()
    phone = State()


_ = i18n.gettext


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    u = await user.get_user(message.from_user.id)
    if u is not None:
        await message.answer(_("Hi {user_name}! Choose menu item:").format(user_name=hbold(u.name)),
                             reply_markup=keyboard.main_menu_markup(message.from_user.id))
    else:
        await message.answer("Hi {user}!\nChoose your language please👇".format(
            user=hbold(message.from_user.full_name)
        ), reply_markup=keyboard.choose_language_markup())


@dp.callback_query_handler(
    OrFilter(
        *[
            keyboard.cb_property.filter(property="language", value=code)
            for code in i18n.AVAILABLE_LANGUAGES
        ]
    )
)
async def cq_choose_language(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    target_language = callback_data["value"]
    logger.info(
        "User {user} set language '{language}'",
        user=query.from_user.id,
        language=target_language,
    )
    i18n.ctx_locale.set(target_language)
    u = await user.get_user(query.message.chat.id)
    if u is None:
        await user.create_user(query.message.chat.id, target_language)
        async with state.proxy() as data:
            data["language"] = target_language
        await query.message.answer(_("Let's meet, what's your name?"))
        await Registration.name.set()
        await query.answer()

    else:
        await user.update_user(query.message.chat.id, u.name, u.phone, target_language)
        await query.message.answer(_("Language changed successfully."),
                                   reply_markup=keyboard.main_menu_markup(query.message.chat.id))
        await query.answer()


@dp.message_handler(state=Registration.name)
async def input_name_handler(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input name: '{name}'",
        user=message.from_user.id,
        name=message.text
    )
    if helpers.check_name(message.text):
        async with state.proxy() as data:
            data["name"] = message.text
        await message.answer(_("Please, enter your phone number or send a contact by clicking on the button below:"),
                             reply_markup=keyboard.send_contact_markup())
        await Registration.phone.set()
    else:
        await message.answer(_("The name is not correct! Please try again."))


@dp.message_handler(content_types=types.ContentTypes.CONTACT | types.ContentTypes.TEXT, state=Registration.phone)
async def input_name_handler(message: types.Message, state: FSMContext):
    u = await user.get_user(message.chat.id)
    if message.content_type in types.ContentTypes.TEXT:
        phone = helpers.parse_phone(message.text)
        if phone is None:
            await message.answer(_("The phone number is incorrect! Please try again."))
            return
    else:
        phone = int(message.contact.phone_number)
    async with state.proxy() as data:
        await user.update_user(
            chat_id=message.chat.id,
            name=data["name"],
            phone=phone,
            language=u.language
        )
    logger.info(
        "User {user} input phone number: '{phone}'",
        user=message.from_user.id,
        phone=phone
    )
    await state.finish()
    await message.answer(_("Thank you for registering! You can now start recording. Please, choose menu item:"),
                         reply_markup=keyboard.main_menu_markup(message.chat.id))
