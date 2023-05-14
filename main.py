import time
import machine
import query
import led
import setup
import _thread

# Pin number for the button
button_pin = 9

# Variable to store the previous result from get_topdesk_data()
previous_data = None

# Variable to track the setup mode
setup_mode = False

# Function to handle button interrupt
def button_interrupt(pin):
    global setup_mode

    # Disable the button interrupt to avoid multiple triggers
    pin.irq(None)

    # Enter setup mode
    setup_mode = True

    # Start the webpage serving thread
    _thread.start_new_thread(setup.serve_webpage, ())

    # Start the LEDs thread
    _thread.start_new_thread(led.run_leds_up_down, (led.get_num_led(),))

    # Wait for the setup mode to finish
    while setup_mode:
        time.sleep(1)

    # Enable the button interrupt again
    pin.irq(button_interrupt, machine.Pin.IRQ_FALLING)

# Function to check if the button is pressed
def is_button_pressed():
    button = machine.Pin(button_pin, machine.Pin.IN)
    return button.value() == 0

# Configure button pin for interrupt handling
button = machine.Pin(button_pin, machine.Pin.IN)
button.irq(button_interrupt, machine.Pin.IRQ_FALLING)

# Main loop
while True:
    # Check if not in setup mode
    if not setup_mode:
        # Get data from get_topdesk_data()
        data = query.get_topdesk_data()

        # Check if the data has changed
        if data != previous_data:
            previous_data = data

            # Run turn_on_leds() with the new data
            led.turn_on_leds(data)

    # Wait for 1 second
    time.sleep(1)

    # Check if the button is pressed
    if is_button_pressed():
        button_interrupt(button)

    # Wait for 59 more seconds before the next iteration
    time.sleep(59)
