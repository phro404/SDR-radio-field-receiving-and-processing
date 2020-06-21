import socket
import json
import configparser
from time import sleep

class Client_socket:
	"""Set up and handle a socket for receiving testtelegrams."""
	
	retries = 10	#Maximum Connecting Retries
	
	def __init__(self):
		"""Read starting parameters out of a config-file and create a listening socket."""
		#starting with reading out configuration parameter for socket out of config-file
		config = configparser.ConfigParser()	#ConfigParser implementing interpolation
		#config.sections()   #returns a list of section names, excluding [DEFAULT]
		config.read('import_init_data.conf')
		
		if ('SOCKET' in config):
			pass
			#print("Socket configuration section found.")
		else:
			print("No socket configuration section available!")

		#saving paramter in local variables
		adress_family = config['SOCKET']['IP_ADRESS_FAMILY']
		ip_adress = config['SOCKET']['IP_ADRESS']
		port_number = config['SOCKET']['PORT']
		start_listening = config['SOCKET']['START_LISTENING']
		protocol = config['SOCKET']['PROTOCOL']
		codec = config['SOCKET']['DECODING']

		if (protocol == 'TCP'):
			protocol = 'SOCK_STREAM'
		elif (protocol == 'UDP'):
			protocol = 'SOCK_DGRAM'
		else:
			protocol = 'unknown protocol'
			print("unkown protocol choosen in configuration ['SOCKET']['PROTOCOL']")
		
		self.codec = codec
		self.localInputBuffer = []
		self.client_s = socket.socket(getattr(socket, adress_family), getattr(socket, protocol))
		
		self.working = False
		for i in range(Client_socket.retries):
			try:
				#self.client_s.connect(getattr(socket, ip_adress), getattr(socket, port))
				self.client_s.connect((ip_adress, int(port_number)))
				self.working = True
				break
			except Exception as e:
				if (i == Client_socket.retries-1):
					print("Client_socket couldn't connect to the testtelegram server. Continuing anyway..")
					print(e)

	def run(self, pipe_out, exception_queue, exit):
		"""Keep receiving data, decode them, convert them into a JSON-string and write them into a pipe.
		
		Arguments:
		pipe_out (named pipe) -- the pipe in which socket-received and decoded data gets written
		exception_queue
		exit
		"""
		if (self.working):
			while (not exit.is_set()):
				try:
					data_recv = self.client_s.recv(1024)
					 
					#decoding data stream into readable JSON-string
					if (self.codec == ""):
						data_recv = data_recv.decode()
					else:
						data_recv = data_recv.decode(self.codec)
		   
					if (len(data_recv) != 0):
						self.localInputBuffer.append(data_recv)
						
					for container in self.localInputBuffer:
						data_dict = json.loads(data_recv)	#convert JSON-string into dictionary
						pipe_out.send(data_dict)
						#print(data_dict)

					self.localInputBuffer = []
				except Exception as e:
					exception_queue.put(["Problems with receiving testtelegram messages detected: ", e])
					print("Error occured in Client_socket.run()")
					print(e)
					exit.set()
		else:
			while(not exit.is_set()):
				sleep(10)		
			
			
