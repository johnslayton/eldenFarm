from pynput import mouse, keyboard
from time import time
import json
import os

# Fields
mouse_listener = None
start_time = None
unreleased_keys = [] # use set here
input_events = []


def main():
    print("Go")
    runListeners()


# Keyboard Monitoring
def on_press(key):
    try:
        print('alphanumeric key {} pressed'.format(key.char))
    except AttributeError:
        print('special key {} pressed'.format(key))

def on_release(key):
    print('{} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Mouse Monitoring
def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
def runListeners():


        # Collect mouse input events
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
    mouse_listener.start()
    mouse_listener.wait()  # wait for the listener to become ready

    # Collect keyboard inputs until released
    # https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    with keyboard.Listener(
            on_press=on_press, 
            on_release=on_release) as listener:
        global start_time
        start_time = time()
        listener.join()
    # with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    #     listener.join()
    # # Listen for input from mouse and keyboard
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()

if __name__ == "__main__":
    main()
