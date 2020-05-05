class Socket:
	def __init__(self, port, ipAdresse):
		pass
		#irgendwie den Socket initialisieren
		#Port einstellen
		#etc
		
	def irgendwasTun(self, zuVerarbeitendeDaten):
		pass
		#irgendeine Funktion
		
	def run(self, pipe_in, pipe_out): #pipe_out ist zum empfangen von Daten #pipe_in ist zum empfangen von Daten
		self.pipeOUT = pipe_out
		self.pipeIN = pipe_in
		while (True):
            while self.pipeIN.poll():
                dataReceived = self.pipeIN.recv()
                localInputBuffer.append(dataReceived)
                
            for data in localInputBuffer:
                self.irgendwasTun(data)
                
            localInputBuffer = []
                
