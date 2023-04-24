import utime
from machine import Pin

class InvalidChecksum(Exception):
    pass

class InvalidPulseCount(Exception):
    pass

class DHT11:
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
        self._last_measure = utime.ticks_us()
        self._temperature = -1
        self._humidity = -1

    def measure(self, retries=3):
        buffer = None

        for _ in range(retries):
            try:
                buffer = self._read_data()
                if buffer is not None:
                    break
            except InvalidChecksum:
                pass
            utime.sleep_ms(100)

        if buffer is None:
            return None, None

        self._humidity = buffer[0]
        self._temperature = buffer[2]

        return self._temperature, self._humidity

    def _send_init_signal(self):
        self._pin.init(Pin.OUT, Pin.PULL_DOWN)
        self._pin.value(1)
        utime.sleep_ms(50)
        self._pin.value(0)
        utime.sleep_ms(18)
        self._pin.init(Pin.IN, Pin.PULL_UP)

    def _read_data(self):
        self._send_init_signal()

        data = bytearray(5)
        idx = 0

        for _ in range(50):  # Up to 50 * 2 ms = 100 ms to start
            if self._pin.value() == 0:
                break
            utime.sleep_ms(2)
        else:
            return None

        for byte_idx in range(5):
            for bit_idx in range(8):
                while self._pin.value() == 0:  # Wait for the start of the HIGH pulse
                    pass
                start = utime.ticks_us()

                while self._pin.value() == 1:  # Wait for the end of the HIGH pulse
                    pass
                duration = utime.ticks_diff(utime.ticks_us(), start)

                data[byte_idx] <<= 1
                if duration > 50:
                    data[byte_idx] |= 1

        if (sum(data[0:4]) & 0xFF) != data[4]:
            raise InvalidChecksum()

        return data
