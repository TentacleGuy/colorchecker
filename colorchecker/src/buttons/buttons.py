from gpiozero import Button
from time import sleep

class ButtonHandler:
    def __init__(self, capture_pin, next_pin, prev_pin):
        self.capture_button = Button(capture_pin)
        self.next_button = Button(next_pin)
        self.prev_button = Button(prev_pin)

        self.capture_button.when_pressed = self.capture
        self.next_button.when_pressed = self.next
        self.prev_button.when_pressed = self.previous

    def capture(self):
        print("Capture button pressed.")
        # Implement capture logic here

    def next(self):
        print("Next button pressed.")
        # Implement logic to go to the next item here

    def previous(self):
        print("Previous button pressed.")
        # Implement logic to go to the previous item here

    def debounce(self, func, *args, **kwargs):
        # Implement debounce logic here
        pass

    def long_press(self, func, *args, **kwargs):
        # Implement long press logic here
        pass

# Example usage
if __name__ == "__main__":
    handler = ButtonHandler(capture_pin=17, next_pin=27, prev_pin=22)
    while True:
        sleep(0.1)  # Keep the script running to listen for button presses