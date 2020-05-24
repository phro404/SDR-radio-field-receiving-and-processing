import multiprocessing
import time

class TelegramProcessing:
	def __init__(self):
		self.dump1090_buffer = []
		self.socket_buffer = []
		self.out_buffer = []
		
	def processing(self):
		t0 = time.time()
		#defining dictionaries
		Dlist = {'time': 0, 'rx_cnt': 0, 'rx_avg_lvl': 0, 'curr_ch_occ': 0, 'curr_planes': 0, 'test_tx_cnt': 0, 'test_rx_succ_cnt_s': 0, 'test_rx_succ_cnt_l': 0, 
		  'test_rx_succ_cnt_ac': 0, 'test_succ_lvl_s': 0, 'test_succ_lvl_l': 0, 'text_succ_lvl_ac': 0, 'test_avg_lvl_s': 0, 'test_avg_lvl_l': 0, 'test_avg_lvl_ac': 0}
		Slist = {'time': 0, 'type': 'S Short Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
		  '-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
		  '-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		Llist = {'time': 0, 'type': 'S Short Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
		  '-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
		  '-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		AClist = {'time': 0, 'type': 'S Short Reply', 'total': 0, '-90': 0, '-89': 0, '-88': 0, '-87': 0, '-86': 0, '-85': 0, '-84': 0, '-83': 0, '-82': 0, '-81': 0, '-80': 0,
		  '-79': 0, '-78': 0, '-77': 0, '-76': 0, '-75': 0, '-74': 0, '-73': 0, '-72': 0, '-71': 0, '-70': 0, '-69': 0, '-68': 0, '-67': 0, '-66': 0, '-65': 0, '-64': 0, '-63': 0,
		  '-62': 0, '-61': 0, '-60': 0, '-59': 0, '-58': 0, '-57': 0, '-56': 0, '-55': 0, '-54': 0, '-53': 0, '-52': 0, '-51': 0, '-50': 0, '-49': 0, '-48': 0, '-47': 0, '-46': 0}
		
		#filling dictionaries
		if (len(self.dump1090_buffer) > 0):
			Dlist['time'] = self.dump1090_buffer[0][1]	#using earliest timestamp
			Slist['time'] = self.dump1090_buffer[0][1]
			Llist['time'] = self.dump1090_buffer[0][1]
			AClist['time'] = self.dump1090_buffer[0][1]

			Dlist['test_tx_cnt'] = len(self.socket_buffer)

			counter = 0; chOccCnt = 0; sCnt = 0; lCnt = 0; acCnt = 0; lvl_sum = 0
			ICAO_list = []

			for d_element in self.dump1090_buffer:
				counter +=1; lvl_sum += d_element[2]

				if (d_element[0] == 49):	#modeA/C detected
					chOccCnt += 0.0000203
					if(d_elemnt[2] > -46):
						AClist['-46'] += 1
					else:
						AClist[str(round(d_element[2],0))[0:3]] += 1
			
				if (d_element[0] == 50):	#modeS short detected
					chOccCnt += 0.000064
					if(d_element[2] > -46):
						Slist['-46'] += 1
					else:
						Slist[str(round(d_element[2],0))[0:3]] += 1
						
				if (d_element[0] == 51):	#modeL long detected
					chOccCnt += 0.000120
					if(d_element[2] > -46):
						Llist['46'] += 1
					else:
						llist[str(round(d_element[2],0))[0:3]] += 1
						
				foundflag = 0
				for address in ICAO_list:
					if (d_element[3] == address):
						foundflag = 1
						break
				if (foundflag == 0):
					ICAO_list.append(d_element[3])


				if(len(self.socket_buffer) > 0):
					for s_element in self.socket_buffer:
						if (s_element != d_element[4]):	#dump1090 output does not match with a send test-telegram TODO: check when socket ready !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
							Dlist['rx_cnt'] +=1
						elif (s_element == d_element[4] and d_element[0] == 49):	#modeA/C test-telegram matched
							Dlist['test_rx_succ_cnt_ac'] += 1
							Dlist['test_avg_lvl_ac'] += d_element[2]
							acCnt += 1 
						elif (s_element == d_element[4] and d_element[0] == 50):	#modeS short test-telegram matched
							Dlist['test_rx_succ_cnt_s'] += 1
							Dlist['test_avg_lvl_s'] += d_element[2]
							sCnt += 1 
						elif (s_element == d_element[4] and d_element[0] == 51):	#modeS long test-telegram matched
							Dlist['test_rx_succ_cnt_l'] += 1
							Dlist['test_avg_lvl_l'] += d_element[2]
							lCnt += 1 
						else:
							print("Exception while matching socket data occured.")
	

			Dlist['test_succ_lvl_s'] = 33		#tbd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			Dlist['test_succ_lvl_ac'] = 33		#tbd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			Dlist['test_succ_lvl_l'] = 33		#tbd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			Dlist['test_avg_lvl_l'] /= lCnt
			Dlist['test_avg_lvl_s'] /= sCnt
			Dlist['test_avg_lvl_ac'] /= acCnt
			Dlist['rx_avg_lvl'] = (lvl_sum / counter)
			Dlist['curr_ch_occ'] = (chOccCnt / (self.dump1090_buffer[len(self.dump1090_buffer)][1] - self.dump1090_buffer[0][1]))		#calculating channel occupation TODO: test!!!!!!!!!!!!!!!!!!!!!!!
			Dlist['curr_planes'] = len(ICAO_list)

			self.out_buffer.append(Dlist)
			self.out_buffer.append(Slist)
			self.out_buffer.append(Llist)
			self.out_buffer.append(AClist)
		
		t1 = time.time()
		totaltime = t1 - t0
		time.sleep(0.99 - totaltime)
		
	def run(self, socket_pipe, dump1090_pipe, out_pipe, exit):
		#Um z.B. im Falle eines schwerwiegenden Errors das KOMPLETTE Programm zu beenden kann der Befehl "exit.set()" benutzt werden
		while (not exit.is_set()):
			while (socket_pipe.poll()):
				data = socket_pipe.recv()
				self.socket_buffer.append(data)
				
			while (dump1090_pipe.poll()):
				data = dump1090_pipe.recv()
				self.dump1090_buffer.append(data)
				
			self.processing()	
			
			for data in self.out_buffer:
				print(data)
				out_pipe.send(data)
				
			self.dump1090_buffer = []
			self.socket__buffer = []
			self.out_buffer = []
