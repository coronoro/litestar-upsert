from typing import TYPE_CHECKING, Annotated

from litestar import Controller, get
from litestar.pagination import OffsetPagination
from litestar.params import Dependency

from api.domain.card import urls
from api.domain.card.schemas import Card
from api.domain.card.services import CardService
from advanced_alchemy.filters import FilterTypes

class CardController(Controller):
    tags = ["Cards"]
    dto = None
    return_dto = None

    @get(
        operation_id="ListCards",
        name="cards:list",
        summary="List Cards",
        description="Retrieve the cards.",
        path=urls.CARD_LIST,
        cache=60,
    )
    async def list_cards(
            self,
            cards_service: CardService,
            filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Card]:
        """List users."""
        results, total = await cards_service.list_and_count(*filters)
        return cards_service.to_schema(data=results, total=total, schema_type=Card, filters=filters)
