import eel
import threading
import App

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
def python_function_from_js(param):
    print(f"Python function called with parameter: {param}")

# Iniciar o aplicativo Eel
eel.start('index.html', size=(800, 600))
