import eel
import threading
import App
import Tools.VariableContainer as vbc
import pygetwindow as gw

# Inicializar o Eel
eel.init('web')

# Função que será executada em um thread separado
def loop_python():
    while True:
        App.run()

# Iniciar o loop em um thread separado
thread = threading.Thread(target=loop_python)
thread.daemon = True  # O thread será encerrado quando o programa principal for encerrado
thread.start()

# Expor uma função para o JavaScript (opcional)
@eel.expose
def python_print(param):
    print(f"Python function called with parameter: {param}")

@eel.expose
def get_json_file(param):
    container = vbc.VariableContainer(param)
    return container.data

@eel.expose
def python_set_speed(speed):
    vbc.VariableContainer("userVariables").update_data({"speed": speed})

@eel.expose
def python_get_active_window():
    active_window = gw.getActiveWindowTitle()
    print(active_window)

# Iniciar o aplicativo Eel
eel.start('index.html', size=(800, 500))
