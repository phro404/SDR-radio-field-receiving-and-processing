import socket
import json

##################
#work in progress#
##################

class Client_socket:
    def __init__(self, adress_family, protocol):
        self.localInputBuffer = []

        self.client_s = socket.socket(getattr(socket, adress_family), getattr(socket, protocol))

    def connect_socket(self, ip_adress, port):
        self.client_s.connect(getattr(socket, ip_adress), getattr(socket, port))

    def recv_socket(self, codec, pipe_out):
        self.pipeOUT = pipe_out

        while (True):
            data_recv = self.client_s.recv(1024)
             
            #decoding data stream into JSON-strings
            if (codec == ""):
                data_recv = data_recv.decode()
            else:
                data_recv = data_recv.decode(codec)
   
            if (len(data) != 0):
                self.localInputBuffer.append(data_rev)
                
            for container in self.localInputBuffer:
                data_dict = json.loads(data_rec)    #convert JSON-string into dictionary
                self.pipeOUT.send(data_dict)

            self.localInputBuffer = []
