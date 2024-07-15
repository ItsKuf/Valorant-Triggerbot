import json
import time
import threading
import keyboard
import sys
import win32api
from ctypes import WinDLL
import numpy as np
from mss import mss as mss_module


def exiting():
    # Exit the program gracefully
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()
        except:
            raise SystemExit


# Load Windows libraries
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

# Set DPI awareness
shcore.SetProcessDpiAwareness(2)

# Get screen dimensions
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Define the zone to capture around the center of the screen
ZONE = 5
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE),
    int(HEIGHT / 2 - ZONE),
    int(WIDTH / 2 + ZONE),
    int(HEIGHT / 2 + ZONE),
)


class Triggerbot:
    def __init__(self):
        self.sct = mss_module()
        self.triggerbot = False
        self.triggerbot_toggle = True
        self.exit_program = False 
        self.toggle_lock = threading.Lock()

        # Load configuration
        with open('config.json') as json_file:
            data = json.load(json_file)

        try:
            self.trigger_hotkey = int(data["trigger_hotkey"], 16)
            self.always_enabled = data["always_enabled"]
            self.trigger_delay = data["trigger_delay"]
            self.base_delay = data["base_delay"]
            self.color_tolerance = data["color_tolerance"]
            self.R, self.G, self.B = (250, 100, 250)  # target color (purple)
        except:
            exiting()

    def cooldown(self):
        # Cooldown period after toggling triggerbot
        time.sleep(0.1)
        with self.toggle_lock:
            self.triggerbot_toggle = True
            # Play different beeps based on triggerbot state
            if self.triggerbot:
                kernel32.Beep(440, 75)
                kernel32.Beep(700, 100)
            else:
                kernel32.Beep(440, 75)
                kernel32.Beep(200, 100)

    def searcherino(self):
        # Capture the screen and search for the target color
        img = np.array(self.sct.grab(GRAB_ZONE))
        pixels = img.reshape(-1, 4)
        
        color_mask = (
            (pixels[:, 0] > self.R - self.color_tolerance) & (pixels[:, 0] < self.R + self.color_tolerance) &
            (pixels[:, 1] > self.G - self.color_tolerance) & (pixels[:, 1] < self.G + self.color_tolerance) &
            (pixels[:, 2] > self.B - self.color_tolerance) & (pixels[:, 2] < self.B + self.color_tolerance)
        )
        matching_pixels = pixels[color_mask]
        
        if self.triggerbot and len(matching_pixels) > 0:
            delay_percentage = self.trigger_delay / 100.0  
            actual_delay = self.base_delay + self.base_delay * delay_percentage
            time.sleep(actual_delay)
            keyboard.press_and_release("k")

    def toggle(self):
        # Toggle the triggerbot on/off
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.triggerbot_toggle:
                    self.triggerbot = not self.triggerbot
                    print(self.triggerbot)
                    self.triggerbot_toggle = False
                    threading.Thread(target=self.cooldown).start()

        # Exit the program if the specific keybind is pressed
        if keyboard.is_pressed("ctrl+shift+x"):
            self.exit_program = True
            exiting()
        
    def hold(self):
        # Continuously check if the hotkey is pressed
        while True:
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True
                self.searcherino()
            else:
                time.sleep(0.1)
            if keyboard.is_pressed("ctrl+shift+x"):
                self.exit_program = True
                exiting()

    def starterino(self):
        # Main loop to run the triggerbot
        while not self.exit_program:
            if self.always_enabled:
                self.toggle()
                if self.triggerbot:
                    self.searcherino()
                else:
                    time.sleep(0.1)
            else:
                self.hold()


# Start the triggerbot
Triggerbot().starterino()
