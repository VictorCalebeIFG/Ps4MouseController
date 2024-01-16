import customtkinter
from PIL import Image
from keyboard_mapping_data import keys
from json_reader import ler_json
import os

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        mapping_data = ler_json("input_mapping.json")

        folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images")

        incons_path = ["cross.png","circle.png","square.png","triangle.png"]
        
        tk_imagens = []
        for i in range(len(incons_path)):
            tk_imagens.append(customtkinter.CTkImage(Image.open(os.path.join(folder_path, incons_path[i])), size=(26, 26)))
            self.label = customtkinter.CTkLabel(self,image=tk_imagens[i],text="")
            self.label.grid(row=i, column=0, padx=0,pady=5)

            
        tk_option_menu = []
        for i in range(len(incons_path)):
            aux = customtkinter.CTkOptionMenu(self, values=keys,
                                                command=self.combobox_callback,
                                                )
            tk_option_menu.append(aux)
            tk_option_menu[i].grid(row=i, column=1, padx=0,pady=5)
        
        for k in mapping_data.keys():
            button = mapping_data[k]
            for i in range(len(tk_option_menu)):
                if str(i) == button:
                    tk_option_menu[i].set(k)

    

    def combobox_callback(widget,choice):
        print("combobox dropdown clicked:", choice)

        


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


app = App()
app.mainloop()