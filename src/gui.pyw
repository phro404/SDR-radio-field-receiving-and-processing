import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import handler
import multiprocessing
from time import sleep

class Userinterface:
	
	def __init__(self):
		#initialize attributes
		self.__file_path="None"

		#initalize gui-window
		self.window = tk.Tk()
		self.window.title("radio-field-measurement")
		self.window.geometry("900x500")
		
		self.exit = multiprocessing.Event() #used to exit the handler.run() Funktion
		self.handlerProcess = None #Processin which the handler.run() loop runs
		self.outputQueue = multiprocessing.Queue()

		#initalize buttons
		self.first_button = tk.Button(self.window, text = "Start measurement", relief = tk.RAISED, bg = "blue",
									fg = "black", font = ("15"), command = self.startHandler1Daemon)

		self.second_button = tk.Button(self.window, text = "Plot from data", relief = tk.RAISED, width = 25, 
									height = 5, bg = "blue", fg = "black", font = ("15"),
									command = self.__openexplorer_button_action__)

		self.third_button = tk.Button(self.window, text = "Exit", relief = tk.RAISED, width = 25, height = 5, bg = "red", 
									fg = "black", font = ("15"), command = self.closeAll)

		#link buttons with gui-window
		self.first_button.place(relx = 0.1, rely = 0.14, relwidth = 0.370, relheight = 0.3)
		self.second_button.place(relx = 0.53, rely = 0.14, relwidth = 0.370, relheight = 0.3)
		self.third_button.place(relx = 0.1, rely = 0.54, relwidth = 0.8, relheight = 0.3)

		#self.window.mainloop()  #forces the gui to stay opened, but lets the __init__-method never end


	def __openexplorer_button_action__(self):   #method for second button, opens the file-explorer
		self.__file_path = filedialog.askopenfilenames()

	def startHandler1Daemon(self):	 #method for first button, is supposed to be the link to the first main-process
		main1 = handler.Handler1()
		self.handlerProcess = multiprocessing.Process(target=main1.run, args=(self.exit, self.outputQueue))
		self.handlerProcess.start()
		#self.outputQueue.put("Button 1 Pressed")
	  
	def get_file_path(self):	#get-method for file path
		return self.__file_path
		
	def closeAll(self):
		self.first_button.config(state=tk.DISABLED, bg = "black")
		self.second_button.config(state=tk.DISABLED, bg = "black")
		self.third_button.config(state=tk.DISABLED, bg = "black")
		self.exit.set()	
		sleep(0.2)
		self.getOutput()		
		if (self.handlerProcess != None):
			self.handlerProcess.join()
		self.getOutput()
		self.window.quit() #closes whole programm
		
	def getOutput(self):
		if not self.outputQueue.empty():
			print(self.outputQueue.get())
			
	def loop(self):
		self.window.after(100, self.loop)
		self.getOutput()
		if (self.exit.is_set()):			
			self.closeAll()
		
gui = Userinterface()
gui.window.after(100, gui.loop)
gui.window.mainloop()


