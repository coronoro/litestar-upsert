from typing import Iterable

from advanced_alchemy.exceptions import wrap_sqlalchemy_exception
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.repository.typing import ModelT

from api.db.models import Card


class CardRepository(SQLAlchemyAsyncRepository[Card]):
    """Card SQLAlchemy Repository."""

    model_type = Card

    async def upsert_with_merge(
        self,
        data: ModelT,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_expunge: bool | None = None,
        auto_commit: bool | None = None,
        auto_refresh: bool | None = None,
        match_fields: list[str] | str | None = None,
    ) -> ModelT:
        if match_fields := self._get_match_fields(match_fields=match_fields):
            match_filter = {
                field_name: getattr(data, field_name, None)
                for field_name in match_fields
                if getattr(data, field_name, None) is not None
            }
        elif getattr(data, self.id_attribute, None) is not None:
            match_filter = {self.id_attribute: getattr(data, self.id_attribute, None)}
        else:
            match_filter = data.to_dict()
        existing = await self.get_one_or_none(**match_filter)
        if not existing:
            return await self.add(data, auto_commit=auto_commit, auto_expunge=auto_expunge, auto_refresh=auto_refresh)
        with wrap_sqlalchemy_exception():
            data = self._merge_on_match_fields([data], [existing], match_fields)[0] # kinda hacky
            instance = await self._attach_to_session(data, strategy="merge")
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
                auto_refresh=auto_refresh,
            )
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance


