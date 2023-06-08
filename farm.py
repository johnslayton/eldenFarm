import pydirectinput
from time import sleep, time
import os
import json
import sys
from PIL import ImageGrab

works = True
def main():
    
    initializepydirectinput()
    countdownTimer()
    #TODO print out how many souls farmed each time
    start_time = time()
    for i in range(50):
        playActions("farm3.json")
        sleep(6.75)
        sleep(1)
        minutes = (time() - start_time) // 60
        seconds = (time() - start_time) % 60
        print("Time elapsed: {} minutes and {:.2f} seconds\n".format(minutes, seconds), flush=True)
    print("Done", flush=True)
    minutes = (time() - start_time) // 60
    seconds = (time() - start_time) % 60

def runesPerHour(runes, time):
    per_second = runes/time
    per_hour = (per_second * 60 * 60)
    return per_hour


def initializepydirectinput():
    # Initialized pydirectinput
    # https://pydirectinput.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pydirectinput.FAILSAFE = True


def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        sleep(.5)
    print("Go")


def grabRunes(coords):
    im=ImageGrab.grab(bbox=(coords[0],coords[1],coords[2],coords[3]))
    # im.show()

    # to file
    im.save('images\\runes.png')

    img = cv2.imread('images\\runes.png')

    text = pytesseract.image_to_string(img, config='--psm 6')
    return text


def playActions(filename):
    # Read the file
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    script_dir = application_path
    # script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir, 
        'recordings', 
        filename
    )
    with open(filepath, 'r') as jsonfile:
        # parse the json
        data = json.load(jsonfile)
        
        # loop over each action
        # Because we are not waiting any time before executing the first action, any delay before the initial
        # action is recorded will not be reflected in the playback.
        for index, action in enumerate(data):
            action_start_time = time()

            # look for escape input to exit
            if action['button'] == 'Key.esc':
                break

            # perform the action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pydirectinput.keyDown(key)
                # print("keyDown on {}".format(key))
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pydirectinput.keyUp(key)
                # print("keyUp on {}".format(key))
            elif action['type'] == 'click':
                pydirectinput.click(action['pos'][0], action['pos'][1], duration=0.25)
                # print("click on {}".format(action['pos']))

            # then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                # this was the last action in the list
                break
            elapsed_time = next_action['time'] - action['time']

            # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
            if elapsed_time < 0:
                raise Exception('Unexpected action ordering.')

            # adjust elapsed_time to account for our code taking time to run
            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            # print('sleeping for {}'.format(elapsed_time))
            sleep(elapsed_time)
    jsonfile.close()


# convert pynput button keys into pydirectinput keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pydirectinput.readthedocs.io/en/latest/keyboard.html
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()