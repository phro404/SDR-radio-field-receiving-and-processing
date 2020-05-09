import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Userinterface:
    
    def __init__(self):
        #initialize attributes
        self.__file_path="None"

        #initalize gui-window
        self.window = tk.Tk()
        self.window.title("radio-field-measurement")
        self.window.geometry("900x500")

        #initalize buttons
        self.first_button = tk.Button(self.window, text = "Start measurement", relief = tk.RAISED, bg = "blue",
                                    fg = "black", font = ("15"), command = self.callBack)

        self.second_button = tk.Button(self.window, text = "Plot from data", relief = tk.RAISED, width = 25, 
                                    height = 5, bg = "blue", fg = "black", font = ("15"),
                                    command = self.__openexplorer_button_action__)

        self.third_button = tk.Button(self.window, text = "Exit", relief = tk.RAISED, width = 25, height = 5, bg = "red", 
                                    fg = "black", font = ("15"), command = self.window.quit)

        #link buttons with gui-window
        self.first_button.place(relx = 0.1, rely = 0.14, relwidth = 0.370, relheight = 0.3)
        self.second_button.place(relx = 0.53, rely = 0.14, relwidth = 0.370, relheight = 0.3)
        self.third_button.place(relx = 0.1, rely = 0.54, relwidth = 0.8, relheight = 0.3)

        self.window.mainloop()  #forces the gui to stay opened, but lets the __init__-method never end


    def __openexplorer_button_action__(self):   #method for second button, opens the file-explorer
        self.__file_path = filedialog.askopenfilenames()

    def callBack(self):     #method for first button, is supposed to be the link to the first main-process
        tk.messagebox.showinfo( "Lorem ipsum dolor sit amet,", "consectetur adipisici elit,")   #just a dummy
        #TODO: insert code here
      
    def get_file_path(self):    #get-method for file path
        return self.__file_path
