
import socket
HOST = 'localhost'
PORT=30005
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        try:
            data = s.recv(64)
            #print(len(data),data,type(data))
            #                               level
            print(len(data),data[0],data[1],int.from_bytes(data[2:7],byteorder='big'),data[8],data[9:].hex())

        except Exception as e:
            print("End/Error")
            print(e)
            break
