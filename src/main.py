from machine import Pin
import utime as time
from dht import DHT11, InvalidChecksum, InvalidPulseCount
import wifi_connector
from blink import blink_lamp
from umqtt.simple import MQTTClient


# Connect to WiFi network, provide credentials (SSID, Wi-FI password as arguments)
try:
    wifi_connector.connect_to_network("WIFI SSID", "WIFI PASSWORD")    
except:
    print("An error occured connecting to wifi")

# Get the LED pin
led = Pin("LED", Pin.OUT)

# Blink the lamp 5 times to confirm startup
blink_lamp(5, 0.3)
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)

# Initialize the DHT11 sensor
sensor = DHT11(pin)


'''
### MQQT-settings ###
'''
# Define Adafruit IO Authentication
mqtt_host = "io.adafruit.com"
mqtt_username = "username"  # Adafruit IO username
mqtt_password = "aio_SECRET_KEY"  # Adafruit IO Key

# Feed MQTT Topic details
# Publish topics
mqtt_publish_topic_temperature = "example/feeds/temperature"
mqtt_publish_topic_humidity = "example/feeds/humidity"

# Subscribe topics
mqtt_subscribe_topic_led = "example/feeds/led"

# Enter a random ID for this MQTT Client
mqtt_client_id = "Unique client ID (Secret)"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

# Function to handle incoming MQTT messages
# Checks if "on" or "off" message has been published by the LED topic
# That is subscribed to
# Turns LED on/off, depending on message
def handle_incoming_messages(topic, msg):
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')
    if topic == mqtt_subscribe_topic_led:
        if msg == "on":
            led.value(1)
        elif msg == "off":
            led.value(0)
            
# Register the message handler function
mqtt_client.set_callback(handle_incoming_messages)

# Subscribe to the LED topic
mqtt_client.subscribe(mqtt_subscribe_topic_led)

while True:
    try:
        # Call mqtt_client.check_msg() to handle incoming messages
        mqtt_client.check_msg()
        
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

        # Wait before the next measurement
        time.sleep(5)
        
        # Check for exceptions, and continue to try to avoid program to crash
    except Exception as e:
        print(f'Failed to publish message: {e}')
    continue

