import socket
HOST = 'localhost'
PORT=30005
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		try:
			data = s.recv(64)
			#print(len(data),data,type(data))
			#data1 = typ
			
			#print(data[1],int.from_bytes(data[2:8],byteorder='big'),int.from_bytes(data[8:12],byteorder='big'),data[12:16].hex(),data[16:].hex())
			print(data[2:8].hex())
		except Exception as e:
			print("End/Error")
			print(e)
			break
