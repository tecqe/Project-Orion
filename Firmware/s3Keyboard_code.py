#Make sure you have kmk, OLED libraries, neopixe.mpy, simpleio.py, and adafruit_displayio_sh1107.mpy in your lib folder
print("Starting Keyboard...")
import boardimport digitalio
import analogio
import busio
import displayio
import terminalio
import time 
from adafruit_display_text import label
import adafruit_displayio_sh1107

# KMK Imports
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.extensions.pegasus_rgb import PegasusRGB
from kmk.scaners import Scanner

# HARDWARE PIN DEFINITIONS 

PIN_ANALOG_SWITCH = board.IO2

PIN_NEOPIXEL = board.IO48

PIN_SR_LATCH = board.IO10
PIN_SR_CLK = board.IO12
PIN_SR_DATA = board.IO13

ROW_PINS = [board.IO4, board.IO5, board.IO6 board.IO7, board.IO15, board.IO16]

PIN_I2C_SDA = board.IO8
PIN_I2C_SCL = board.IO9

PIN_BAT_SENS = board.IO1
PIN_THERM_SENS = board.IO1

PIN_MISCSW1 = board.IO42
PIN_MISCSW2 = board.IO41

PIN_RE_A = board.IO21
PIN_RE_B = board.IO38

PIN_ENBST = board.IO17
PIN_INOKB = board.IO18


# SHIFT REGISTER SCANNER 

class ShiftRegisterMatrix(Scanner):
    def __init__(self, row_pins, clock_pin, data_pin, latch_pin, bot_count=16):

        self.rows = []
        for pin in row_pins:
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = True 
            self.rows.appent(p)

            self.clk = digitalio.DigitalInOut(clock_pin)
            self.clk.direction = digitalio.Direction.OUTPUT

            self.data = digitalio.DigitalInOut(data_pin)
            self.data.direction = digitalio.Direction.INPUT
            # pins have pull-up resistors on board

            self.latch digitalio.DigitalInOut(latch_pin)
            self.latch.direction = digitalio.Direction.OUTPUT
            self.latch.value = True

            self.bit_count = bit_count

        def scan(self, keyboard):
            pressed_keys = []
        
        for col_ifx, in range(self.bit_count):
            # 0 = pressed, 1 = not pressed
            if not self.data.value:
                key.index = (row_inx * self.bit_count) + col_idx
                pressed_keys.append(key_index)

            self.clk.value = True
            self.clk.value = False

        row_pin.value = True

        return pressed_keys
    
# CONNECTION MODE LOGIC 

def get_connection_mode():
    try:
        with analogio.AnalogIn(PIN_ANALOG_SWITCH) as adc:
            #Average readings for stability 
            val = sum([adc.value for _ in range(10)]) / 10

            if val < 8000:
                return "DONGLE"
            elif val 8000 <= val < 45000:
                return "BLUETOOTH"
            elif val >= 45000:
                return "WIRED"
            
        except Exception as e:
            print(f"Error reading analog pin, deafulting to WIRED mode: {e}")
            return "WIRED"

current_mode = get_connection_mode()
print(f"Detected mode: {current_mode}")

# OLED SETUP

displayio.release_displays()

i2c = busio.I2C(scl=board.IO9, sda=board.IO8, frequency=1000000)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

display = adafruit_displayio_sh1107.SH1107(
    display_bus,
    width=128,
    height=128,
    rotation=0 # prob gonna have to change this later
)
splash = displayio.Group()
display.show(splash)

# OLED TEXT (FOR TESTING)
text_area = label.Label(
    terminalio.FONT,
    text"= f"Mode: {current_mode}",
    color=0xFFFFFF,
    x=10,
    y=64,
    scale=2
)

splash.append(text_area)

# KEYBOARD AND KMK SETUP
keyboard = KMKKeyboard()

# matrix
keyboard.matrix = ShiftRegisterMatrix(row_pins=ROW_PINS, clock_pin=PIN_SR_CLK, data_pin=PIN_SR_DATA, latch_pin=PIN_SR_LATCH, bit_count=16)

# split/connection setup
if current_mode == "DONGLE":
    split = Split(
        split_side = SplitSide.KEYBOARD,
        split_type = SplitType.ESP_NOW,
        split_target_left=False # This keyboard is the "right" half of the split 
    )
    keyboard.modules.append(split)

else: #wired
    pass

rgb = PegasusRGB(
    pixel_pin=PIN_NEOPIXEL,
    num_pixels=83,
    hue_default=170,
    sat_default=255,
    val_default=100,
    val_deafult=100,
    val_limit=150,
    rgb_order="(1, 0 2)"
)
keyboard.extensions.append(rgb)

keyboard.keymap = [
    [KC.A for _ in range(96)] # Sets all keys to A for testing 
]

if __name__ == '__main__':
    keyboard.go()