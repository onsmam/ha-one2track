"""Switch platform for One2Track — setting toggles.

Step counter command code differs per model (0079 for Connect MOVE,
0082 for Connect UP). The correct code is determined from capability
discovery at setup time.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import STEP_COUNTER_CODES
from .coordinator import One2TrackCoordinator
from .entity import One2TrackEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import One2TrackConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: One2TrackConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up One2Track setting switches based on discovered capabilities."""
    coordinator = entry.runtime_data.coordinator
    entities: list[SwitchEntity] = [
        One2TrackPollingSwitch(coordinator, entry.entry_id),
    ]

    for device in coordinator.device_list:
        uuid = device["uuid"]
        step_code = coordinator.device_find_code(uuid, STEP_COUNTER_CODES)
        if step_code:
            entities.append(
                One2TrackStepCounterSwitch(coordinator, uuid, step_code)
            )

    async_add_entities(entities)


class One2TrackPollingSwitch(CoordinatorEntity[One2TrackCoordinator], SwitchEntity):
    """Switch to pause/resume automatic polling of the One2Track portal.

    Useful when GPS satellites are not working and frequent updates are
    unnecessary. Polling resumes instantly when turned back on.
    """

    _attr_translation_key = "polling"
    _attr_icon = "mdi:refresh-auto"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: One2TrackCoordinator, entry_id: str) -> None:
        """Initialize the polling switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_polling"

    @property
    def is_on(self) -> bool:
        """Return True when automatic polling is active."""
        return self.coordinator.polling_enabled

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable automatic polling and trigger an immediate refresh."""
        self.coordinator.set_polling_enabled(True)
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Pause automatic polling."""
        self.coordinator.set_polling_enabled(False)
        self.async_write_ha_state()


class One2TrackStepCounterSwitch(One2TrackEntity, SwitchEntity):
    """Switch to enable/disable the step counter on the watch."""

    _attr_translation_key = "step_counter"
    _attr_icon = "mdi:shoe-print"
    _attr_assumed_state = True

    def __init__(self, coordinator, uuid: str, cmd_code: str) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, uuid)
        self._attr_unique_id = f"{uuid}_step_counter"
        self._cmd_code = cmd_code
        self._is_on = True

    @property
    def is_on(self) -> bool:
        """Return True if step counter is enabled."""
        return self._is_on

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the resolved command code for debugging."""
        return {"cmd_code": self._cmd_code}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable step counter."""
        success = await self.coordinator.client.async_send_command(
            self._uuid, self._cmd_code, ["1"]
        )
        if success:
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable step counter."""
        success = await self.coordinator.client.async_send_command(
            self._uuid, self._cmd_code
        )
        if success:
            self._is_on = False
            self.async_write_ha_state()
