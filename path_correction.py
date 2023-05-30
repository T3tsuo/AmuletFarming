import os
import pickle
import time
import pyautogui
import pydirectinput
from PIL import Image
import requests

import random_breaks

project_d = os.getcwd()

game_config_dict = {}

fight_option = Image.open(requests.get("https://raw.githubusercontent.com/"
                                       "T3tsuo/AmuletFarming/main/location/fight_option.png", stream=True).raw)


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
            # if there is a Nonetype assignment by accident then continue to try again
            try:
                if pyautogui.locateOnScreen(img, confidence=0.8) is not None:
                    location = pyautogui.locateOnScreen(img, confidence=0.8)
                    pydirectinput.PAUSE = 0.03
                    if compare_diff(game_config_dict["game_xpos"], location[0]) < val - 25:
                        with open("log.txt", "a") as f_temp:
                            print("Going left", file=f_temp)
                        pydirectinput.press("left")
                        time.sleep(random_breaks.input_break())
                    elif compare_diff(game_config_dict["game_xpos"], location[0]) > val + 25:
                        with open("log.txt", "a") as f_temp:
                            print("Going right", file=f_temp)
                        pydirectinput.press("right")
                        time.sleep(random_breaks.input_break())
                    else:
                        with open("log.txt", "a") as f_temp:
                            print("Aligned", file=f_temp)
                        pydirectinput.PAUSE = 0.1
                        break
            except TypeError:
                pass
    else:
        return


def self_align_vertical(img, val):
    if can_align:
        while True:
            # if there is a Nonetype assignment by accident then continue to try again
            try:
                if pyautogui.locateOnScreen(img, confidence=0.8) is not None:
                    location = pyautogui.locateOnScreen(img, confidence=0.8)
                    pydirectinput.PAUSE = 0.03
                    if compare_diff(game_config_dict["game_ypos"], location[1]) < val - 25:
                        with open("log.txt", "a") as f_temp:
                            print("Going up", file=f_temp)
                        pydirectinput.press("up")
                        time.sleep(random_breaks.input_break())
                    elif compare_diff(game_config_dict["game_ypos"], location[1]) > val + 25:
                        with open("log.txt", "a") as f_temp:
                            print("Going down", file=f_temp)
                        pydirectinput.press("down")
                        time.sleep(random_breaks.input_break())
                    else:
                        with open("log.txt", "a") as f_temp:
                            print("Aligned", file=f_temp)
                        pydirectinput.PAUSE = 0.1
                        break
                # if while moving around we got a wild encounter
                elif pyautogui.locateOnScreen(fight_option, confidence=0.8) is not None:
                    # then stop alignment
                    return
            except TypeError:
                pass
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
