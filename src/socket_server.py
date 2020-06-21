#============================================== import of the relevant libraries ================================================
import socket	
import json
import time
import random
#============================================== import of the relevant libraries End =============================================

 """creating testtelegrams for testing the socket"""
while True:
	"""creat a socket object""" 
	s = socket.socket()		  
	print ("Socket successfully created")
	
	"""establishing connection with the client"""
	s.bind(('localhost', 8012)) 					#TODO: choose correct arguments here
	print ("socket binded to 8012") 
	
	"""socket starts to listen"""
	s.listen(5)	  
	print ("socket is listening")			
	
	"""connection established"""
	c, addr = s.accept()	  
	print ('Got connection from', addr) 

	"""creat test data with json"""
	"""dictionary for Mode AC"""
	telegram_mode_ac = {
		'type': 'mode_ac',
		'payload': '7311',
		'amplitude': 1.0,
		'shift': 0.0,
		'phase': 0	}

	"""dictionary for Mode S short"""
	telegram_mode_s_short = {
		'type': 'mode_s_short',
		'format_number': 'DF00',
		'payload': None,
		'amplitude': 1.0,
		'shift': 0.0,
		'phase': 0	}
		
	"""dictionary for Mode S long"""
	telegram_mode_s_long = {
		'type': 'mode_s_long',
		'format_number': 'DF16',
		'payload': None,
		'amplitude': 1.0,
		'shift': 0.0,
		'phase': 0	}

	"""Sending test data"""
	try:
		while True: 
			time.sleep(32)					#TODO: you can choose a sleeping time by yourself e.g:32 seconds
			randomint = random.randint(1, 30) 		#creating a random value between 1 and 30 for the rate
			
			"""dictionary for the testtelegrams"""
			testtelegrams = {
				'level': -50,
				'rate': randomint,
				'amount': 15,
				'samplerate': 20000000,
				'telegrams': [telegram_mode_ac, telegram_mode_s_short, telegram_mode_s_long]	}
				
			testtelegrams = json.dumps(testtelegrams) 	#converting dictionary in json-string
			c.send(testtelegrams.encode('ascii')) 	
			print("Data sent!")
	except:
		pass
		
	finally:
		c.close() 						# Close the connection with the client
