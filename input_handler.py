import pygame
import pyautogui

from json_reader import ler_json

def initialize_joystick():
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Nenhum controle encontrado.")
        quit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

def create_key_board_event(event):
    input_data = ler_json("input_mapping.json")
    if input_data["left-mouse"] == str(event.button):
        pyautogui.click(button="left")
    elif input_data["right-mouse"] == str(event.button):
        pyautogui.click(button="right")
    
    for k in input_data.keys():
        if input_data[k] == str(event.button):            
            if '-' in k and len(k.split('-')) >= 2 and k.split('-')[0] != 'left' and k.split('-')[0] != 'right':
                pyautogui.hotkey(*k.split('-'))
            else:
                pyautogui.hotkey(k)
            


def get_button_events(pygame, joystick):
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        elif event.type == pygame.JOYBUTTONUP:
            create_key_board_event(event)
        elif event.type == pygame.JOYHATMOTION:
            None

def get_smoothed_values(alpha, current_values, new_values):
    return (
        alpha * new_values[0] + (1 - alpha) * current_values[0],
        alpha * new_values[1] + (1 - alpha) * current_values[1]
    )

def move_mouse(analog_values, current_position):
    velocity = 10 

    new_x = int(current_position[0] + analog_values[0] * velocity)
    new_y = int(current_position[1] + analog_values[1] * velocity)
    if new_x != 0 or new_y != 0:
        pyautogui.moveTo(new_x, new_y, duration=0.001)

def adjust_values(value, threshold):
    return value if abs(value) >= threshold else 0
       

def move_mouse_with_joystick(joystick, alpha, smoothed_values, threshold,joystick_number = 0,speed = 1):
    x_axis = joystick.get_axis(joystick_number)
    y_axis = joystick.get_axis(joystick_number + 1)

    smoothed_values = get_smoothed_values(alpha, smoothed_values, (x_axis, y_axis))

    analog_x = adjust_values(smoothed_values[0], threshold)
    analog_y = adjust_values(smoothed_values[1], threshold)

    current_mouse_position = pyautogui.position()

    move_mouse((analog_x*speed, analog_y*speed), current_mouse_position)



def move_scroll_with_joystick(joystick, alpha, smoothed_values, threshold,joystick_number = 2):
    x_axis = joystick.get_axis(joystick_number)
    y_axis = joystick.get_axis(joystick_number + 1)

    smoothed_values = get_smoothed_values(alpha, smoothed_values, (x_axis, y_axis))

    analog_x = adjust_values(smoothed_values[0], threshold)
    analog_y = adjust_values(smoothed_values[1], threshold)

    if analog_y != 0:
        pyautogui.scroll(round(analog_y*-20))