import datetime
from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino
from loguru import logger

from app.config import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


async def on_startup(dispatcher: Dispatcher):
    logger.info("Setup PostgreSQL Connection")
    postgres_uri = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD.get_secret_value()}@" \
                   f"{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    await db.set_bind(postgres_uri)
    version = await db.scalar("SELECT version();")
    logger.info("Connected to {postgres}", postgres=version)


async def on_shutdown(dispatcher: Dispatcher):
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


def setup(app):
    app.on_startup.append(on_startup)
