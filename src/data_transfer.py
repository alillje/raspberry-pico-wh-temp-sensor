import urequests
from machine import Pin
import utime as utime
from blink import blink_lamp


def send_data_to_server(temp, hum, time):
    led = Pin("LED", Pin.OUT)

    # Send temperature, humidity and time data to a server via a POST request.
    try:
        print("Sending data to server.. ")
        # Set URL, headers and request body
        url = "<server-url>"
        headers = {"Content-Type": "application/json", "X-Api-Key": "<api-key>"}

        data = {"temperature": temp, "humidity": hum, "timestamp": time}

        response = urequests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            print("Data sent successfully.")
            # Blink the lamp to indicate sucess
            blink_lamp(3, 0.5)
    
        else:
            print("Failed to send data. Status code:", response.status_code)
            print(response.content)
            blink_lamp(1, 2)


        response.close()

    except Exception as e:
        print("Something went wrong when sending data to the server.")
        print("Error details:", repr(e))


