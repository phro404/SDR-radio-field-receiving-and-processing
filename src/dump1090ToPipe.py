from time import sleep
import subprocess
import os
import socket
import signal

#Die Pipe gibt Listen aus mit dem Inhalt:
#[0]: 49(AC), 50(SS), 51(SL)
#[1]: Timestamp in Sekunden
#[2]: Signal-Pegel
#[3]: ICAO Addresse
#[4]: Telegramm in Hex

class Dump1090ToPipe: #Leitet Beast-TCP Output auf Pipe um
	retries = 10 #Maximum TCP Connecting Retries
	
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
					if (len(data) <= 16): 	#Fehlerhaftes Paket Empfangen
						print("Fehlerhaftes Paket von dump1090 empfangen")
						continue
					msgType = data[1]
					timeStamp = int.from_bytes(data[2:8],byteorder='big') / (10**7)
					signalPower = int.from_bytes(data[8:12],byteorder='big')/(10**5) * (-1)
					if data[12] == 0:
						icao = data[13:16].hex()
					else:
						icao = data[12:16].hex()
					msg = data[16:].hex()
					
					pipe_out.send([msgType, timeStamp, signalPower, icao, msg])
					
					self.subprocessAlive(exception_queue, exit)
				except Exception as e:
					print("Fehler: " + str(e))
					exception_queue.put(["Probleme beim Empfangen der TCP Beast Messages: ", e])
					exit.set()
			os.killpg(os.getpgid(self.dump1090process.pid), signal.SIGTERM)	#self.dump1090process.terminate() and kill() not working ¯\_(ツ)_/¯
			s.close()
			return
			    
