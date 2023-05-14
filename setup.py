import network
import socket
import time
import machine


def url_decode(url):
    url = url.replace("%2F", "/")
    url = url.replace("%3A", ":")
    # Add more replacements for other special characters as needed
    return url




def switch_to_ap_mode():
    ap_ssid = "TD_setup"
    ap_password = ""

    # Initialize the access point interface
    ap = network.WLAN(network.AP_IF)

    # Disable the access point interface (AP mode) if it is active
    if ap.active():
        ap.active(False)

    # Disable the station interface (STA mode) if it is active
    wifi = network.WLAN(network.STA_IF)
    if wifi.active():
        wifi.active(False)

    # Enable the access point interface (AP mode)
    ap.active(True)

    # Configure the access point SSID and password
    ap.config(essid=ap_ssid, password=ap_password)

    print("ESP32-C3 switched to AP mode.")



def check_wifi_connection():
    wifi = network.WLAN(network.STA_IF)
    while not wifi.isconnected():
        time.sleep(1)
    print("Wi-Fi connected:", wifi.ifconfig()[0])

def serve_webpage():
    # Switch ESP32-C3 to AP mode
    switch_to_ap_mode()

    # Initialize the access point interface
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    print("ESP32-C3 switched to AP mode.")

    # Create a socket and bind it to a specific address and port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(1)

    print("Web server started. Listening for connections...")

    # Read the contents of the HTML template files
    with open('html/index.html', 'r') as main_file:
        main_html = main_file.read()

    with open('html/wifi.html', 'r') as wifi_file:
        wifi_html = wifi_file.read()

    with open('html/td.html', 'r') as td_file:
        td_html = td_file.read()

    with open('html/gp.html', 'r') as gp_file:
        gp_html = gp_file.read()

    # Accept incoming connections and handle requests
    while True:
        conn, addr = s.accept()
        print("Client connected:", addr)

        # Receive the request from the client
        request = conn.recv(1024).decode()

        # Extract the requested path from the request
        path = request.split()[1]

        # Check if the requested path is the main page
        if path == '/':
            # Send the main HTML as the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + main_html
            conn.send(response.encode())

        # Check if the requested path is the Wi-Fi configuration page
        elif path == '/wifi':
            # Send the Wi-Fi HTML as the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + wifi_html
            conn.send(response.encode())

        # Check if the requested path is the TD configuration page
        elif path == '/td':
            # Send the TD HTML as the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + td_html
            conn.send(response.encode())

        # Check if the requested path is the GP configuration page
        elif path == '/gp':
            # Send the GP HTML as the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + gp_html
            conn.send(response.encode())

        # Check if the requested path is the save page for Wi-Fi configuration
        elif path == '/save_wifi':
            # Extract the content from the request
            content_start = request.find('\r\n\r\n') + 4
            content = request[content_start:]

            # Parse the content into a dictionary
            content_dict = {}
            for line in content.split('&'):
                if '=' in line:
                    key, value = line.split('=')
                    content_dict[key] = value

            # Store the Wi-Fi configuration in a text file
            with open('config/wifi_config.txt', 'w') as file:
                file.write(f"wifi_ssid: {content_dict['wifi_ssid']}\n")
                file.write(f"wifi_pw: {content_dict['wifi_pw']}\n")

            # Redirect to the success page
            response = "HTTP/1.1 303 See Other\r\nLocation: /success\r\n\r\n"
            conn.send(response.encode())

        # Check if the requested path is the save page for TD configuration
        elif path == '/save_td':
            # Extract the content from the request
            content_start = request.find('\r\n\r\n') + 4
            content = request[content_start:]

            # Parse the content into a dictionary
            content_dict = {}
            for line in content.split('&'):
                if '=' in line:
                    key, value = line.split('=')
                    content_dict[key] = value
            
            # Store the TD configuration in a text file
            with open('config/td_config.txt', 'w') as file:
                td_url = url_decode(content_dict['td_url'])
                file.write("td_url: {}\n".format(td_url))
                file.write("td_user: {}\n".format(content_dict['td_user']))
                file.write("td_pw: {}\n".format(content_dict['td_pw']))

            # Redirect to the success page
            response = "HTTP/1.1 303 See Other\r\nLocation: /success\r\n\r\n"
            conn.send(response.encode())

        # Check if the requested path is the save page for GP configuration
        elif path == '/save_gp':
            # Extract the content from the request
            content_start = request.find('\r\n\r\n') + 4
            content = request[content_start:]

            # Parse the content into a dictionary
            content_dict = {}
            for line in content.split('&'):
                if '=' in line:
                    key, value = line.split('=')
                    content_dict[key] = value

            # Store the GP configuration in a text file
            with open('config/gp_config.txt', 'w') as file:
                num_led = content_dict.get('num_led', 'default_num_led')
                td_group = content_dict.get('td_group', 'default_td_group')
                file.write(f"num_led: {num_led}\n")
                file.write(f"td_group: {td_group}\n")



            # Redirect to the success page
            response = "HTTP/1.1 303 See Other\r\nLocation: /success\r\n\r\n"
            conn.send(response.encode())

        # Check if the requested path is the success page
        elif path == '/success':
            # Read the contents of the success HTML file
            with open('html/success.html', 'r') as success_file:
                success_html = success_file.read()

            # Send the success HTML as the response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + success_html
            conn.send(response.encode())

        # Check if the requested path is for resetting the ESP
        elif path == '/reset':
            # Reset the ESP
            machine.reset()
            
        # Handle 404 Not Found error for any other paths
        else:
            # Generate the 404 Not Found error message HTML
            html = '''
            <!DOCTYPE html>
            <html>
            <body>
            <h2>404 Not Found</h2>
            <p>The requested page was not found.</p>
            </body>
            </html>
            '''

            # Send the 404 error message as the response
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + html
            conn.send(response.encode())

        # Close the connection
        conn.close()
        
