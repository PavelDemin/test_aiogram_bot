from app.misc import dp, i18n
from app.models import db
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiohttp import web
from app.config import config
import secrets

_ = i18n.gettext
secret_key = secrets.token_urlsafe(48)


async def on_startup(web_app: web.Application):
    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(f"https://{config.DOMAIN}/{config.WEBHOOK_PATH}/{secret_key}")


async def execute(req: web.Request) -> web.Response:
    upds = [types.Update(**(await req.json()))]
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    try:
        await dp.process_updates(upds)
    except Exception as e:
        logger.error(e)
    finally:
        return web.Response()


def setup():
    app = web.Application()
    db.setup(app)
    app.on_startup.append(on_startup)
    app.add_routes([web.post(f"/{config.WEBHOOK_PATH}/{secret_key}", execute)])
    web.run_app(app, port=config.BOT_PUBLIC_PORT, host=config.PUBLIC_HOST)
