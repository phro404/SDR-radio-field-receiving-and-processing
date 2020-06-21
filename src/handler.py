import multiprocessing
import subprocess
import os
import sys
from time import sleep
import signal
from dump1090ToPipe import Dump1090ToPipe
from socket_client import Client_socket
from telegramProcessing import TelegramProcessing
from fileWriter import FileWriter

numPipes = 3	#Amount of pipes required

class Handler1:
	def __init__(self):
		"""Init method of Handler1"""
		self.processes = {} 	#all processes are stored inside here
		self.pipes = []	#all pipes are stored here like this: [[pipe1_in, pipe1_out], [pipe2_in, pipe2_out], [pipe3_in, pipe3_out]]
		self.exit = multiprocessing.Event()	#used to enable every subprocess to close whole program in case of an error
		
		for i in range(numPipes):
			self.pipes.append(multiprocessing.Pipe())
					
					
	def run(self, exit):
		"""Initialization of every subprocess. Inside of a loop it is checked, whether every subprocess is running. If not, every subprocess is closed and the programm closes itself.
		
		Parameters:
			exit: Used to enable this method to tell gui.py if the whole programm should be closed and vice versa"""
			
		def stopAllProcesses():
			"""Closes every subprocess"""
			self.exit.set() 	#The parameter of every while-loop inside every run-method of every subprocess is now not false. Subprocesses will now begin to stop
			print("Handler1: Starting to terminate all subprocesses")
			sleep(0.4)
			for process in self.processes.values():
				process.join()
				
		print("Handler1: starting every subprocess...")
		
		socketClientObj = Client_socket()
		self.processes["client_socket"] = multiprocessing.Process(target=socketClientObj.run, args=(self.pipes[1][0], self.exit))
		
		dump1090ToPipeObj = Dump1090ToPipe()
		self.processes["dump1090ToPipe"] = multiprocessing.Process(target=dump1090ToPipeObj.run, args=(self.pipes[0][0], self.exit))
		
		telegramProcessingObj = TelegramProcessing()
		self.processes["telegramProcessing"] = multiprocessing.Process(target=telegramProcessingObj.run, args=(self.pipes[1][1], self.pipes[0][1], self.pipes[2][0], self.exit))
		
		fileWriterObj = FileWriter()
		self.processes["fileWriter"] = multiprocessing.Process(target=fileWriterObj.run, args=(self.pipes[2][1], self.exit))
		
		
		
		for process in self.processes.values():
			process.start()	#starts every subprocess
		print("Handler1: All subprocesses started")
		sleep(1)
		while not exit.is_set():	#Loop until gui.py sets exit or it is set, due to a subprocess failing
			allAlive = True
			for key in self.processes.keys():
				if(not self.processes[key].is_alive()):
					outputQueue.put("Handler1: A subprocess stopped running: " + key)
					allAlive = False
					
			if(not allAlive):
				exit.set() 	#Stopping the while loop
			sleep(0.1)
						
		stopAllProcesses()
		print("Handler1: Stopped")	
		
		
		
		
