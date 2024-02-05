import pygame
import pyautogui
import pygetwindow as gw
import time
from Tools.VariableContainer import VariableContainer



def initialize_joystick():
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Controller not found")
        quit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick


def get_button_events(pygame,eel = None):
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            create_key_board_event(event,eel=eel)
        elif event.type == pygame.JOYBUTTONUP:
            print(event)
        elif event.type == pygame.JOYHATMOTION:
            None


def create_key_board_event(event,eel=None):
    '''
    Responsible for Matching the button on the controller with the button on the keyboard.
    '''
    input_event = VariableContainer("input_mapping").data

    actions = {
        input_event["left-mouse"]: lambda: pyautogui.click(button="left"),
        input_event["right-mouse"]: lambda: pyautogui.click(button="right"),
        input_event["open-user-interface"]: lambda: open_main_ui(),
        input_event["GridUp"]: lambda: GridUp(eel),
        input_event["GridDown"]: lambda: GridDown(eel),
        input_event["GridLeft"]: lambda: GridLeft(eel),
        input_event["GridRight"]: lambda: GridRight(eel)
    }

    actions[str(event.button)]()

    handle_complex_hot_key(mapping_data=input_event.data)
            

def get_smoothed_values(alpha, current_values, new_values):
    """
    Smoothed Values: it helps to avoid jittering
    """
    return (
        alpha * new_values[0] + (1 - alpha) * current_values[0],
        alpha * new_values[1] + (1 - alpha) * current_values[1]
    )

def move_mouse(analog_values, current_position):
    velocity = int (VariableContainer("userVariables").data["speed"])

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

def open_main_ui():
    window = gw.getWindowsWithTitle(VariableContainer("userVariables").data["active_window"])[0]
    if window.isMinimized:
        window.restore()
    else:
        window.minimize()
    time.sleep(0.5)

def GridUp(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(0, -userData.data["stepvy"])
    eel.js_arrow_up()

def GridDown(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(0, userData.data["stepvy"])
    #eel.js_arrow_down()

def GridLeft(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(-userData.data["stepvx"], 0)
    #eel.js_arrow_left()

def GridRight(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(userData.data["stepvx"], 0)
    #eel.js_arrow_right()

def handle_complex_hot_key(mapping_data):
    for k in mapping_data.keys():
        if k in mapping_data:
            if '-' in k and len(k.split('-')) >= 2 and k.split('-')[0] != 'left' and k.split('-')[0] != 'right':
                pyautogui.hotkey(*k.split('-'))
            else:
                pyautogui.hotkey(k)