import network
import urequests

def connect_to_network(ssid, password):
    
    # Connect to the specified WiFi network using the given credentials,
    # and test the internet connection by making an HTTP GET request to Google.

    # Create WLAN object
    wlan = network.WLAN(network.STA_IF)
    
    # Activate the WLAN interface
    wlan.active(True)

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
