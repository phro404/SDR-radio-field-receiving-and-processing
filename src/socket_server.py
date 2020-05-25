import socket	
import json
import time 
from random import randint

while True:
	#create a socket object 
	s = socket.socket()		  
	print ("Socket successfully created")
		  
	s.bind(('localhost', 8012)) #TODO: choose correct arguments here
	print ("socket binded to 8012") 
	  
	s.listen(5)	  
	print ("socket is listening")			
	   
	c, addr = s.accept()	  
	print ('Got connection from', addr) 


	#create dictionary 
	testdict = {'format': 'unkown', 'payload': 0}
	
	try:
		while True:
			#creating test data
			temp_rand = randint(1,3)
			if (temp_rand == 1):
				testdict['format'] = 's'
			elif (temp_rand == 2):
				testdict['format'] = 'l'
			else:
				testdict['format'] = 'ac'
			
			testdict['payload'] = hex(randint(0,2**112))
			#sending test data
			testdict = json.dumps(testdict)	#converting dictionary in json-string
			time.sleep(randint(1,1000000)/4000000)	#wait a random time up to 0.25s
			c.send(testdict.encode('ascii'))
						
	except:
		pass
		
	finally:
		c.close() # Close the connection with the client
