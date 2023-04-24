import utime
from machine import Pin
from dht import DHT11, InvalidPulseCount

class Sensor:
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
        self._sensor = DHT11(self._pin)
        self._temperature = None
        self._humidity = None
        self._last_measure = 0

    def measure(self):
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, self._last_measure) < 10000 and self._temperature is not None and self._humidity is not None:
            return self._temperature, self._humidity

        try:
            self._sensor.measure()
            self._temperature = self._sensor.temperature
            self._humidity = self._sensor.humidity
            self._last_measure = current_time
            return self._temperature, self._humidity
        except InvalidPulseCount:
            print("InvalidPulseCount error")
            return None, None