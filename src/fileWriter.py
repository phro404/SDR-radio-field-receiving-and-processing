import os
import visualization
from datetime import datetime	
from time import sleep

class FileWriter(object):							

	def __init__(self): 
		self.lvl = ""							#defines string for lvl_reply_date prints
		self.amp = ""							#defines string for amp_hist_date prints
		self.d = ""			#defines string for first usage of self.print
		
		self.lvlFirstLine = "time,rx_cnt,rx_avg_lvl,curr_ch_occ,curr_planes,test_tx_cnt,test_rx_succ_cnt_s,test_rx_succ_cnt_l,test_rx_succ_cnt_ac,test_succ_lvl_s,test_succ_lvl_l,test_succ_lvl_ac,test_avg_lvl_s,test_avg_lvl_l,test_avg_lvl_ac\n"

		self.ampFirstLine = "time,type,total,-90,-89,-88,-87,-86,-85,-84,-83,-82,-81,-80,-79,-78,-77,-76,-75,-74,-73,-72,-71,-70,-69,-68,-67,-66,-65,-64,-63,-62,-61,-60,-59,-58,-57,-56,-55,-54,-53,-52,-51,-50,-49,-48,-47,-46\n"
		self.numFiles = 0
		
	
	def sort(self, raw_pipe_out):
		local_buffer = []
		Slist = {}
		Llist = {}
		AClist = {}
		Dlist = {}
		
		while(not raw_pipe_out.poll()):
			sleep(0.05)
		
		while(raw_pipe_out.poll()):						#polling
			data = raw_pipe_out.recv()				#receive piped data
			#print("fileWriter polling: " + str(data))
			local_buffer.append(data)				#get piped date in local buffer
			sleep(0.05)

		for dataPackage in local_buffer:
			for key, value in dataPackage.items():
				if (not isinstance(value, str)):
					dataPackage[key] = str(value)
			#print('fileWriter' + str(dataPackage))
			if not isinstance(dataPackage, dict):
				print("Pipe-Packet ist kein Wörterbuch sondern: " + str(type(dataPackage)))
				break
			if ('rx_cnt' in dataPackage.keys()):
				Dlist = {**Dlist, **dataPackage}
			elif (dataPackage['type'] == 'S Short Reply'):
				Slist = {**Slist, **dataPackage}
			elif (dataPackage['type'] == 'S Long Reply'):
				Llist = {**Llist, **dataPackage}
			elif (dataPackage['type'] == 'AC Reply'):
				AClist = {**AClist, **dataPackage}

		
		if not (len(Dlist) < 15):
			self.lvl = Dlist["time"] + "," + Dlist["rx_cnt"] + "," + Dlist["rx_avg_lvl"] + "," + Dlist["curr_ch_occ"] + "," + Dlist["curr_planes"] + "," + Dlist["test_tx_cnt"] + "," + Dlist["test_rx_succ_cnt_s"] + "," + Dlist["test_rx_succ_cnt_l"] + "," + Dlist["test_rx_succ_cnt_ac"] + "," + Dlist["test_succ_lvl_s"] + "," + Dlist["test_succ_lvl_l"] + "," +Dlist["test_succ_lvl_ac"] + "," +Dlist["test_avg_lvl_s"] + "," + Dlist["test_avg_lvl_l"] + "," + Dlist["test_avg_lvl_ac"] + "\n"
		
		if not (len(Slist) < 48):
			self.amp = Slist["time"] + "," + Slist["type"] + "," + Slist["total"] + "," + Slist["-90"] + "," + Slist["-89"] + "," + Slist["-88"] + "," + Slist["-87"] + "," + Slist["-86"] + "," + Slist["-85"] + "," + Slist["-84"] + "," + Slist["-83"] + "," + Slist["-82"] + "," + Slist["-81"] + "," + Slist["-80"] + "," + Slist["-79"] + "," + Slist["-78"] + "," + Slist["-77"] + "," + Slist["-76"] + "," + Slist["-75"] + "," + Slist["-74"] + "," + Slist["-73"] + "," + Slist["-72"] + "," + Slist["-71"] + "," + Slist["-70"] + "," + Slist["-69"] + "," + Slist["-68"] + "," + Slist["-67"] + "," + Slist["-66"] + "," + Slist["-65"] + "," + Slist["-64"] + "," + Slist["-63"] + "," + Slist["-62"] + "," + Slist["-61"] + "," + Slist["-60"] + "," + Slist["-59"] + "," + Slist["-58"] + "," + Slist["-57"] + "," + Slist["-56"] + "," + Slist["-55"] + "," + Slist["-54"] + "," + Slist["-53"] + "," + Slist["-52"] + "," + Slist["-51"] + "," + Slist["-50"] + "," + Slist["-49"] + "," + Slist["-48"] + "," + Slist["-47"] + "," + Slist["-46"] + "\n"
		if not (len(Llist) < 48):
			self.amp = self.amp + Llist["time"]+"," + Llist["type"]+"," + Llist["total"]+"," + Llist["-90"]+"," + Llist["-89"]+"," + Llist["-88"] + "," + Llist["-87"] + "," + Llist["-86"] + "," + Llist["-85"] + "," + Llist["-84"] + "," + Llist["-83"] + "," + Llist["-82"] + "," + Llist["-81"] + "," + Llist["-80"] + "," + Llist["-79"] + "," + Llist["-78"] + "," + Llist["-77"] + "," + Llist["-76"] + "," + Llist["-75"] + "," + Llist["-74"] + "," + Llist["-73"] + "," + Llist["-72"] + "," + Llist["-71"] + "," + Llist["-70"] + "," + Llist["-69"] + "," + Llist["-68"] + "," + Llist["-67"] + "," + Llist["-66"] + "," + Llist["-65"] + "," + Llist["-64"] + "," + Llist["-63"] + "," + Llist["-62"] + "," + Llist["-61"] + "," + Llist["-60"] + "," + Llist["-59"] + "," + Llist["-58"] + "," + Llist["-57"] + "," + Llist["-56"] + "," + Llist["-55"] + "," + Llist["-54"] + "," + Llist["-53"] + "," + Llist["-52"] + "," + Llist["-51"] + "," + Llist["-50"] + "," + Llist["-49"] + "," + Llist["-48"] + "," + Llist["-47"] + "," + Llist["-46"] + "\n"
		if not (len(AClist) < 48):
			self.amp = self.amp + AClist["time"]+"," + AClist["type"]+"," + AClist["total"]+"," + AClist["-90"]+"," + AClist["-89"]+"," + AClist["-88"]+"," + AClist["-87"]+"," + AClist["-86"]+"," + AClist["-85"]+"," + AClist["-84"]+"," + AClist["-83"]+"," + AClist["-82"]+"," + AClist["-81"]+"," + AClist["-80"]+"," + AClist["-79"]+"," + AClist["-78"]+"," + AClist["-77"]+"," + AClist["-76"]+"," + AClist["-75"]+"," + AClist["-74"]+"," + AClist["-73"]+"," + AClist["-72"]+"," + AClist["-71"]+"," + AClist["-70"]+"," + AClist["-69"]+"," + AClist["-68"]+"," + AClist["-67"]+"," + AClist["-66"]+"," + AClist["-65"]+"," + AClist["-64"]+"," + AClist["-63"]+"," + AClist["-62"]+"," + AClist["-61"]+"," + AClist["-60"]+"," + AClist["-59"]+"," + AClist["-58"]+"," + AClist["-57"]+"," + AClist["-56"]+"," + AClist["-55"]+"," + AClist["-54"]+"," + AClist["-53"]+"," + AClist["-52"]+"," + AClist["-51"]+"," + AClist["-50"]+"," + AClist["-49"]+"," + AClist["-48"]+"," + AClist["-47"]+"," + AClist["-46"] + "\n"


	def write(self):	
		now = datetime.now()

		plotNow = False						#EDIT05.26.2020 for liveplot criteria
		if (self.d !=  now.strftime("%Y.%m.%d_%H")):				#check for new hour
			self.d = now.strftime("%Y.%m.%d_%H")				#set d as timedefinition #EDIT 05.26.2020 auf nachfrage von roman reihenfolge angepasst
			
			name_lvl = "../data/lvl_reply_" + self.d + ".csv"				#set name lvl_reply_date
			f = open(name_lvl ,"a")						#open data with name, if not existing create
			f.write(self.lvlFirstLine)						#print string in data
			f.close()
			
			name_amp = "../data/amp_hist_" + self.d + ".csv"				#set name lvl_reply_date
			f = open(name_amp ,"a")						#open data with name, if not existing create
			f.write(self.ampFirstLine)						#print string in data
			f.close()
			
			plotNow = True 					#EDIT05.26.2020  for starting a live plot when first line is printed
			
			self.numFiles = self.numFiles + 1
			if (self.numFiles == 1):
				self.oldOrderedList = [os.path.abspath("../data/lvl_reply_" + self.d + ".csv"), os.path.abspath("../data/lvl_reply_" + self.d + ".csv")]
				

		#os.chdir("..")
		#os.chdir("data")
		if (len(self.lvl) != 0):
			name_lvl = "../data/lvl_reply_" + self.d + ".csv"				#set name lvl_reply_date
			f = open(name_lvl ,"a")						#open data with name, if not existing create
			f.write(self.lvl)						#print string in data
			f.close()
			
		if (len(self.lvl) != 0):
			name_amp = "../data/amp_hist_" + self.d + ".csv"  				#set name amp_hist_date
			f = open(name_amp ,"a")						#open data with name, if not existing creat
			f.write(self.amp)						#print string in data
			f.close()
			
		if (self.numFiles >= 2 and plotNow):					#if first line in data written start liveplot
			visualization.visualization(self.oldOrderedList, True)
			self.oldOrderedList = [os.path.abspath("../data/lvl_reply_" + self.d + ".csv"), os.path.abspath("../data/lvl_reply_" + self.d + ".csv")]

		
	def run(self, in_pipe, exit):
		while (not exit.is_set()):
			self.sort(in_pipe)
			self.write()
		
		
		
