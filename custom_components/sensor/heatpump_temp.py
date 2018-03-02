"""
Platform to produce a sensor based on the temperature readings
provided by a mitsubishi_mqtt entity
"""
import asyncio
import logging

from homeassistant.const import TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity, async_device_update

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Heatpump Temp'

CONF_HEATPUMP = 'heatpump'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HEATPUMP): cv.entity_id,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the heatpump sensor platform."""
    heatpump_entity_id = config.get(CONF_HEATPUMP)
    name = config.get(CONF_NAME)
    async_add_devices([HeatpumpTemp(hass, name, heatpump_entity_id)], True)


class HeatpumpTemp(Entity):
    """Representation of a heatpump temperature sensor."""

    def __init__(self, hass, name, heatpump_entity_id):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._heatpump_entity_id = heatpump_entity_id
        self._unit_of_measurement = TEMP_FAHRENHEIT

    @property
    def should_poll(self):
        """No polling needed for a demo sensor."""
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    @asyncio.coroutine
    def async_update(self):
        """Update the state of the sensor."""
        # heatpump_states = yield from async_fetch_state(self._heatpump_entity_id)
        heatpump_states = hass.states.get(self._heatpump_entity_id)
        # heatpump_states = self._hass.states.get(self._heatpump_entity_id)
        _LOGGER.warning('heatpump_states: {0}'.format(heatpump_states))
        self._state = heatpump_states.attributes.get('current_temperature')
        _LOGGER.debug("New temperature: %s", self._state)
