from machine import Pin
import utime as time
from dht import DHT11, InvalidChecksum, InvalidPulseCount
import wifi_connector
import data_transfer
from blink import blink_lamp

# Connect to WiFi network
try:
    wifi_connector.connect_to_network("<wifi-ssid>", "<wifi-password>")    
except:
    print("An error occured connecting to wifi")

# Get the LED pin
led = Pin("LED", Pin.OUT)


# Blink the lamp 5 times to confirm startup
blink_lamp(5, 1)
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)


sensor = DHT11(pin)


while True:
    
    # Blink the lamp 1 time to confirm entering loop
    blink_lamp(1, 0.1)

    time.sleep(2)

    try:
        # Get the temperatur and humidity
        temperature = (sensor.temperature)
        time.sleep(2)
        humidity = (sensor.humidity)
        
        # Get the current time from internet
        current_time = wifi_connector.get_time_from_internet()

        # Log information about the data
        print("Current time:", current_time)
        print("Temperature: {}".format(temperature))
        print("Humidity: {}".format(humidity))
        
        # Blink the lamp 2 times to confirm reading data
        blink_lamp(2, 0.4)
        
        # Send data to server
        data_transfer.send_data_to_server(temperature, humidity, current_time )
        print("- - - - - - - - - - - - - - - - - - - - - -")
        # Wait 15 minutes until next read
        time.sleep(15*60)
    except Exception as e:
        print("An exception occurred:", e)
        print("Error reading sensor data, skipping data transfer")
        continue


