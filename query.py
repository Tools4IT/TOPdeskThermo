import network
import urequests
import ujson

def get_topdesk_data():
    # Read WiFi configuration from file
    with open("config/wifi_config.txt") as f:
        wifi_config = dict(line.strip().split(": ") for line in f)

    # Read Topdesk configuration from file
    with open("config/td_config.txt") as f:
        td_config = dict(line.strip().split(": ") for line in f)

    # Read group configuration from file
    with open("config/gp_config.txt") as f:
        group_config = dict(line.strip().split(": ") for line in f)

    # WiFi connection settings
    ssid = wifi_config.get("wifi_ssid")
    password = wifi_config.get("wifi_pw")

    # Topdesk API settings
    topdesk_username = td_config.get("td_user")
    topdesk_password = td_config.get("td_pw")
    topdesk_url = td_config.get("td_url")

    # Group configuration
    group = group_config.get("td_group")

    # Connect to WiFi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    # Wait until connected to WiFi
    while not wifi.isconnected():
        pass

    print("Connected to WiFi")

    # Topdesk API request settings
    base_url = "{}/tas/api/incidents".format(topdesk_url)
    query_params = {
        'query': "closed==false;completed==false;operatorGroup.name=sw={}".format(group),
        'fields': 'id',
        'pageSize': '100'
    }

    # Construct the query string
    query_string = "query={}&fields={}&pageSize={}".format(
        query_params['query'],
        query_params['fields'],
        query_params['pageSize']
    )
    # print("Query string:", query_string)
    url = "{}?{}".format(base_url, query_string)

    # print("url:", url)

    auth = (topdesk_username, topdesk_password)

    try:
        # Send the GET request with basic authentication
        response = urequests.get(url, auth=auth)

        # Check the response status code
        if 200 <= response.status_code <= 210:
            print("responsecode:", response.status_code)
            data = response.json()
            # Do something with the data
            # print("Response data:", data)
            return len(data)  # Return the size of the response data array
        elif response.status_code == 400:
            error_content = response.content.decode('utf-8')
            error_data = ujson.loads(error_content)
            error_message = error_data.get('errors', [{}])[0].get('errorMessage', 'Unknown error')
            print("Error 400 - Bad Request:")
            print("Error message:", error_message)
            print("Response content:", error_content)
        else:
            print("Error:", response.status_code)

    except Exception as e:
        print("An error occurred:", e)

    # Disconnect from WiFi
    wifi.disconnect()
    wifi.active(False)

    print("Disconnected from WiFi")

# Call the function and print the return value
result = get_topdesk_data()
print("Size of response data array:", result)
