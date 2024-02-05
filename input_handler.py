import pygame
import pyautogui
import pygetwindow as gw
import time
from Tools.VariableContainer import VariableContainer
from pywinauto import Desktop



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
        input_event["left-mouse"]: lambda: confirmation_key(eel),
        input_event["right-mouse"]: lambda: pyautogui.click(button="right"),
        input_event["open-user-interface"]: lambda: open_main_ui(eel),
        input_event["GridUp"]: lambda: GridUp(eel),
        input_event["GridDown"]: lambda: GridDown(eel),
        input_event["GridLeft"]: lambda: GridLeft(eel),
        input_event["GridRight"]: lambda: GridRight(eel),
        input_event["esc"]: lambda: pyautogui.hotkey('esc'),
        input_event["left-browser-tab"]: lambda: left_browser_tab(),
        input_event["right-browser-tab"]: lambda: right_browser_tab()
    }

    actions[str(event.button)]()
    time.sleep(0.01)


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

def open_main_ui(eel = None):
    window = gw.getWindowsWithTitle(VariableContainer("userVariables").data["active_window"])[0]
    if window.isMinimized:
        window.restore()
        VariableContainer("userVariables").update_data({"is_app_open": True})
    else:
        window.minimize()
        VariableContainer("userVariables").update_data({"is_app_open": False})
    

def GridUp(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(0, -userData.data["stepvy"])
    eel.js_select_screen_ui("up")

def GridDown(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(0, userData.data["stepvy"])
    eel.js_select_screen_ui("down")

def GridLeft(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(-userData.data["stepvx"], 0)
    #eel.js_arrow_left()

def GridRight(eel):
    userData = VariableContainer("userVariables")
    pyautogui.move(userData.data["stepvx"], 0)
    #eel.js_arrow_right()

def left_browser_tab():
    k = "ctrl-shift-tab"
    pyautogui.hotkey(*k.split('-'))

def right_browser_tab():
    k = "ctrl-tab"
    pyautogui.hotkey(*k.split('-'))

def confirmation_key(eel):
    ui_mode = 0
    if is_app_open():
        if ui_mode == 0:
            eel.js_get_screen_selected()(lambda x: open_window(x))
            
    else:
        pyautogui.click(button="left")

def is_app_open():
    return VariableContainer("userVariables").data["is_app_open"]


def open_window(titulo_da_janela):
    try:
        # Tente encontrar a janela pelo título
        janela = Desktop(backend="uia").window(title=titulo_da_janela)
        
        # Verifique se a janela foi encontrada
        if janela.exists():
            # Restaure a janela se ela estiver minimizada
            if janela.is_minimized():
                janela.restore()
            # Traz a janela para a frente
            janela.set_focus()
        else:
            print(f"Janela com o título '{titulo_da_janela}' não encontrada.")
    except Exception as e:
        print(f"Erro ao tentar encontrar a janela: {e}")
    
    open_main_ui(eel = None)
    