import os
import pickle
import time
import pyautogui
import pydirectinput

import random_breaks

project_d = os.getcwd()

game_config_dict = {}


def get_config(path, project_d):
    os.chdir(path)
    with open("main.properties", "r") as txt_file:
        properties = txt_file.readlines()
        for i in range(len(properties)):
            if "client.graphics.xpos=" in properties[i]:
                game_config_dict.update({"game_xpos": int(properties[i].replace("\n", "").replace("client.graphics"
                                                                                                  ".xpos=", ""))})
                os.chdir(project_d)
            if "client.graphics.ypos=" in properties[i]:
                game_config_dict.update({"game_ypos": int(properties[i].replace("\n", "").replace("client.graphics"
                                                                                                  ".ypos=", ""))})
                os.chdir(project_d)
            if "client.graphics.width=" in properties[i]:
                game_config_dict.update({"game_width": int(properties[i].replace("\n", "").replace("client.graphics"
                                                                                                   ".width=", ""))})
                os.chdir(project_d)
            if "client.graphics.height=" in properties[i]:
                game_config_dict.update({"game_height": int(properties[i].replace("\n", "").replace("client.graphics"
                                                                                                    ".height=", ""))})
                os.chdir(project_d)


def compare_diff(x1, x2):
    return abs(x1 - x2)


def self_align_side(img, val):
    if can_align:
        while True:
            if pyautogui.locateOnScreen(img, confidence=0.8) is not None:
                location = pyautogui.locateOnScreen(img, confidence=0.8)
                pydirectinput.PAUSE = 0.03
                if compare_diff(game_config_dict["game_xpos"], location[0]) < val - 25:
                    print("Going left")
                    pydirectinput.press("left")
                    time.sleep(random_breaks.input_break())
                elif compare_diff(game_config_dict["game_xpos"], location[0]) > val + 25:
                    print("Going right")
                    pydirectinput.press("right")
                    time.sleep(random_breaks.input_break())
                else:
                    print("Aligned")
                    pydirectinput.PAUSE = 0.1
                    break
    else:
        return


def get_game_pos_size():
    return game_config_dict


if os.path.isfile("game_path.dat"):
    path = pickle.load(open("game_path.dat", "rb"))
    get_config(path, project_d)
    can_align = True
else:
    can_align = False
