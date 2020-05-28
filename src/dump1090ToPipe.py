from time import sleep, time
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
		args = (curDir+'/dump1090', '--net', '--modeac', '--fix', '--fix', '--gain', '49,6')
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
			startTime = time()		
			while not(exit.is_set()):
				try:
					dataFull = s.recv(4096)
					print("Socket-Packet:" + dataFull.hex())
					dataFull = dataFull.decode('iso-8859-1')
					for data in dataFull.split("\n\n\n"):
					
						
						data.replace(chr(0x1A)*2, chr(0x1A))	#0x1A1A to 0x1A
						data = data.encode('iso-8859-1')
						
						if (len(data) == 0):	#string.split also returns empty strings
							continue
								
						if (len(data) <= 10): 	#Fehlerhaftes Paket Empfangen
							print("Fehlerhaftes Paket von dump1090 empfangen")
							continue
						
						if (data[0] != 0x1A):
							print("Fehler: Paket hat nicht als erstes Byte 0x1A")
							continue	
						
						
						msgType = data[1]
						timeStamp = time() - startTime	#dump1090 liefert falsche Zeitwerte
						signalPower = int.from_bytes(data[2:6],byteorder='big')/(10**5) * (-1)
						if data[6] == 0:
							icao = data[7:10].hex()
						else:
							icao = data[6:10].hex()
							
						msg = data[10:].hex()
						
						if (icao == "000000" and msgType == 49 and signalPower == -21474.83648):
							icao = None
							signalPower = None
						pipe_out.send([msgType, timeStamp, signalPower, icao, msg])
						self.subprocessAlive(exception_queue, exit)
				except Exception as e:
					print("Fehler: " + str(e))
					exception_queue.put(["Probleme beim Empfangen der TCP Beast Messages: ", e])
					exit.set()
			os.killpg(os.getpgid(self.dump1090process.pid), signal.SIGTERM)	#self.dump1090process.terminate() and kill() not working ¯\_(ツ)_/¯
			s.close()
			return
			    
