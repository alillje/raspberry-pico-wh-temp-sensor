from machine import Pin
import utime as time

led = Pin("LED", Pin.OUT)


def blink_lamp(times = 1, duration = 0.5):
    led.off()
    for i in range(times):
        led.on()
        time.sleep(duration)
        led.off()
        time.sleep(duration)

