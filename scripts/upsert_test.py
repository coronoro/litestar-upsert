import asyncio
import string
import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api.config import get_settings
from api.db.models import Card
from api.domain.card.repositories import CardRepository


def get_session(engine=None):
    settings = get_settings()
    if engine is None:
        engine = settings.db.get_engine()
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def get_update():
    """
    dummy method generates a
    :return:
    """
    return {
        "name": "Name",
        "external_id": "86bf43b1-8d4e-4759-bb2d-0b2e03ba7012"
    }


async def import_json():
    async_session = get_session()
    async with async_session() as session:
        card_repo = CardRepository(session=session)
        update = get_update()
        card = Card()
        card.name = update['name']
        card.external_id = update['external_id']
        # await card_repo.upsert_with_merge(data=card, match_fields=["external_id"])# works
        # await card_repo.upsert(data=card, match_fields=["external_id"])# dont work
        await card_repo.upsert_many(data=[card], match_fields=["external_id"]) # works
        await session.commit()

asyncio.run(import_json())
