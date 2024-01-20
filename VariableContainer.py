import json
import os

class VariableContainer:
    def __init__(self, container_name):
        self.name = container_name
        self._data = {}

        self.create_container(self.name)

    def create_container(self, name):
        if not os.path.exists(f"{name}.json"):
            json.dump({}, open(f"{name}.json", "w"))
        else:
            # Se o arquivo já existe, carregue os dados para o dicionário _data
            with open(f"{name}.json", "r") as file:
                self._data = json.load(file)

    @property
    def data(self):
        return self._data

    def _update_data(self, new_data):
        self._data = new_data
        self.save_data()

    def save_data(self):
        with open(f"{self.name}.json", "w") as file:
            json.dump(self._data, file)

    def update_data(self, new_data):
        current_data = self._data.copy()
        current_data.update(new_data)
        self._update_data(current_data)


