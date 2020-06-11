#!/usr/bin/python3

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import handler
import multiprocessing
from time import sleep
from visualization import visualization
from debug import plnw

class Userinterface:
	
	def __init__(self):
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
									command = self.visualizeFiles)

		self.third_button = tk.Button(self.window, text = "Exit", relief = tk.RAISED, width = 25, height = 5, bg = "red", 
									fg = "black", font = ("15"), command = self.closeAll)

		#link buttons with gui-window
		self.first_button.place(relx = 0.1, rely = 0.14, relwidth = 0.370, relheight = 0.3)
		self.second_button.place(relx = 0.53, rely = 0.14, relwidth = 0.370, relheight = 0.3)
		self.third_button.place(relx = 0.1, rely = 0.54, relwidth = 0.8, relheight = 0.3)
			
		plnw(0)


	def visualizeFiles(self):   #method for second button, opens the file-explorer
		unorderedList = filedialog.askopenfilenames(initialdir = "../data", title = "Select files", filetypes = (("csv files", "*.csv"), ("pdf files", "*.pdf"), ("all files", "*.*")))
		file_path = self.orderPathList(unorderedList)
		if (file_path != 0):
			visualization(file_path, False)
			
	def startHandler1Daemon(self):	 #method for first button, is supposed to be the link to the first main-process
		self.first_button.config(state=tk.DISABLED, bg = "black")
		self.second_button.config(state=tk.DISABLED, bg = "black")
		plnw(2)
		main1 = handler.Handler1()
		self.handlerProcess = multiprocessing.Process(target=main1.run, args=(self.exit, self.outputQueue))
		self.handlerProcess.start()
		#self.outputQueue.put("Button 1 Pressed")
	
	def closeAll(self):
		self.first_button.config(state=tk.DISABLED, bg = "black")
		self.second_button.config(state=tk.DISABLED, bg = "black")
		self.third_button.config(state=tk.DISABLED, bg = "black")
		plnw(3)
		sleep(0.2)
		self.exit.set()
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
			print("Gui exit")			
			self.closeAll()
			
	def orderPathList(self, unorderedList):
		if ((len(unorderedList) < 2) or len(unorderedList) % 2 == 1):   #to few or an odd number of files had been selected
			 tk.messagebox.showinfo("Error", "Wrong data selection, please pick again.")
			 return 0
		orderedList = []
		foundflag = 0
		for  i in range(0, 24):
			for j in unorderedList:
				if (-1 != j.rfind("_lvl_reply")):   #rfind returns '-1' if element is not found
					tempindex = j.rfind("_lvl_reply")   #rfind returns position in string if sub-string is found 

					#generating string for hour-search
					if(i < 10):
						tempstr = "0" + str(i)
					else:
						tempstr = str(i)

					if(-1 != j.rfind(tempstr, (tempindex - 2))):   #checking hour
						orderedList.append(j)

						#searching for matching amp_hist file element by element
						for k in unorderedList:
							if (-1 != k.rfind("_amp_hist")):
								tempindex = k.rfind("_amp_hist")
								if(-1 != k.rfind(tempstr, (tempindex - 2))):
									orderedList.append(k)
									foundflag = 1
									break

						if (foundflag == 0):	#no matching amp_hist file found in whole list
							tk.messagebox.showinfo("Error", "Wrong data selection, please pick again.")
							return 0
						else:
							foundflag = 0
		return orderedList
		
gui = Userinterface()
sleep(1)
plnw(1)
gui.window.after(100, gui.loop)
gui.window.mainloop()


