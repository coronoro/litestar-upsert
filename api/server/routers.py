"""Application Modules."""
from __future__ import annotations

from typing import TYPE_CHECKING

from api.domain.accounts.controllers import AccessController, UserController, UserRoleController
from api.domain.card.controllers import CardController

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler

route_handlers: list[ControllerRouterHandler] = [
    AccessController,
    UserController,
    UserRoleController,
    CardController,
]
