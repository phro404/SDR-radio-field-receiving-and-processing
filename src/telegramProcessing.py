import multiprocessing

class TelegramProcessing:
	def __init__(self):
		self.dump1090_buffer = []
		self.socket_buffer = []
		self.out_buffer = []
		
	def processing(self):
		pass
		################################################################
		#####	Dein Code	#########################################
		#####	Allen Output für Ingo in out_buffer appenden	##########
		################################################################
		
	def run(self, socket_pipe, dump1090_pipe, out_pipe, exit):
		#Um z.B. im Falle eines schwerwiegenden Errors das KOMPLETTE Programm zu beenden kann der Befehl "exit.set()" benutzt werden
		while (not exit.is_set()):
			while (socket_pipe.poll()):
				data = socket_pipe.recv()
				self.socket_buffer.append(data)
				
			while (dump1090_pipe.poll()):
				data = dump1090_pipe.recv()
				self.dump1090_buffer.append(data)
				
			self.processing()	
			
			for data in self.out_buffer:
				print(data)
				out_pipe.send(data)
				
			self.dump1090_buffer = []
			self.socket__buffer = []
			self.out_buffer = []
