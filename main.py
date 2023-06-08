import time

import pyautogui as pag

# could use pag.locateonscreen or opencv, 
# which allows for confidence on if image is there

# if you have a click from point a to point b, look at human mouse movements
# from there interpolate to simulate human movement

# additionally, any sleeps should have variance of ~10ms

def main():
    # print("hello")
    # Initialized PyAutoGUI
    pag.FAILSAFE = True

    # Timer
    print("Starting")
    for i in range(10):
        print(".")
        time.sleep(.5)
    print('go')
    pressKey('a', 1)

    print("Done")

def pressKey(key, sec=1):
    pag.keyDown(key)
    time.sleep(sec)
    pag.keyUp(key)


def initializePyAutoGUI():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pag.FAILSAFE = True

if __name__ == "__main__":
    main()
