import os
import visualization
from datetime import datetime	
from time import sleep

class FileWriter(object):							

	def __init__(self): 
		self.lvl = ""											#defines string for lvl_reply_date prints
		self.amp = ""											#defines string for amp_hist_date prints
		self.d = ""											#defines string for first usage of self.print
		self.name_lvl = ""										#defines string for name of lvl
		self.name_amp = ""										#defines string for name of amp for liveplots
		self.name_lvl_live = ""										#defines string for name of lvl for liveplots
		self.name_amp_live = ""
		self.orderedList = [] 
		
		self.lvlFirstLine = "time,rx_cnt,rx_avg_lvl,curr_ch_occ,curr_planes,test_tx_cnt,test_rx_succ_cnt_s,test_rx_succ_cnt_l,test_rx_succ_cnt_ac,test_succ_lvl_s,test_succ_lvl_l,test_succ_lvl_ac,test_avg_lvl_s,test_avg_lvl_l,test_avg_lvl_ac\n"		#sets the first line for every lvl-file
		
		self.ampFirstLine = "time,type,total,-90,-89,-88,-87,-86,-85,-84,-83,-82,-81,-80,-79,-78,-77,-76,-75,-74,-73,-72,-71,-70,-69,-68,-67,-66,-65,-64,-63,-62,-61,-60,-59,-58,-57,-56,-55,-54,-53,-52,-51,-50,-49,-48,-47,-46\n"				#sets the first line for every amp-file
		
	def write(self, delete_liveplot_csv):	
		############################################---CSV-write-start---###############################################
		now = datetime.now()

		if (self.d !=  now.strftime("%Y-%m-%d_%H")):							#check for new hour
			self.d = now.strftime("%Y-%m-%d_%H")							#set d as timedefinition
			self.name_lvl = "../data/" + self.d + "_lvl_reply.csv"					#set name lvl_reply_date
			self.name_amp = "../data/" + self.d + "_amp_hist.csv"					#set name date_amp_hist.csv
			
			f = open(self.name_lvl ,"a")								#generating for empty-test lvl, attend to save possible content
			f.close()
			f = open(self.name_amp ,"a")								#generating for empty-test amp, attend to save possible content
			f.close()
			
			if os.stat(self.name_lvl).st_size == 0:							#if lvl is empty write firstline
				f = open(self.name_lvl ,"w+")							#open data with name, if not existing create
				f.write(self.lvlFirstLine)							#print first line in file
				f.close()
			
			if os.stat(self.name_amp).st_size == 0:							#if amp is empty write firstline
				f = open(self.name_amp ,"w+")							#open data with name, if not existing create
				f.write(self.ampFirstLine)							#print first line in file
				f.close()
					
		if (len(self.lvl) != 0):
			f = open(self.name_lvl ,"a")								#open data with name, if not existing create, attand to written text
			f.write(self.lvl)									#print string in data
			f.close()
			
		if (len(self.lvl) != 0):
			f = open(self.name_amp ,"a")								#open data with name, if not existing create, attand to written text
			f.write(self.amp)									#print string in data
			f.close()
		############################################---CSV-write-end---#####################################################
				
		############################################---Liveplot-write-start---###############################################
		self.name_lvl_live = "../data/" + "lvl_reply_live.csv"					#set name lvl_reply_date
		self.name_amp_live = "../data/" + "amp_hist_live.csv"					#set name date_amp_hist.csv
				
		if delete_liveplot_csv == True:
			if os.path.exists(self.name_lvl_live):
				print('New Live-CSV created')
				os.remove(self.name_lvl_live)
				os.remove(self.name_amp_live)
				
		f = open(self.name_lvl_live ,"a")							#generating for empty-test lvl, attend to save possible content
		f.close()
		f = open(self.name_amp_live ,"a")							#generating for empty-test amp, attend to save possible content
		f.close()

		if os.stat(self.name_lvl_live).st_size == 0:						#if lvl is empty write firstline
			f = open(self.name_lvl_live ,"w+")						#open data with name, if not existing create
			f.write(self.lvlFirstLine)							#print first line in file
			f.close()

		if os.stat(self.name_amp_live).st_size == 0:						#if amp is empty write firstline
			f = open(self.name_amp_live ,"w+")						#open data with name, if not existing create
			f.write(self.ampFirstLine)							#print first line in file
			f.close()

		if (len(self.lvl) != 0):
			f = open(self.name_lvl_live ,"a")						#open data with name, if not existing create, attand to written text
			f.write(self.lvl)								#print string in data
			f.close()
			
		if (len(self.lvl) != 0):
			f = open(self.name_amp_live ,"a")						#open data with name, if not existing create, attand to written text
			f.write(self.amp)								#print string in data
			f.close()
		############################################---Liveplot-write-end---#####################################################
		
		self.orderedList = [os.path.abspath(self.name_lvl_live), os.path.abspath(self.name_amp_live)]
		visualization.visualization(self.orderedList, True)
	
	
	def sort(self, raw_pipe_out):
		local_buffer = []										#declines the local buffer as an empty array
		Slist = {}											#declines Slist as an empty list
		Llist = {}											#declines Llist as an empty list
		AClist = {}											#declines AClist as an empty list
		Dlist = {}											#declines Dlist as an empty list
		
		while(not raw_pipe_out.poll()):									#pollingprocess
			sleep(0.05)										#waittime for polling
		
		while(raw_pipe_out.poll()):									#polling
			data = raw_pipe_out.recv()								#receive piped data
			#print("fileWriter polling: " + str(data))
			local_buffer.append(data)								#get piped date in local buffer
			sleep(0.05)										#waittime for polling
		
		for dataPackage in local_buffer:
			for key, value in dataPackage.items():
				if (not isinstance(value, str)):
					dataPackage[key] = str(value)
			#print('fileWriter' + str(dataPackage))
			if not isinstance(dataPackage, dict):							#for when piped data wrong / not a dict
				print("Pipe-Packet ist kein Wörterbuch sondern: " + str(type(dataPackage)))
				break
			if ('rx_cnt' in dataPackage.keys()):
				Dlist = {**Dlist, **dataPackage}						#set Dlist
			elif (dataPackage['type'] == 'S Short Reply'):
				Slist = {**Slist, **dataPackage}						#set Slist
			elif (dataPackage['type'] == 'S Long Reply'):
				Llist = {**Llist, **dataPackage}						#set Llist
			elif (dataPackage['type'] == 'A/C Reply'):
				AClist = {**AClist, **dataPackage}						#set AClist
		
		
		if not (len(Dlist) < 15):									#set lvl with Dlist-data
			self.lvl = Dlist["time"] + "," + Dlist["rx_cnt"] + "," + Dlist["rx_avg_lvl"] + "," + Dlist["curr_ch_occ"] + "," + Dlist["curr_planes"] + "," + Dlist["test_tx_cnt"] + "," + Dlist["test_rx_succ_cnt_s"] + "," + Dlist["test_rx_succ_cnt_l"] + "," + Dlist["test_rx_succ_cnt_ac"] + "," + Dlist["test_succ_lvl_s"] + "," + Dlist["test_succ_lvl_l"] + "," +Dlist["test_succ_lvl_ac"] + "," +Dlist["test_avg_lvl_s"] + "," + Dlist["test_avg_lvl_l"] + "," + Dlist["test_avg_lvl_ac"] + "\n"
		
		if not (len(Slist) < 48):									#set amp = Slist-data, then add Llist-data and AClist-data
			#print({k:v for k, v in Slist.items() if v != '0'})
			self.amp = Slist["time"] + "," + Slist["type"] + "," + Slist["total"] + "," + Slist["-90"] + "," + Slist["-89"] + "," + Slist["-88"] + "," + Slist["-87"] + "," + Slist["-86"] + "," + Slist["-85"] + "," + Slist["-84"] + "," + Slist["-83"] + "," + Slist["-82"] + "," + Slist["-81"] + "," + Slist["-80"] + "," + Slist["-79"] + "," + Slist["-78"] + "," + Slist["-77"] + "," + Slist["-76"] + "," + Slist["-75"] + "," + Slist["-74"] + "," + Slist["-73"] + "," + Slist["-72"] + "," + Slist["-71"] + "," + Slist["-70"] + "," + Slist["-69"] + "," + Slist["-68"] + "," + Slist["-67"] + "," + Slist["-66"] + "," + Slist["-65"] + "," + Slist["-64"] + "," + Slist["-63"] + "," + Slist["-62"] + "," + Slist["-61"] + "," + Slist["-60"] + "," + Slist["-59"] + "," + Slist["-58"] + "," + Slist["-57"] + "," + Slist["-56"] + "," + Slist["-55"] + "," + Slist["-54"] + "," + Slist["-53"] + "," + Slist["-52"] + "," + Slist["-51"] + "," + Slist["-50"] + "," + Slist["-49"] + "," + Slist["-48"] + "," + Slist["-47"] + "," + Slist["-46"] + "\n"
		if not (len(Llist) < 48):
			self.amp = self.amp + Llist["time"]+"," + Llist["type"]+"," + Llist["total"]+"," + Llist["-90"]+"," + Llist["-89"]+"," + Llist["-88"] + "," + Llist["-87"] + "," + Llist["-86"] + "," + Llist["-85"] + "," + Llist["-84"] + "," + Llist["-83"] + "," + Llist["-82"] + "," + Llist["-81"] + "," + Llist["-80"] + "," + Llist["-79"] + "," + Llist["-78"] + "," + Llist["-77"] + "," + Llist["-76"] + "," + Llist["-75"] + "," + Llist["-74"] + "," + Llist["-73"] + "," + Llist["-72"] + "," + Llist["-71"] + "," + Llist["-70"] + "," + Llist["-69"] + "," + Llist["-68"] + "," + Llist["-67"] + "," + Llist["-66"] + "," + Llist["-65"] + "," + Llist["-64"] + "," + Llist["-63"] + "," + Llist["-62"] + "," + Llist["-61"] + "," + Llist["-60"] + "," + Llist["-59"] + "," + Llist["-58"] + "," + Llist["-57"] + "," + Llist["-56"] + "," + Llist["-55"] + "," + Llist["-54"] + "," + Llist["-53"] + "," + Llist["-52"] + "," + Llist["-51"] + "," + Llist["-50"] + "," + Llist["-49"] + "," + Llist["-48"] + "," + Llist["-47"] + "," + Llist["-46"] + "\n"
		if not (len(AClist) < 48):
			#print({k:v for k, v in AClist.items() if v != '0'})
			self.amp = self.amp + AClist["time"]+"," + AClist["type"]+"," + AClist["total"]+"," + AClist["-90"]+"," + AClist["-89"]+"," + AClist["-88"]+"," + AClist["-87"]+"," + AClist["-86"]+"," + AClist["-85"]+"," + AClist["-84"]+"," + AClist["-83"]+"," + AClist["-82"]+"," + AClist["-81"]+"," + AClist["-80"]+"," + AClist["-79"]+"," + AClist["-78"]+"," + AClist["-77"]+"," + AClist["-76"]+"," + AClist["-75"]+"," + AClist["-74"]+"," + AClist["-73"]+"," + AClist["-72"]+"," + AClist["-71"]+"," + AClist["-70"]+"," + AClist["-69"]+"," + AClist["-68"]+"," + AClist["-67"]+"," + AClist["-66"]+"," + AClist["-65"]+"," + AClist["-64"]+"," + AClist["-63"]+"," + AClist["-62"]+"," + AClist["-61"]+"," + AClist["-60"]+"," + AClist["-59"]+"," + AClist["-58"]+"," + AClist["-57"]+"," + AClist["-56"]+"," + AClist["-55"]+"," + AClist["-54"]+"," + AClist["-53"]+"," + AClist["-52"]+"," + AClist["-51"]+"," + AClist["-50"]+"," + AClist["-49"]+"," + AClist["-48"]+"," + AClist["-47"]+"," + AClist["-46"] + "\n"

		
	def run(self, in_pipe, exit):
		first_run = True
		delete_live = False
		
		while (not exit.is_set()):
			if first_run == True:
				print('Measurement started')
				delete_live = True
			first_run = False
			
			print(1)
			self.sort(in_pipe)
			print(2)
			self.write(delete_live)			
			delete_live = False
