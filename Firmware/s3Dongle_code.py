print("Starting Dongle...")
import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.split import Split, SplitSide, SplitType 

keyboard = KMKKeyboard()

# Dongle Config:

split = Split(
    split_side=SplitSide.DONGLE,
    split_type=SplitType.ESP_NOW,
)

keyboard.modules.append(split)

# Defining that the dongle has no keys

keyboard.col_pins = []
keyboard.row_pins = []
keyboard.diode_orientation = 0

keyboard.keymap = [[KC.NO]]

if __name__ == "__main__":
    keyboard.go()