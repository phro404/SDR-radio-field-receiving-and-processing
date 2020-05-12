import multiprocessing
import subprocess
import os
import sys
from time import sleep
import signal
from dump1090ToPipe import Dump1090ToPipe

numPipes = 1
	
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
		dump1090ToPipeObj = Dump1090ToPipe()
		self.processes["dump1090ToPipe"] = multiprocessing.Process(target=dump1090ToPipeObj.run, args=(self.pipes[0][0], self.exception_queue, self.exit))
		for process in self.processes.values():
			process.start()
		sleep(2)
		while not exit.is_set():
			outputQueue.put("Loop start")
			allAlive = True
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
			
			if(self.pipes[0][1].poll()):
				outputQueue.put(self.pipes[0][1].recv())
			outputQueue.put("Loop End")
			
		stopAllProcesses()
		outputQueue.put("Handler1 stopped")	
		
		
		
		
