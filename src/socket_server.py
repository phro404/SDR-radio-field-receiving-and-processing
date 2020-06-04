import socket	
import json
import time 
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


	#create test data with json
	testlist=[1,2,3,4,5]
	teststring='ModeS_Short'
	testint = 60

	testcontainer = {
		'payload1': 'firstpayload',
		'payload2': 'secondpayload',
		'payload3': 'thirdpayload'}

	testdict = {
		'format': teststring,
		'payload': testcontainer,
		'amount': '10',
		'duration_in_sec': testint,
		'repeats': 2}

	testdict = json.dumps(testdict) #converting dictionary in json-string


	#sending test data
	try:
		while True: 
			time.sleep(3)
			c.send(testdict.encode('ascii'))
						
	except:
		pass
		
	finally:
		c.close() # Close the connection with the client

