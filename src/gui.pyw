#!/usr/bin/python3

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import handler
import multiprocessing
from time import sleep
from visualization import visualization

class Userinterface:
	"""Build the GUI and link its buttons with functions"""
	
	def __init__(self):
		"""Create the graphical user interface and distribute it to the screen"""
		self.window = tk.Tk()
		self.window.title("radio-field-measurement")
		self.window.geometry("900x500")
		
		self.exit = multiprocessing.Event()	#used to exit the handler.run() function
		self.handlerProcess = None	#Variable in which a Handler1-process reference is stored

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

	def visualizeFiles(self):   
		"""Open a file-explorer window and pass the choosen filepaths to visualization"""
		unorderedList = filedialog.askopenfilenames(initialdir = "../data", title = "Select files", filetypes = (("csv files", "*.csv"), ("pdf files", "*.pdf"), ("all files", "*.*")))
		file_path = self.orderPathList(unorderedList)
		if (file_path != 0):
			visualization(file_path, False)
			
	def startHandler1Daemon(self):
		"""Starts the Handler1.run() subprocess and disables the 2 upper buttons. The exit button remains uneffected"""
		self.first_button.config(state=tk.DISABLED, bg = "black")
		self.second_button.config(state=tk.DISABLED, bg = "black")
		main1 = handler.Handler1()
		self.handlerProcess = multiprocessing.Process(target=main1.run, args=[self.exit])
		self.handlerProcess.start()
	
	def closeAll(self):
		"""Disables all buttons. Sets self.exit, which leads to the handler1 process shutting down. After shutting it down the GUI closes itself"""
		self.first_button.config(state=tk.DISABLED, bg = "black")
		self.second_button.config(state=tk.DISABLED, bg = "black")
		self.third_button.config(state=tk.DISABLED, bg = "black")
		sleep(0.2)
		self.exit.set()
		if (self.handlerProcess != None):
			self.handlerProcess.join()
		self.window.quit() #closes whole programm
		
			
	def loop(self):
		"""Recursive loop which checks if the Handler1 process is closed. If it is, self.closeall() is called"""
		self.window.after(100, self.loop)
		if (self.exit.is_set()):
			print("Gui exit")			
			self.closeAll()
			
	def orderPathList(self, unorderedList):
		"""Check a list of filepaths for plausibility and swap its elements into a specific order.
		
		Arguments:
		unorderedList (list of strings) -- contains a list of filepaths 
		
		Returns:
		orderedList (list of strings) -- contains the same filepaths as unordered list, but in a specific order
		"""
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
gui.window.after(100, gui.loop)	#gui.loop now starts looping
gui.window.mainloop()

