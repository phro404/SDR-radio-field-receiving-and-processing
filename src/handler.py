import multiprocessing
import subprocess
import os
import sys
import time
import signal
from tcpToPipe import TcpToPipe

numPipes = 1
	
class Handler1:

	def __init__(self):
		self.processes = {} 	#all processes are stored inside here
		self.pipes = []	#all pipes are stored here like: [[pipe1_in, pipe1_out], [pipe2_in, pipe2_out]]
		self.exception_queue = multiprocessing.Queue()
		
		for i in range(numPipes):
			self.pipes.append(multiprocessing.Pipe())
					
		tcpToPipeObj = TcpToPipe(self.pipes[0][0], self.exception_queue)
		self.processes["tcpToPipe"] = multiprocessing.Process(target=tcpToPipeObj.run)
		
		devnull = open(os.devnull, 'wb')
		curDir = os.getcwd()	#get working directory
		args = (curDir+'/dump1090', '--net')
		self.dump1090process = subprocess.Popen(args, shell=False, stdout=devnull, stderr=devnull)
				
		
	def shutdown(self):
		for process in self.processes.values():
			process.terminate()
		for process in self.processes.values():
			process.join()
		self.dump1090process.kill()
	
				
	def closeall(self, signal):
		print("Keyboard Interrupt")
		self.shutdown()
		sys.exit(0)
		
		
	def run(self):
		for process in self.processes.values():
			process.start()
		time.sleep(2)
		while True:
			allAlive = True
			for key in self.processes.keys():
				if(not self.processes[key].is_alive()):
					print("Stopped Running: " + key)
					allAlive = False
			if(self.dump1090process.poll() != None):
				print("Stopped Running: dump1090")
				allAlive = False	
					
			if(not allAlive):
				self.shutdown()
				print("Something went wrong")
				sys.exit(1)
			time.sleep(0.1)
			
			if(self.pipes[0][1].poll()):
				print(self.pipes[0][1].recv())
		
		
		
		
		
		
