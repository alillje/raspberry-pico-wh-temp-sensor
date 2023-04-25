from machine import Pin, I2C
import utime as time
# from dht import DHT11, InvalidChecksum
from dht_v2 import DHT11
from sensor import Sensor
import wifi_connector
import data_transfer
from blink import blink_lamp

# Connect to WiFi network
wifi_connector.connect_to_network("<wifi-name>", "<wifi password>")
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C Using Pins GP8 And GP9 "Default I2C0 Pins"
led = Pin("LED", Pin.OUT)

# Blink the lamp 5 times to confirm startup
blink_lamp(3, 1)

sensor = Sensor(28)


while True:
    
    # Blink the lamp 3 times to confirm entering loop
    blink_lamp(3, 0.1)

    time.sleep(2)
    # pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    #sensor = DHT11(pin)

    # t = (sensor.temperature)
    # h = (sensor.humidity)

    temperature, humidity = sensor.measure()

    # current_time = time.localtime()
    # Get the time from the internet
    current_time = wifi_connector.get_time_from_internet()
 
    # Format time so it can be parsed to Datetime object
    # formatted_time = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])

    if temperature is None or humidity is None:
        print("Error reading sensor data, skipping data transfer")
    else:
        # Log information
        print("Current time:", current_time)
        print("Temperature: {}".format(temperature))
        print("Humidity: {}".format(humidity))
        # Blink the lamp 2 times to confirm reading data
        blink_lamp(2, 0.4)
        data_transfer.send_data_to_server(temperature, humidity, current_time )
        print("- - - - - - - - - - - - - - - - - - - - - -")
    time.sleep(5)
