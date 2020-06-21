from time import sleep, time
import subprocess
import os
import socket
import signal

#Out-pipe-packages contain:
#[0]: 49(AC), 50(SS), 51(SL) (integer containing the telegram-type)
#[1]: timestamp in seconds
#[2]: signal-power
#[3]: ICAO address
#[4]: telegramm-payload in hex

class Dump1090ToPipe:
	"""Takes the TCP-output from the dump1090 binary file and puts all important into a pipe."""
	retries = 10 #maximum TCP Connecting Retries
	
	def __init__(self, port=30005, host='localhost'):
		"""Initializes a dump1090 process. The port and host argument are used to connect to the TCP-socket of dump1090.
	
		Parameters:
			port: Port which is used to cannect to dump1090's socket
			host: IP-address of dump1090's socket			
		"""
		self.port = port
		self.host = host
		devnull = open(os.devnull, 'wb')
		curDir = os.getcwd()	#get working directory
		args = (curDir+'/dump1090', '--net', '--modeac', '--fix', '--fix', '--gain', ' 49,6')
		self.dump1090process = subprocess.Popen(args, shell=False, stdout=devnull, stderr=devnull)
		
	def checkDump1090Running(self, exit):
		"""Returns True if a dump1090 process is running on the local machine. Otherwise returns False and sets the exit variable, leading to a shutdown of the programm.
		
		Parameters:
			exit: Used to close whole programm if set"""		
		stdout = subprocess.check_output(['pgrep', 'dump1090'])
		if len(stdout) == 0:
			print("dump1090ToPipe: dump1090 not running anymore. Starting to close the programm")
			exit.set()
			return False
		else:
			return True
					
	def run(self, pipe_out, exit):
		"""The main loop of dump1090ToPipe. First it tries to connect to the dump1090 socket. If this is successfull, as long as "exit" is not set, the programm will receive dump1090 packets,
		interpret them and forward them via pipe
		
		Parameters:
			pipe_out: Pipe used to pipe-out information
			exit: Used to close whole programm if set"""
		sleep(1)
		if not self.checkDump1090Running(exit):
			print("dump1090ToPipe: dump1090 closed itself immediately")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			for i in range(Dump1090ToPipe.retries):
				try:
					s.connect((self.host, self.port))
					print("dump1090ToPipe: Connected to dump1090 socket")
					break
				except Exception as e:
					if (i == Dump1090ToPipe.retries-1):
						print("dump1090ToPipe: Could not connect to dump1090 socket. Is your SDR connected? Error: "+ str(e))
						exit.set()
						break
					else:
						sleep(0.1)
			startTime = time()
			while not(exit.is_set()):
				try:
					dataFull = s.recv(1024)	#Receive dump1090 packets
					dataFull = dataFull.decode('iso-8859-1')
					
					if len(dataFull) < 3:
						self.checkDump1090Running(exit)
					
					for data in dataFull.split("\n\n\n"):	#All dump1090 telegram-packtes are seperated by 3x newline symbols
						data.replace(chr(0x1A)*2, chr(0x1A))	#since "0x1A" is send as "0x1A0x1A" -> revert this
						data = data.encode('iso-8859-1')
						
						if (len(data) == 0):	#string.split() also returns empty strings
							continue
						if (len(data) <= 10): 	#The packet received is shorter than expected 
							if (data != '\n'):
								print("dump1090ToPipe: Packet received is broken. Packet: " + str(repr(data)))
							continue
						if (data[0] != 0x1A):	#All packets must begin with '0x1A', otherwise they are broken
							data = data[1:]	#It is possible that a newline symbol is inserted at the very beginning of the packet. Checking if this is the problem
							if (data[0] != 0x1A):
								print("dump1090ToPipe: Error! First Byte of dump1090 packet not 0x1A. Packet: " + str(repr(data)))
								continue
						
						msgType = data[1]
						timeStamp = time() - startTime	#dump1090 return false timestamps. Creating own ones
						signalPower = int.from_bytes(data[2:6],byteorder='big')/(10**5) * (-1)
						if data[6] == 0:
							icao = data[7:10].hex()
						else:
							icao = data[6:10].hex()
							
						msg = data[10:].hex()
						
						if (msgType != 49):				#Calibration of ModeS signalpower
							signalPower = signalPower - 50
							
						pipe_out.send([msgType, timeStamp, signalPower, icao, msg])
				except Exception as e:
					print("dump1090ToPipe: Error: " + str(e))
					exit.set()
			os.killpg(os.getpgid(self.dump1090process.pid), signal.SIGTERM)	#Terminating the dump1090 process
			s.close()
			return
