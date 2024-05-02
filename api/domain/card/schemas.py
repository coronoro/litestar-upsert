from uuid import UUID

from sqlalchemy import JSON

from api.lib.schema import CamelizedBaseStruct


class Card(CamelizedBaseStruct):
    """User properties to use for a response."""

    name: str
