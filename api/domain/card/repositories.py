from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from api.db.models import Card


class CardRepository(SQLAlchemyAsyncRepository[Card]):
    """Card SQLAlchemy Repository."""

    model_type = Card
