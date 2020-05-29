import socket
HOST = 'localhost'
PORT=30005
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		try:
			data = s.recv(64)
			print(data[2:8].hex())
		except Exception as e:
			print("End/Error")
			print(e)
			break
