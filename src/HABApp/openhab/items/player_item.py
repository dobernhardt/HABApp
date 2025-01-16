from collections.abc import Mapping
from typing import TYPE_CHECKING, Final, Optional

from HABApp.openhab.definitions import (
    NextPreviousType,
    PlayPauseType,
    RefreshType,
    RewindFastforwardType,
    StringType,
    UnDefType,
)
from HABApp.openhab.items.base_item import MetaData, OpenhabItem, ValueToOh


if TYPE_CHECKING:
    MetaData = MetaData
    Optional = Optional
    Mapping = Mapping


# https://github.com/openhab/openhab-core/blob/main/bundles/org.openhab.core/src/main/java/org/openhab/core/library/items/PlayerItem.java
class PlayerItem(OpenhabItem):
    """PlayerItem which accepts and converts the data types from OpenHAB

    :ivar str name: |oh_item_desc_name|
    :ivar str value: |oh_item_desc_value|

    :ivar str | None label: |oh_item_desc_label|
    :ivar frozenset[str] tags: |oh_item_desc_tags|
    :ivar frozenset[str] groups: |oh_item_desc_group|
    :ivar Mapping[str, MetaData] metadata: |oh_item_desc_metadata|
    """

    _update_to_oh: Final = ValueToOh('PlayerItem', PlayPauseType, RewindFastforwardType, UnDefType)
    _command_to_oh: Final = ValueToOh('PlayerItem', PlayPauseType, RewindFastforwardType, NextPreviousType, RefreshType)
    _state_from_oh_str: Final = staticmethod(StringType.from_oh_str)
