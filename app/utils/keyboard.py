from aiogram.utils.callback_data import CallbackData
from app.misc import i18n
from app.config import config
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from typing import List, Union

cb_property = CallbackData("id", "property", "value")


_ = i18n.lazy_gettext


BUTTONS = [
    _("🛠 Settings"),
    _("🌐 Change language"),
    _("⬅️ Main menu"),
    _("📝 Make an appointment"),
    _("🗒 List of records"),
    _("❌ Cancel"),
    _("✅ Confirm"),
    _("❌ Decline"),
    _("Show more 👉")
]


def main_menu_markup(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTONS[3]),
            KeyboardButton(text=BUTTONS[0]),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)


def choose_language_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for code, language in i18n.AVAILABLE_LANGUAGES.items():
        markup.add(
            InlineKeyboardButton(
                language.label, callback_data=cb_property.new(property="language", value=code)
            )
        )
    return markup


def send_contact_markup() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=_("📱 Send contact"),
                request_contact=True
            )
        ]
    ], resize_keyboard=True)


def settings_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTONS[1]),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)


def cancel_button_markup() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[4],
                callback_data=cb_property.new(
                    property="cancel",
                    value=0
                )
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def admin_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTONS[4]),
        ],
        [
            KeyboardButton(text=BUTTONS[2]),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)


def generate_list_markup(data: List[list], start: Union[int, str] = 0) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in data[:config.COUNT_RECORDS_RER_PAGE]:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{i[3]} {i[0]}. {i[1]} - {i[2]}",
                callback_data=cb_property.new(
                    property="show_record",
                    value=i[0]
                )
            )
        ])
    if len(data) > config.COUNT_RECORDS_RER_PAGE:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=BUTTONS[8],
                callback_data=cb_property.new(
                    property="show_more",
                    value=int(start) + config.COUNT_RECORDS_RER_PAGE
                )
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def confirm_markup(value: Union[int, str]) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[6],
                callback_data=cb_property.new(
                    property="confirm",
                    value=value
                )
            ),
            InlineKeyboardButton(
                text=BUTTONS[7],
                callback_data=cb_property.new(
                    property="decline",
                    value=value
                )
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
