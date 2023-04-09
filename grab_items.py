import time
import pyautogui
import pydirectinput
from random import random
from PIL import Image
import requests

import random_breaks

stole_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                    "T3tsuo/AmuletFarming/main/battle_logs/stole.png", stream=True).raw)

flinched_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                       "T3tsuo/AmuletFarming/main/battle_logs/flinched.png", stream=True).raw)

banette_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                      "T3tsuo/AmuletFarming/main/location/banette.png", stream=True).raw)

frisked_meowth_png = Image.open(requests.get("https://raw.githubusercontent.com/T3tsuo/AmuletFarming/main/"
                                             "battle_logs/frisked_meowth.png", stream=True).raw)

shiny_png = Image.open(requests.get("https://raw.githubusercontent.com/"
                                    "T3tsuo/AmuletFarming/main/battle_logs/shiny_pokemon.png", stream=True).raw)

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


def heal_up():
    at_nurse = False
    # we are not at nurse yet
    while at_nurse is False:
        # once we are at the nurse
        if pyautogui.locateOnScreen(inside_building, confidence=0.8) is not None:
            # then set flag to true, so we can talk to the nurse
            print("At Nurse")
            at_nurse = True
            time.sleep(0.5)
        else:
            time.sleep(0.5)

    # talk through dialogue
    print("Talking to Nurse")
    pydirectinput.keyDown("z")
    time.sleep(random_breaks.heal_up_break())
    pydirectinput.keyUp("z")
    print("Healing Done")
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
        print("Fight")
        time.sleep(random_breaks.paying_attention_break())
        # press thief (first move)
        location = pyautogui.locateOnScreen(thief_move,
                                            confidence=0.8)
        pyautogui.moveTo(location.left + random() * location.width,
                         location.top + random() * location.height)
        pydirectinput.click()
        print("Thief")
        time.sleep(random_breaks.paying_attention_break())
        # select and attack specific pokemon
        which_to_attack(select_pokemon)
        # if pokemon flinches
        flinched = False
        # if there is a shiny
        isShiny = False
        # wait for entire attack break while checking if thief took an item
        turn_done = False
        while turn_done is False:
            # if turn is done
            if pyautogui.locateOnScreen(fight_option, confidence=0.8) is not None:
                turn_done = True
            # if shiny is found
            if pyautogui.locateOnScreen(shiny_png, confidence=0.8) is not None:
                isShiny = True
                print("Shiny Found")
            # if item is found
            if pyautogui.locateOnScreen(stole_png, confidence=0.8) is not None and not isShiny and turn_done:
                print("Stole item")
                # return that item was found
                return True
            if pyautogui.locateOnScreen(flinched_png, confidence=0.8) is not None:
                flinched = True
                print("Flinched")
            if pyautogui.locateOnScreen(battle_done, confidence=0.8) is not None:
                print("Horde is dead")
                # if item was stolen
                if pyautogui.locateOnScreen(stole_png, confidence=0.8) is not None:
                    print("Stole item")
                    return True
                else:
                    # return that item was not found
                    return False
        while isShiny:
            run_away()
        if not flinched:
            select_pokemon += 1
    return False


def which_to_attack(n):
    print("SELECT #" + str(n + 1))
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
    location = pyautogui.locateOnScreen(run_option,
                                        confidence=0.8)
    pyautogui.moveTo(location.left + random() * location.width,
                     location.top + random() * location.height)
    pydirectinput.click()
    print("Run Away")
    time.sleep(random_breaks.paying_attention_break())
    while True:
        if pyautogui.locateOnScreen(battle_done, confidence=0.8) is not None:
            break
        else:
            time.sleep(0.1)


def teleport_away():
    # press teleport
    pydirectinput.press('5')
    print("Teleport")
    time.sleep(random_breaks.paying_attention_break())


def in_battle():
    # keep on checking until we are in battle
    while True:
        # check if we can fight yet
        if pyautogui.locateOnScreen(fight_option, confidence=0.8) is not None:
            break
        else:
            time.sleep(0.1)
    # once we can fight, check if we found item
    if pyautogui.locateOnScreen(frisked_meowth_png) is not None:
        print("Found item")
        time.sleep(2)
        # switch to attacking stage
        took_item = thief()
        # switch to run away the pokemons if battle isn't done
        if pyautogui.locateOnScreen(battle_done, confidence=0.8) is None:
            run_away()
        print("Battle End")
        # found item but return if we took the item
        return True, took_item
    # did not find any items on pokemon so did not take it
    return False, False


def take_item():
    item_taken = False
    while item_taken is False:
        if pyautogui.locateOnScreen(banette_png, confidence=0.8) is not None:
            # grab location of image
            location = pyautogui.locateOnScreen(banette_png, confidence=0.8)
            # click randomly on the box
            pyautogui.moveTo(location.left + random() * location.width, location.top + random() * location.height)
            pydirectinput.click()
            print("Quagsire Selected")
            # user paying attention reaction time
            time.sleep(random_breaks.paying_attention_break())
            while item_taken is False:
                # do the same thing for amulet coin
                if pyautogui.locateOnScreen(amulet_png, confidence=0.8):
                    location = pyautogui.locateOnScreen(amulet_png,
                                                        confidence=0.8)
                    print("Taking Amulet Coin")
                    pyautogui.moveTo(location.left + random() * location.width,
                                     location.top + random() * location.height)
                    pydirectinput.click()
                    item_taken = True
                    time.sleep(random_breaks.paying_attention_break())
                elif pyautogui.locateOnScreen(quick_claw_png, confidence=0.8):
                    # same thing for quick claw
                    location = pyautogui.locateOnScreen(quick_claw_png,
                                                        confidence=0.8)
                    print("Taking Quick Claw")
                    pyautogui.moveTo(location.left + random() * location.width,
                                     location.top + random() * location.height)
                    pydirectinput.click()
                    item_taken = True
                    time.sleep(random_breaks.paying_attention_break())


def run(x):
    for i in range(x):
        # use sweet scent
        pydirectinput.press('4')
        print("Sweet Scent")
        # check if item was found and if it was it will try to get it and return if it did or didn't
        found_item, took_item = in_battle()
        # if you did not find the item nor stole it, means that thief failed so run if the battle is done
        if not found_item and not took_item:
            print("Not found")
            # run away if battle isn't done
            if pyautogui.locateOnScreen(battle_done, confidence=0.8) is None:
                # run away from battle
                run_away()
        elif found_item and took_item:
            # if item is stolen then take it off of your pokemon
            take_item()
    # when all of sweet scent is used then leave to pokecenter
    teleport_away()
    # then heal up
    heal_up()
