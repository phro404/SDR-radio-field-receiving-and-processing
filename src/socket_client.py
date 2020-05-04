import configparser 
import socket
import json

#starting with reading out configuration parameter for socket out of config-file
config = configparser.ConfigParser()    #ConfigParser implementing interpolation
#config.sections()   #returns a list of section names, excluding [DEFAULT]
config.read('import_init_data.conf')

if ('SOCKET' in config):
    print("Socket configuration section found.")
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

#initializing socket
with socket.socket(getattr(socket, adress_family), getattr(socket, protocol)) as client_s:    #because of 'with'-statement closing of socket is not necessary 
    client_s.connect(('localhost', 8012))

    while True:
        try:
            data = client_s.recv(1024)  #argument specifies the buffer size in bytes
            
            if (codec == ""):
                data = data.decode()
            else:
                data = data.decode(codec)

            if (len(data) != 0):
                data_dict = json.loads(data)    #convert JSON-string into dictionary

                #some examples for testing
                print(data_dict["payload"])
                print("Received", data_dict["amount"], data_dict["format"] )

                #TODO: insert pipe and give relevant data to main process

        except Exception as e:
            print("Error occurred!")
            print(e)
            break
