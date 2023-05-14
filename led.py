import time
import neopixel
import machine

def get_num_led():
    # Read the config file
    with open('config/gp_config.txt', 'r') as file:
        config_data = file.readlines()

    # Search for the line containing the number of LEDs
    for line in config_data:
        if line.startswith('num_led:'):
            num_led = int(line.split(':')[1].strip())
            return num_led

    # Return a default value if the number of LEDs is not found
    return 0

def turn_on_leds(num_to_turn_on):
    # Get the number of LEDs from the config file
    num_led = get_num_led()

    # Define the pin number for the NeoPixel strip
    pixel_pin = 10

    # Initialize the NeoPixel strip with the number of LEDs
    strip = neopixel.NeoPixel(machine.Pin(pixel_pin), num_led)

    # Set the maximum brightness to 50% (128 out of 255)
    max_brightness = 75

    # Turn off all LEDs initially
    strip.fill((0, 0, 0))
    strip.write()

    # Check if the number to turn on exceeds the number of LEDs
    if num_to_turn_on > num_led:
        # Turn on all LEDs and set them to red with reduced brightness
        strip.fill((max_brightness, 0, 0))
    else:
        # Calculate the number of LEDs for each color
        num_blue = min(num_to_turn_on, num_led // 3)
        num_green = min(num_to_turn_on - num_blue, num_led // 3)
        num_orange = min(num_to_turn_on - num_blue - num_green, num_led // 3)

        # Set the color and brightness of the LEDs
        for i in range(num_blue):
            strip[i] = (0, 0, max_brightness)  # Blue

        for i in range(num_blue, num_blue + num_green):
            strip[i] = (0, max_brightness, 0)  # Green

        for i in range(num_blue + num_green, num_blue + num_green + num_orange):
            strip[i] = (max_brightness, int(max_brightness * 0.65), 0)  # Orange

    # Update the LED strip to show the changes
    strip.write()


def run_leds_up_down(num_leds):
    pin = machine.Pin(10, machine.Pin.OUT)
    np = neopixel.NeoPixel(pin, num_leds)

    # Set the maximum brightness to 75% (191 out of 255)
    max_brightness = 75

    while True:
        # Run LEDs up
        for i in range(num_leds - 1):
            np.fill((max_brightness, 0, 0))  # Set all LEDs to red with reduced brightness
            np[i] = (0, 0, 0)  # Turn off current LED
            np[i + 1] = (max_brightness, 0, 0)  # Turn on next LED
            np.write()
            time.sleep(0.1)

        # Run LEDs down
        for i in range(num_leds - 1, 0, -1):
            np.fill((max_brightness, 0, 0))  # Set all LEDs to red with reduced brightness
            np[i] = (0, 0, 0)  # Turn off current LED
            np[i - 1] = (max_brightness, 0, 0)  # Turn on previous LED
            np.write()
            time.sleep(0.1)

