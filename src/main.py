from machine import Pin
import utime as time
from dht import DHT11, InvalidChecksum, InvalidPulseCount
import wifi_connector
from blink import blink_lamp
from umqtt.simple import MQTTClient


# Connect to WiFi network
try:
    wifi_connector.connect_to_network("Lillje-Luna", "santiagodechile")    
except:
    print("An error occured connecting to wifi")

# Get the LED pin
led = Pin("LED", Pin.OUT)


# Blink the lamp 5 times to confirm startup
blink_lamp(5, 0.3)
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)


sensor = DHT11(pin)


# MQQT-settings

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = "alillje"  # Your Adafruit IO username
mqtt_password = "aio_eTeQ95pjfZICOOYfoDBOEcLHj3Ki"  # Adafruit IO Key
mqtt_publish_topic_temperature = "alillje/feeds/temperature"
mqtt_publish_topic_humidity = "alillje/feeds/humidity"


# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "8c48dc57-4c00-4b90-9f9a-f506f2c15463"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

while True:
    try:
        # Measure temperature and humidity
        sensor.measure()
        temperature = sensor.temperature
        humidity = sensor.humidity
        
        # Convert temperature and humidity to strings
        temperature_str = str(temperature)
        humidity_str = str(humidity)

        # Publish the temperature payload to the Temperature MQTT topic
        mqtt_client.publish(mqtt_publish_topic_temperature, temperature_str)
        print(f'Temperature data successfully published: {temperature_str}')

        # Publish the humidity payload to the Humidity MQTT topic
        mqtt_client.publish(mqtt_publish_topic_humidity, humidity_str)
        print(f'Humidity data successfully published: {humidity_str}')


        # Blink the LED to indicate successful data transfer
        # blink_lamp(1, 0.1)

        # Wait before the next measurement
        time.sleep(5)
        # Check for exceptions, and continue to try to avoid program to crash
    except Exception as e:
    # Blink the LED to 2 times indicate unsuccessful data transfer
        blink_lamp(2, 0.1)
        print(f'Failed to publish message: {e}')
    continue

