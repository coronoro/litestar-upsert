from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from api.db.models import Card
from api.domain.card.repositories import CardRepository


class CardService(SQLAlchemyAsyncRepositoryService[Card]):
    repository_type = CardRepository
