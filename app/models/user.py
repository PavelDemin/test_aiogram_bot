from app.models.db import TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    chat_id = db.Column(db.Integer)
    name = db.Column(db.String)
    phone = db.Column(db.BigInteger)
    language = db.Column(db.String)


async def get_user(chat_id: int) -> User:
    return await User.query.where(User.chat_id == chat_id).gino.first()


async def create_user(chat_id: int, language: str) -> dict:
    rv = await User.create(
        chat_id=chat_id,
        language=language
    )
    return rv.to_dict()


async def update_user(chat_id: int, name: str, phone: int, language: str):
    return await User.update. \
        values(name=name). \
        values(phone=phone). \
        values(language=language). \
        where(User.chat_id == chat_id).gino.status()