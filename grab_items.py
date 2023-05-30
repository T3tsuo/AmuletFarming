import sys
import time
import os
import pickle
import pyautogui
import pydirectinput
from random import random
from PIL import Image
import requests

import random_breaks
from shiny_notify import ping_mail, check_mail_acc
from battle_log_config import two_log_region
from path_correction import self_align_vertical

stole_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                    "T3tsuo/AmuletFarming/main/battle_logs/stole.png", stream=True).raw)

flinched_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                       "T3tsuo/AmuletFarming/main/battle_logs/flinched.png", stream=True).raw)

banette_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                      "T3tsuo/AmuletFarming/main/location/banette.png", stream=True).raw)

frisked_meowth_png = Image.open(requests.get("https://raw.githubusercontent.com/T3tsuo/AmuletFarming/main/"
                                             "battle_logs/frisked_meowth.png", stream=True).raw)

inside_building = Image.open(requests.get("https://raw.githubusercontent.com/"
                                          "T3tsuo/AmuletFarming/main/location/inside_building.png", stream=True).raw)

battle_done = Image.open(requests.get("https://raw.githubusercontent.com/"
                                      "T3tsuo/AmuletFarming/main/location/battle_done.png", stream=True).raw)

amulet_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                     "T3tsuo/AmuletFarming/main/location/take_amulet.png", stream=True).raw)

quick_claw_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                         "T3tsuo/AmuletFarming/main/location/take_quick_claw.png", stream=True).raw)

fight_option = Image.open(requests.get("https://raw.githubusercontent.com/"
                                       "T3tsuo/AmuletFarming/main/location/fight_option.png", stream=True).raw)

run_option = Image.open(requests.get("https://raw.githubusercontent.com/"
                                     "T3tsuo/AmuletFarming/main/location/run_option.png", stream=True).raw)

thief_move = Image.open(requests.get("https://raw.githubusercontent.com/"
                                     "T3tsuo/AmuletFarming/main/location/thief_move.png", stream=True).raw)

shiny_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                    "T3tsuo/AmuletFarming/main/location/shiny_pokemon.png", stream=True).raw)

at_grass_align_val = 148

if os.path.isfile("email.dat"):
    google_email = pickle.load(open("email.dat", "rb"))

if os.path.isfile("mail_password.dat"):
    mail_password = pickle.load(open("mail_password.dat", "rb"))


def heal_up():
    at_nurse = False
    # we are not at nurse yet
    while at_nurse is False:
        # once we are at the nurse
        if pyautogui.locateOnScreen(inside_building, confidence=0.8) is not None:
            # then set flag to true, so we can talk to the nurse
            with open("log.txt", "a") as f_temp:
                print("At Nurse", file=f_temp)
            at_nurse = True
            time.sleep(0.5)
        else:
            time.sleep(0.5)

    # talk through dialogue
    with open("log.txt", "a") as f_temp:
        print("Talking to Nurse", file=f_temp)
    pydirectinput.keyDown("z")
    time.sleep(random_breaks.heal_up_break())
    pydirectinput.keyUp("z")
    with open("log.txt", "a") as f_temp:
        print("Healing Done", file=f_temp)
    # break
    time.sleep(random_breaks.input_break())


def thief():
    # counter to keep track of which pokemon is currently selected
    select_pokemon = 0
    # while the item is not found, and we still have not attacked all 5 pokemons
    while select_pokemon < 3:
        # click fight
        location = pyautogui.locateOnScreen(fight_option,
                                            confidence=0.8)
        pyautogui.moveTo(location.left + random() * location.width,
                         location.top + random() * location.height)
        pydirectinput.click()
        with open("log.txt", "a") as f_temp:
            print("Fight", file=f_temp)
        time.sleep(random_breaks.paying_attention_break())
        # press thief (first move)
        location = pyautogui.locateOnScreen(thief_move,
                                            confidence=0.8)
        pyautogui.moveTo(location.left + random() * location.width,
                         location.top + random() * location.height)
        pydirectinput.click()
        with open("log.txt", "a") as f_temp:
            print("Thief", file=f_temp)
        time.sleep(random_breaks.paying_attention_break())
        # select and attack specific pokemon
        which_to_attack(select_pokemon)
        # if we stole the item
        stole_item = False
        # if pokemon flinches
        flinched = False
        # wait for entire attack break while checking if thief took an item
        turn_done = False
        while turn_done is False:
            # if turn is done
            if pyautogui.locateOnScreen(fight_option, confidence=0.8) is not None:
                turn_done = True
            # if item is found
            if pyautogui.locateOnScreen(stole_png, confidence=0.8, region=two_log_region()) \
                    is not None and stole_item is False:
                with open("log.txt", "a") as f_temp:
                    print("Stole item", file=f_temp)
                stole_item = True
            if pyautogui.locateOnScreen(flinched_png, confidence=0.8, region=two_log_region()) is not None:
                flinched = True
                with open("log.txt", "a") as f_temp:
                    print("Flinched", file=f_temp)
            if pyautogui.locateOnScreen(battle_done, confidence=0.8) is not None:
                with open("log.txt", "a") as f_temp:
                    print("Horde is dead", file=f_temp)
                # if item was stolen
                if pyautogui.locateOnScreen(stole_png, confidence=0.8) is not None:
                    with open("log.txt", "a") as f_temp:
                        print("Stole item", file=f_temp)
                    return True
                else:
                    # return that item was not found
                    return False
        time.sleep(random_breaks.input_break())
        if stole_item:
            # return that item was found
            return True
        if not flinched:
            select_pokemon += 1
    return False


def which_to_attack(n):
    with open("log.txt", "a") as f_temp:
        print("SELECT #" + str(n + 1), file=f_temp)
    if n == 0:
        # select the second pokemon
        pydirectinput.press("z")
        time.sleep(random_breaks.paying_attention_break())
    elif n == 1:
        # go down to select the third pokemon
        pydirectinput.press('right')
        time.sleep(random_breaks.paying_attention_break())
        # select it
        pydirectinput.press("z")
        time.sleep(random_breaks.paying_attention_break())
    elif n == 2:
        # go down to select the fourth pokemon
        pydirectinput.press('right')
        time.sleep(random_breaks.paying_attention_break())
        pydirectinput.press('right')
        time.sleep(random_breaks.paying_attention_break())
        # select it
        pydirectinput.press("z")
        time.sleep(random_breaks.paying_attention_break())


def run_away():
    while True:
        if pyautogui.locateOnScreen(run_option, confidence=0.8) is not None:
            location = pyautogui.locateOnScreen(run_option,
                                                confidence=0.8)
            pyautogui.moveTo(location.left + random() * location.width,
                             location.top + random() * location.height)
            pydirectinput.click()
            with open("log.txt", "a") as f_temp:
                print("Run Away", file=f_temp)
        elif pyautogui.locateOnScreen(battle_done, confidence=0.8) is not None:
            # ran away successfully
            time.sleep(random_breaks.input_break())
            break
        else:
            time.sleep(0.1)


def teleport_away():
    # press teleport
    pydirectinput.press('5')
    with open("log.txt", "a") as f_temp:
        print("Teleport", file=f_temp)
    time.sleep(random_breaks.paying_attention_break())


def in_battle():
    global google_email, mail_password
    # keep on checking until we are in battle
    while True:
        # check if we can fight yet
        if pyautogui.locateOnScreen(fight_option, confidence=0.8) is not None:
            time.sleep(random_breaks.input_break())
            break
        else:
            time.sleep(0.1)
    # check shiny
    if pyautogui.locateOnScreen(shiny_png, confidence=0.8) is not None:
        if check_mail_acc():
            ping_mail(google_email, mail_password, "SHINY FOUND")
        sys.exit(0)
    # once we can fight, check if we found item
    elif pyautogui.locateOnScreen(frisked_meowth_png, region=two_log_region()) is not None:
        with open("log.txt", "a") as f_temp:
            print("Found item", file=f_temp)
        # switch to attacking stage
        took_item = thief()
        # switch to run away the pokemons if battle isn't done
        if pyautogui.locateOnScreen(battle_done, confidence=0.8) is None:
            run_away()
        with open("log.txt", "a") as f_temp:
            print("Battle End", file=f_temp)
        # found item and if we took it then take it from our pokemon
        if took_item:
            take_item()
    else:
        # did not find any items on pokemon so did not take it
        with open("log.txt", "a") as f_temp:
            print("Not found", file=f_temp)
        run_away()


def take_item():
    item_taken = False
    while item_taken is False:
        if pyautogui.locateOnScreen(banette_png, confidence=0.8) is not None:
            # grab location of image
            location = pyautogui.locateOnScreen(banette_png, confidence=0.8)
            # click randomly on the box
            pyautogui.moveTo(location.left + random() * location.width, location.top + random() * location.height)
            pydirectinput.click()
            with open("log.txt", "a") as f_temp:
                print("Banette Selected", file=f_temp)
            # user paying attention reaction time
            time.sleep(random_breaks.paying_attention_break())
            while item_taken is False:
                # do the same thing for amulet coin
                if pyautogui.locateOnScreen(amulet_png, confidence=0.8):
                    location = pyautogui.locateOnScreen(amulet_png,
                                                        confidence=0.8)
                    with open("log.txt", "a") as f_temp:
                        print("Taking Amulet Coin", file=f_temp)
                    pyautogui.moveTo(location.left + random() * location.width,
                                     location.top + random() * location.height)
                    pydirectinput.click()
                    item_taken = True
                    time.sleep(random_breaks.paying_attention_break())
                elif pyautogui.locateOnScreen(quick_claw_png, confidence=0.8):
                    # same thing for quick claw
                    location = pyautogui.locateOnScreen(quick_claw_png,
                                                        confidence=0.8)
                    with open("log.txt", "a") as f_temp:
                        print("Taking Quick Claw", file=f_temp)
                    pyautogui.moveTo(location.left + random() * location.width,
                                     location.top + random() * location.height)
                    pydirectinput.click()
                    item_taken = True
                    time.sleep(random_breaks.paying_attention_break())


def check_if_battle_and_aligned():
    time.sleep(3)
    # checking alignment
    with open("log.txt", "a") as f_temp:
        print("Align Check", file=f_temp)
    self_align_vertical(battle_done, at_grass_align_val)
    # checking if we are in battle
    if pyautogui.locateOnScreen(battle_done, confidence=0.8) is None:
        with open("log.txt", "a") as f_temp:
            print("In Battle", file=f_temp)
        in_battle()


def run(x):
    # check if we are in grass and fix ourselves while caring for wild encounters
    check_if_battle_and_aligned()
    for i in range(x):
        # use sweet scent
        pydirectinput.press('4')
        with open("log.txt", "a") as f_temp:
            print("Sweet Scent", file=f_temp)
        # check if item was found and if it was it will try to get it and if not then run away
        in_battle()
    # when all of sweet scent is used then leave to pokecenter
    teleport_away()
    # then heal up
    heal_up()
