import pygame
import pyautogui

from input_handler import *
from Tools.VariableContainer import VariableContainer

pyautogui.FAILSAFE = False


#This version of the app works without user interface.
#It is used for debugging purposes.
def run():
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

        get_button_events(pygame)


run()