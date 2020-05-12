from time import sleep
import subprocess
import os
import socket

class Dump1090ToPipe: #Leitet Beast-TCP Output auf Pipe um
	retries = 10
	
	def __init__(self, port=30005, host='localhost'):
		self.port = port
		self.host = host
		devnull = open(os.devnull, 'wb')
		curDir = os.getcwd()	#get working directory
		args = (curDir+'/dump1090', '--net')
		self.dump1090process = subprocess.Popen(args, shell=False, stdout=devnull, stderr=devnull)
		sleep(1)
		return
		
	def subprocessAlive(self, exception_queue, exit):
		poll = self.dump1090process.poll()
		if poll != None and poll != 0: # ist 0 richtig?
			exception_queue.put("dump1090toPipe: dump1090 läuft nicht. Bitte manuell testen ob das Programm läuft. Return Code:" + str(poll))
			exit.set()
			return False
		else:
			return True
			
			
	def run(self, pipe_out, exception_queue, exit):
		if not self.subprocessAlive(exception_queue, exit):
			print("MIMIMI")
			return
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			for i in range(Dump1090ToPipe.retries):
				try:
					s.connect((self.host, self.port))
					print(self.dump1090process.communicate()[0])
					break
				except Exception as e:
					if (i == Dump1090ToPipe.retries-1):
						exception_queue.put(["Probleme beim Verbinden mit dump1090-Socket: ", e])
						exit.set()
						break
					else:
						sleep(0.1)
						
			while not(exit.is_set()):
				try:
					data = s.recv(64)
					h = int.from_bytes(data[2:7], byteorder='big')
					pipe_out.send([len(data), data[0], data[1], h, data[8], data[9:].hex()])
					self.subprocessAlive(exception_queue, exit)
				except Exception as e:
					self.dump1090process.kill()
					exception_queue.put(["Probleme beim Empfangen der TCP Beast Messages: ", e])
					exit.set()
			
			s.close()
			return
			    
