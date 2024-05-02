from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.models import Card
from api.domain.card.services import CardService


async def provide_card_service(db_session: AsyncSession | None = None) -> AsyncGenerator[CardService, None]:
    """Provide card service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        CardService: A card service object
    """
    async with CardService.new(
            session=db_session,
            statement=select(Card),
    ) as service:
        yield service
