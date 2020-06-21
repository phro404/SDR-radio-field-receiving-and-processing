import multiprocessing
import time
from datetime import datetime
import configparser

class TelegramProcessing:
	"""Calculate all relevant values for the plots"""
	
	def __init__(self):
		"""Set up attributes and read line-duration out of config-file."""
		self.dump1090_buffer = []
		self.socket_buffer = []
		self.out_buffer = []

		#reading out configuration parameter
		config = configparser.ConfigParser()
		config.read('import_init_data.conf')
		if ('PROCESSING_INTERVAL' in config):
			print("Processing interval section was found.")
			self.pro_val = config['PROCESSING_INTERVAL']['LINE_DURATION']
		else:
			print("Processing interval section is not available! Default value is set.")
			self.pro_val = 15

	def processing(self, socket_pipe, dump1090_pipe, out_pipe):
		"""Take data from socket and dump1090 into account for calculating defined values.
		
		Arguments:
		socket_pipe (named pipe) -- contains all current informations received via the testtelegram socket
		dump1090_pipe (named pipe) -- contains all current telegrams received by dump1090
		out_pipe (named pipe) -- results of processing get written into this pipe in a agreed format
		"""
		t_start = time.time()

		#defining dictionaries
		Dlist = {'time': 0, 'rx_cnt': 0, 'rx_avg_lvl': 0, 'curr_ch_occ': 0, 'curr_planes': 0, 'test_tx_cnt': 0, 'test_rx_succ_cnt_s': 0, 'test_rx_succ_cnt_l': 0, 
			'test_rx_succ_cnt_ac': 0, 'test_succ_lvl_s': 0, 'test_succ_lvl_l': 0, 'test_succ_lvl_ac': 0, 'test_avg_lvl_s': 0, 'test_avg_lvl_l': 0, 'test_avg_lvl_ac': 0}
		Slist = {'time': 0, 'type': 'S Short Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
			'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
			'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		Llist = {'time': 0, 'type': 'S Long Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
			'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
			'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		AClist = {'time': 0, 'type': 'A/C Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
			'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
			'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		ICAO_list = []; counter = 0; lvl_sum = 0; ch_occ_cnt = 0; socket_sync_flag = 0; ac_el_cnt = 0; ss_el_cnt = 0; sl_el_cnt = 0; overflow90_cnt = 0; overflow46_cnt = 0;
		t_now = time.time()

		while (t_now < t_start + float(self.pro_val)):
			time.sleep(0.05)
			while (dump1090_pipe.poll()):
				data = dump1090_pipe.recv()
				self.dump1090_buffer.append(data)
			while (socket_pipe.poll()):
				data = socket_pipe.recv()
				self.socket_buffer.append(data)

			if (len(self.socket_buffer) > 0):
				socket_sync_flag = 1
				break
			else:
				#adding only dump1090 data
				if (len(self.dump1090_buffer) > 0):
					for d_element in self.dump1090_buffer:
						counter +=1;

						if (d_element[0] == 49):	#modeA/C detected
							ch_occ_cnt += 0.0000203
							ac_el_cnt += 1
							#getting level information out of current element
							if (d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								AClist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif (d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								AClist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								AClist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]

						elif (d_element[0] == 50):	#modeS short detected
							ch_occ_cnt += 0.000064
							ss_el_cnt += 1
							#getting level information out of current element
							if(d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								Slist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif(d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								Slist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								Slist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]

						elif (d_element[0] == 51):	#modeS long detected
							ch_occ_cnt += 0.000120
							sl_el_cnt += 1
							#getting level information out of current element
							if(d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								Llist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif (d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								Llist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								Llist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]

						else:
							print("Unknown telegram-type was detected.")
						
						#updating list of current planes
						if (d_element[3] != None):
							foundflag = 0
							for address in ICAO_list:
								if (d_element[3] == address):
									foundflag = 1
									break
							if (foundflag == 0):
								ICAO_list.append(d_element[3])



					#emptying self.dump1090_buffer
					self.dump1090_buffer = []

				t_now = time.time()
		
		#calculating values per seconds and write into self.out_buffer
		t_end = time.time()
		t_measurement = round((t_end - t_start), 6)
		t_end = datetime.now()

		Dlist['rx_cnt'] = (counter / t_measurement)
		if (counter > 0):
			Dlist['rx_avg_lvl'] = (lvl_sum / counter)
		Dlist['curr_ch_occ'] = (ch_occ_cnt / t_measurement)
		Dlist['curr_planes'] = len(ICAO_list)
		AClist['total'] = ac_el_cnt
		Slist['total'] = ss_el_cnt
		Llist['total'] = sl_el_cnt
		Dlist['time'] = str(t_end)
		AClist['time'] = str(t_end)
		Slist['time'] = str(t_end)
		Llist['time'] = str(t_end)

		#write into self.out_buffer, only works in this order
		self.out_buffer.append(Dlist)
		self.out_buffer.append(Slist)
		self.out_buffer.append(Llist)
		self.out_buffer.append(AClist)
		
		for values in self.out_buffer:
			out_pipe.send(values)
		self.out_buffer = []
		
		if (overflow90_cnt > 0):
			print(overflow90_cnt, "telegrams had been weaker than -90 dBm and were counted as -90 dBm.")
			
		if (overflow46_cnt > 0):
			print(overflow46_cnt, "telegrams had been stronger than -46 dBm and were counted as -46 dBm.")

		if (socket_sync_flag == 1):
			t_start = time.time()
			t_now = time.time()

			#reseting dictionaries etc.
			Dlist = {'time': 0, 'rx_cnt': 0, 'rx_avg_lvl': 0, 'curr_ch_occ': 0, 'curr_planes': 0, 'test_tx_cnt': 0, 'test_rx_succ_cnt_s': 0, 'test_rx_succ_cnt_l': 0, 
				'test_rx_succ_cnt_ac': 0, 'test_succ_lvl_s': 0, 'test_succ_lvl_l': 0, 'test_succ_lvl_ac': 0, 'test_avg_lvl_s': 0, 'test_avg_lvl_l': 0, 'test_avg_lvl_ac': 0}
			Slist = {'time': 0, 'type': 'S Short Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
				'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
				'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
			Llist = {'time': 0, 'type': 'S Long Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
				'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
				'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
			AClist = {'time': 0, 'type': 'A/C Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
				'-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
				'-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
			ICAO_list = []; counter = 0; lvl_sum += 0; ch_occ_cnt = 0; ac_el_cnt = 0; ss_el_cnt = 0; sl_el_cnt = 0; ac_succ_cnt = 0; ss_succ_cnt = 0; overflow90_cnt = 0; overflow46_cnt = 0;
			sl_succ_cnt = 0; ac_lvl_sum = 0; ss_lvl_sum = 0; sl_lvl_sum = 0

			while (t_now < t_start + float(self.pro_val) + float(1)):
				time.sleep(0.05)
				while (dump1090_pipe.poll()):
					data = dump1090_pipe.recv()
					self.dump1090_buffer.append(data)

				#now adding data with respect to socket data
				if (len(self.dump1090_buffer) > 0):
					for d_element in self.dump1090_buffer:
						counter +=1

						if (d_element[0] == 49):	#modeA/C detected
							ch_occ_cnt += 0.0000203
							ac_el_cnt += 1
							#getting level information out of current element
							if(d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								AClist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif(d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								AClist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								AClist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]

						elif (d_element[0] == 50):	#modeS short detected
							ch_occ_cnt += 0.000064
							ss_el_cnt += 1
							#getting level information out of current element
							if(d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								Slist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif(d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								Slist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								Slist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]

						elif (d_element[0] == 51):	#modeS long detected
							ch_occ_cnt += 0.000120
							sl_el_cnt += 1
							#getting level information out of current element
							if(d_element[2] != None and d_element[2] > -46):	#preventing exceeding the scale
								Llist['-46'] += 1
								lvl_sum += d_element[2]
								overflow46_cnt += 1
							elif(d_element[2] != None and d_element[2] < -90):	#preventing exceeding the scale
								Llist['-90'] += 1
								lvl_sum += d_element[2]
								overflow90_cnt += 1
							elif (d_element[2] != None):	#checking in case level is not available
								Llist[str(round(d_element[2],0))[0:3]] += 1	
								lvl_sum += d_element[2]
						else:
							print("Unknown telegram-type was detected.")
						
						#updating list of current planes
						if (d_element[3] != None):
							foundflag = 0
							for address in ICAO_list:
								if (d_element[3] == address):
									foundflag = 1
									break
							if (foundflag == 0):
								ICAO_list.append(d_element[3])

						if (len(self.socket_buffer) == 0):
							print("An error occured while trying to read an empty socket buffer.")
						else:
							if (len(self.socket_buffer) > 1):
								print("There are too many arguments in socket buffer. Only the first one will be analyzed")

							for k in self.socket_buffer[0]['telegrams']:
								if (k['payload'] != None and k['payload'] != "null"):
									str_index = d_element[4].find(k['payload'])
									if (str_index != -1):	#if find() returns -1 it means the string could not be found
										if (k['type'] == "mode_ac" and d_element[0] == 49):
											ac_succ_cnt += 1
											ac_lvl_sum += d_element[2]
										if (k['type'] == "mode_s_short" and d_element[0] == 50):
											ss_succ_cnt += 1
											ss_lvl_sum += d_element[2]
										if (k['type'] == "mode_s_long" and d_element[0] == 51):
											sl_succ_cnt += 1
											sl_lvl_sum += d_element[2]

				#emptying self.dump1090_buffer
				self.dump1090_buffer = []
				t_now = time.time()


			#calculating values for seconds and write into self.out_buffer
			t_end = time.time()
			t_measurement = round((t_end - t_start), 6)
			t_end = datetime.now()

			Dlist['rx_cnt'] = ((counter - ss_succ_cnt - sl_succ_cnt - ac_succ_cnt) / t_measurement)
			if (counter > 0):
				Dlist['rx_avg_lvl'] = (lvl_sum / counter)
			Dlist['curr_ch_occ'] = (ch_occ_cnt / t_measurement)
			Dlist['curr_planes'] = len(ICAO_list)
			Dlist['test_tx_cnt'] = self.socket_buffer[0]['amount'] * self.socket_buffer[0]['rate'] * len(self.socket_buffer[0]['telegrams'])
			Dlist['test_rx_succ_cnt_s'] = ss_succ_cnt
			Dlist['test_rx_succ_cnt_l'] = sl_succ_cnt
			Dlist['test_rx_succ_cnt_ac'] = ac_succ_cnt

			Dlist['test_succ_lvl_s'] = (ss_succ_cnt / (self.socket_buffer[0]['amount'] ) * 100)
			Dlist['test_succ_lvl_l'] = (sl_succ_cnt / (self.socket_buffer[0]['amount'] ) * 100)
			Dlist['test_succ_lvl_ac'] = (ac_succ_cnt / (self.socket_buffer[0]['amount'] ) * 100)

			if (ss_succ_cnt > 0):
				Dlist['test_avg_lvl_s'] = (ss_lvl_sum / ss_succ_cnt)
			if (sl_succ_cnt > 0):
				Dlist['test_avg_lvl_l'] = (sl_lvl_sum / sl_succ_cnt) 
			if (ac_succ_cnt > 0):
				Dlist['test_avg_lvl_ac'] = (ac_lvl_sum / ac_succ_cnt) 
			
			AClist['total'] = ac_el_cnt
			Slist['total'] = ss_el_cnt
			Llist['total'] = sl_el_cnt
			Dlist['time'] = str(t_end)
			AClist['time'] = str(t_end)
			Slist['time'] = str(t_end)
			Llist['time'] = str(t_end)
			

			#write into self.out_buffer, only works in this order
			self.out_buffer.append(Dlist)
			self.out_buffer.append(Slist)
			self.out_buffer.append(Llist)
			self.out_buffer.append(AClist)
			
			if (overflow90_cnt > 0):
				print(overflow90_cnt, "telegrams had been weaker than -90 dBm and were counted as -90 dBm.")
			
			if (overflow46_cnt > 0):
				print(overflow46_cnt, "telegrams had been stronger than -46 dBm and were counted as -46 dBm.")

	def run(self, socket_pipe, dump1090_pipe, out_pipe, exit):
		"""Poll pipes, call processing and send as well as empty the pipes afterwards.
		
		Arguments:
		socket_pipe (named pipe) -- contains all current informations received via the testtelegram socket
		dump1090_pipe (named pipe) -- contains all current telegrams received by dump1090
		out_pipe (named pipe) -- results of processing get written into this pipe in a agreed format
		exit
		"""
		#in case of a fatale error the whole program will be terminated using exit.set()
		while (not exit.is_set()):
			while (socket_pipe.poll()):
				data = socket_pipe.recv()
				self.socket_buffer.append(data)
				
			while (dump1090_pipe.poll()):
				data = dump1090_pipe.recv()
				self.dump1090_buffer.append(data)
				
			self.processing(socket_pipe, dump1090_pipe, out_pipe)	
			
			for data in self.out_buffer:
				out_pipe.send(data)
				
			self.dump1090_buffer = []
			self.socket_buffer = []
			self.out_buffer = []
