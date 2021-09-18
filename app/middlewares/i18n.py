from dataclasses import dataclass, field
from typing import Any, Tuple
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from app.models import user


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):
    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇺🇸", "English"),
        "ru": LanguageData("🇷🇺", "Русский")
    }

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        tg_user = types.User.get_current()
        *_, data = args
        user_data = await user.get_user(tg_user.id)
        if user_data is None or tg_user is None:
            data['locale'] = 'en'
            return 'en'
        else:
            data['locale'] = user_data.language
            lang = user_data.language
            return lang
