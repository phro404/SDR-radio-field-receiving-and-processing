import multiprocessing
import subprocess
import os
import sys
from time import sleep
import signal
from dump1090ToPipe import Dump1090ToPipe
from socket_client_class import Client_socket
from telegramProcessing import TelegramProcessing
from fileWriter import FileWriter

numPipes = 3

class Handler1:
	def __init__(self):
		self.processes = {} 	#all processes are stored inside here
		self.pipes = []	#all pipes are stored here like: [[pipe1_in, pipe1_out], [pipe2_in, pipe2_out]]
		self.exception_queue = multiprocessing.Queue()
		self.exit = multiprocessing.Event()
		
		for i in range(numPipes):
			self.pipes.append(multiprocessing.Pipe())
					
					
	def run(self, exit, outputQueue):
			
		def stopAllProcesses():
			self.exit.set()
			print("Starting to terminate Processes")
			sleep(0.4)
			for process in self.processes.values():
				process.join()
				
		print("Handler1 started")
		
		socketClientObj = Client_socket()
		self.processes["client_socket"] = multiprocessing.Process(target=socketClientObj.run, args=(self.pipes[1][0], self.exception_queue, self.exit))
		
		dump1090ToPipeObj = Dump1090ToPipe()
		self.processes["dump1090ToPipe"] = multiprocessing.Process(target=dump1090ToPipeObj.run, args=(self.pipes[0][0], self.exception_queue, self.exit))
		
		telegramProcessingObj = TelegramProcessing()
		self.processes["telegramProcessing"] = multiprocessing.Process(target=telegramProcessingObj.run, args=(self.pipes[1][1], self.pipes[0][1], self.pipes[2][0], self.exit))
		
		fileWriterObj = FileWriter()
		self.processes["fileWriter"] = multiprocessing.Process(target=fileWriterObj.run, args=(self.pipes[2][1], self.exit))
		
		
		
		for process in self.processes.values():
			process.start()
		print("All Processes of Handler1 started")
		sleep(1)
		while not exit.is_set():
			#outputQueue.put("Handler1 Loop start")
			allAlive = True
			#while (self.pipes[2][1].poll()):
			#	print(self.pipes[2][1].recv())
			for key in self.processes.keys():
				if(not self.processes[key].is_alive()):
					outputQueue.put("Stopped Running: " + key)
					allAlive = False
					
			if(not allAlive):
				outputQueue.put("Handler: Child Process stopped working")
				exit.set()
				outputQueue.put("Here's the exception_queue:")
				while(not self.exception_queue.empty()):
					outputQueue.put(self.exception_queue.get())
					outputQueue.put("\n")
			sleep(0.1)
			
			#outputQueue.put("Loop End")
			
		stopAllProcesses()
		outputQueue.put("Handler1 stopped")	
		
		
		
		
