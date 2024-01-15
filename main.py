import pygame
import sys
import pyautogui

from input_handler import *

def main():
    pygame.init()

    joystick = initialize_joystick()

    alpha = 0.9
    smoothed_values = (0, 0)
    threshold = 0.05
    speed = 1
    input_data = ler_json("input_mapping.json")

    while True:
        
        move_mouse_with_joystick(joystick, alpha, smoothed_values, threshold)
        move_scroll_with_joystick(joystick, alpha, smoothed_values, threshold)

        get_button_events(pygame, joystick)

if __name__ == "__main__":
    main()
