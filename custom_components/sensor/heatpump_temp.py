"""
Platform to produce a sensor based on the temperature readings
provided by a mitsubishi_mqtt entity
"""
import asyncio
import logging

from homeassistant.core import callback
from homeassistant.const import TEMP_FAHRENHEIT

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change

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
        self._state = None
        self._temp = 0

    async def async_added_to_hass(self):
        """Register callbacks."""
        @callback
        def filter_sensor_state_listener(entity, old_state, new_state):
            """Handle device state changes."""
            #_LOGGER.warning('all states: {0}'.format(self._hass.states.async_entity_ids() ))
            #_LOGGER.warning('sensor state: {0}'.format(new_state.state))
            #_LOGGER.warning('sensor attributes: {0}'.format(new_state.attributes))
            self._state = new_state.attributes['current_temperature']
            self.async_schedule_update_ha_state()

        async_track_state_change(self.hass, self._heatpump_entity_id, filter_sensor_state_listener)

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
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        state_attr = {
            'monkey': 'wild eep',
            'cow': 'moo',
            'dog': 'bark',
            'cat': 'meow'
        }
        return state_attr

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    #@asyncio.coroutine
    #def async_update(self):
        #"""Update the state of the sensor."""
        #_LOGGER.warning('all states: {0}'.format(self._hass.states.async_entity_ids() ))
        ## heatpump_states = yield from async_fetch_state(self._heatpump_entity_id)
        #heatpump_states = self._hass.states.get(self._heatpump_entity_id)
        #if heatpump_states:
            #_LOGGER.warning('hp name: {0}, state: {1}'.format(self._heatpump_entity_id, heatpump_states))
            #self._state = heatpump_states.attributes.get('current_temperature')
            #_LOGGER.debug("New temperature: %s", self._state)
