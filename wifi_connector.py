import network
import urequests
import ntptime
import utime

def connect_to_network(ssid, password):
    """
    Connect to the specified WiFi network using the given credentials,
    and test the internet connection by making an HTTP GET request to Google.
    """
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object
    wlan.active(True)  # Activate the WLAN interface

    # Check if the WLAN interface is already connected to a network
    if wlan.isconnected():
        print("Already connected to a network.")
        response = urequests.get("http://www.google.com")
        if response.status_code == 200:
            print("Internet connection successful!")
        else:
            print("Failed to connect to Google. Please check your internet connection.")
        return

    # Connect to the specified network
    wlan.connect(ssid, password)

    # Wait for the WLAN interface to connect to the network
    while not wlan.isconnected():
        pass

    # Test the internet connection by making an HTTP GET request to Google
    print("Testing internet connection...")
    response = urequests.get("http://www.google.com")
    if response.status_code == 200:
        print("Internet connection successful!")
    else:
        print("Failed to connect to Google. Please check your internet connection.")

    # Print the network information once connected
    print("Connected to network:", ssid)
    print("Network config:", wlan.ifconfig())

def get_time_from_internet():
    try:
        response = urequests.get("https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm")
        if response.status_code == 200:
            data = response.json()
            year, month, day = data["year"], data["month"], data["day"]
            hour, minute, seconds, milli_seconds = data["hour"], data["minute"], data["seconds"], data["milliSeconds"]
            timestamp = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{seconds:02d}.{milli_seconds:03d}Z"
            # formatted_time = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(year, month, day, hour, seconds, milli_seconds)

            return timestamp
        else:
            print("Error retrieving time from the internet1: ", response.status_code)
    except Exception as e:
        print("Error retrieving time from the internet: ", e)