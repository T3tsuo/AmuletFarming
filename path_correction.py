import os
import pickle
import time
import pyautogui
import pydirectinput

import random_breaks

project_d = os.getcwd()

game_config_dict = {"game_xpos": ""}


def get_config(path, project_d):
    os.chdir(path)
    with open("main.properties", "r") as txt_file:
        properties = txt_file.readlines()
        for i in range(len(properties)):
            if "client.graphics.xpos=" in properties[i]:
                game_config_dict["game_xpos"] = properties[i].replace("\n", "").replace("client.graphics.xpos=", "")
                os.chdir(project_d)
                return


def compare_diff(x1, x2):
    return abs(x1 - x2)


def self_align_side(img, val):
    if can_align:
        while True:
            if pyautogui.locateOnScreen(img, confidence=0.8) is not None:
                location = pyautogui.locateOnScreen(img, confidence=0.8)
                pydirectinput.PAUSE = 0.03
                if compare_diff(int(game_config_dict["game_xpos"]), location[0]) < val - 25:
                    print("Going left")
                    pydirectinput.press("left")
                    time.sleep(random_breaks.input_break())
                elif compare_diff(int(game_config_dict["game_xpos"]), location[0]) > val + 25:
                    print("Going right")
                    pydirectinput.press("right")
                    time.sleep(random_breaks.input_break())
                else:
                    print("Aligned")
                    pydirectinput.PAUSE = 0.1
                    break
    else:
        return


if os.path.isfile("game_path.dat"):
    path = pickle.load(open("game_path.dat", "rb"))
    get_config(path, project_d)
    can_align = True
else:
    can_align = False
