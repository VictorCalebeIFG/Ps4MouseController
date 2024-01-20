import pygame
import pyautogui

from input_handler import *
from json_reader import read_json
from VariableContainer import VariableContainer

pyautogui.FAILSAFE = False

def main():
    pygame.init()
    size = pyautogui.size()

    joystick = initialize_joystick()

    userVariables = VariableContainer("userVariables")

    alpha = userVariables.data["alpha"]
    threshold = userVariables.data["threshold"]
    

    userVariables.update_data({"stepvx":int(size.width/userVariables.data["stepdx"])})
    userVariables.update_data({"stepvy":int(size.height/userVariables.data["stepdy"])})
    
    smoothed_values = (0, 0)

    while True:
        
        move_mouse_with_joystick(joystick, alpha, smoothed_values, threshold)
        move_scroll_with_joystick(joystick, alpha, smoothed_values, threshold)

        get_button_events(pygame, joystick)

if __name__ == "__main__":
    main()
