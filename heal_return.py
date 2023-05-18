import time

import pyautogui
import pydirectinput
import requests
from PIL import Image

import random_breaks
from path_correction import self_align_side


outside_building = Image.open(requests.get("https://raw.githubusercontent.com/"
                                           "T3tsuo/AmuletFarming/main/location/outside_building.png", stream=True).raw)

sign_fence = Image.open(requests.get("https://raw.githubusercontent.com/"
                                     "T3tsuo/AmuletFarming/main/location/sign_fence.png", stream=True).raw)


outside_building_align_val = 686
sign_fence_align_val = 161


def leave_building():
    pydirectinput.keyDown("down")
    time.sleep(random_breaks.leave_building())
    pydirectinput.keyUp("down")
    # while cannot find outside, keep on waiting
    is_outside = False
    while is_outside is False:
        # if image recognition detects that we left the building
        if pyautogui.locateOnScreen(outside_building, confidence=0.8) is not None:
            # then we are outside
            with open("log.txt", "a") as f_temp:
                print("Left Building", file=f_temp)
            is_outside = True
            time.sleep(0.5)
        else:
            time.sleep(0.5)


def go_to_grass():
    # hop on bike
    pydirectinput.press("1")
    with open("log.txt", "a") as f_temp:
        print("Bicycle", file=f_temp)
    time.sleep(random_breaks.input_break())
    # go left
    pydirectinput.keyDown("left")
    time.sleep(random_breaks.three_blocks())
    pydirectinput.keyUp("left")
    time.sleep(random_breaks.input_break())
    # check if aligned
    self_align_side(outside_building, outside_building_align_val)
    # go down
    pydirectinput.keyDown("down")
    time.sleep(random_breaks.eleven_blocks())
    pydirectinput.keyUp("down")
    time.sleep(random_breaks.input_break())
    # go right
    pydirectinput.keyDown("right")
    time.sleep(random_breaks.seven_blocks())
    pydirectinput.keyUp("right")
    time.sleep(random_breaks.input_break())
    # check if aligned
    self_align_side(sign_fence, sign_fence_align_val)
    # look down
    pydirectinput.press("down")
    time.sleep(random_breaks.input_break())
    # use cut
    pydirectinput.keyDown("z")
    time.sleep(random_breaks.use_cut_break())
    pydirectinput.keyUp("z")
    time.sleep(random_breaks.input_break())
    # go to grass
    pydirectinput.keyDown("down")
    time.sleep(random_breaks.to_grass_break())
    pydirectinput.keyUp("down")
    with open("log.txt", "a") as f_temp:
        print("At Grass", file=f_temp)
    time.sleep(random_breaks.paying_attention_break())


def run():
    leave_building()
    go_to_grass()
