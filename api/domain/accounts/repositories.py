from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from api.db.models import Role, User, UserRole


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User SQLAlchemy Repository."""

    model_type = User


class RoleRepository(SQLAlchemyAsyncRepository[Role]):
    """User SQLAlchemy Repository."""

    model_type = Role


class UserRoleRepository(SQLAlchemyAsyncRepository[UserRole]):
    """User Role SQLAlchemy Repository."""

    model_type = UserRole
