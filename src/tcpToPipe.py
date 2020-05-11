import socket
import time

class TcpToPipe: #Leitet Beast-TCP Output auf Pipe um
	def __init__(self, pipe_out, exception_queue, port=30005, host='localhost'):
		self.port = port
		self.host = host
		self.pipeOUT = pipe_out
		self.exception_queue = exception_queue
		
	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			for i in range(100):
				try:
					s.connect((self.host, self.port))
					break
				except Exception as e:
					if (i == 99):
						tb = traceback.format_exc()
						self.exception_queue.put((e, tb))
						return
					else:
						time.sleep(0.1)
			while True:
				try:
					data = s.recv(64)
					h = int.from_bytes(data[2:7], byteorder='big')
					self.pipeOUT.send([len(data), data[0], data[1], h, data[8], data[9:].hex()])
				except:
					return
			    
