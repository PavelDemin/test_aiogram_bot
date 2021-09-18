from typing import Union, List
from app.models.db import TimedBaseModel, db
from datetime import datetime
from app.models.user import User


class Record(TimedBaseModel):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    record_date = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)
    comment = db.Column(db.String)


async def get_records_by_user(user_id: int) -> List[Record]:
    return await Record.query.where(Record.user_id == user_id).gino.all()


async def get_all_records() -> List[Record]:
    async with db.transaction():
        data = await Record.load(parent=User).query.order_by(Record.created_at.desc()).gino.all()
    return data


async def create_record(user_id: int, record_date: datetime) -> dict:
    rv = await Record.create(
        user_id=user_id,
        record_date=record_date
    )
    return rv.to_dict()


async def get_records_by_id(record_id: Union[int, str]) -> Record:
    async with db.transaction():
        data = await Record.load(parent=User).query.where(Record.id == int(record_id)).gino.first()
    return data


async def update_status(record_id: Union[int, str], status: int, comment: str = None):
    return await Record.update. \
                values(status=status). \
                values(comment=comment). \
                where(Record.id == int(record_id)).gino.status()
