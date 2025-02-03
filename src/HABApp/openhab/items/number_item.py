from collections.abc import Mapping
from typing import TYPE_CHECKING, Final

from HABApp.core.errors import InvalidItemValueError, ItemValueIsNoneError
from HABApp.openhab.definitions import (
    DecimalType,
    QuantityType,
    QuantityValue,
    RefreshType,
    UnDefType,
)
from HABApp.openhab.items.base_item import MetaData, OpenhabItem, ValueToOh


if TYPE_CHECKING:
    MetaData = MetaData     # noqa: PLW0127
    Mapping = Mapping       # noqa: PLW0127


# https://github.com/openhab/openhab-core/blob/main/bundles/org.openhab.core/src/main/java/org/openhab/core/library/items/NumberItem.java
class NumberItem(OpenhabItem):
    """NumberItem which accepts and converts the data types from OpenHAB

    :ivar str name: |oh_item_desc_name|
    :ivar int | float value: |oh_item_desc_value|

    :ivar str | None label: |oh_item_desc_label|
    :ivar frozenset[str] tags: |oh_item_desc_tags|
    :ivar frozenset[str] groups: |oh_item_desc_group|
    :ivar Mapping[str, MetaData] metadata: |oh_item_desc_metadata|
    """

    _update_to_oh: Final = ValueToOh('NumberItem', DecimalType, QuantityType, UnDefType)
    _command_to_oh: Final = ValueToOh('NumberItem', DecimalType, QuantityType, RefreshType)
    _state_from_oh_str: Final = staticmethod(DecimalType.from_oh_str)

    @property
    def unit(self) -> str | None:
        """Return the item unit if it is a "Unit of Measurement" item else None"""
        if (unit := self.metadata.get('unit')) is None:
            return None
        return unit.value

    def set_value(self, new_value) -> bool:

        if isinstance(new_value, QuantityValue):
            return super().set_value(new_value.value)

        if isinstance(new_value, (int, float)):
            return super().set_value(new_value)

        if new_value is None:
            return super().set_value(new_value)

        raise InvalidItemValueError.from_item(self, new_value)

    def __bool__(self) -> bool:
        if self.value is None:
            raise ItemValueIsNoneError.from_item(self)
        return bool(self.value)
