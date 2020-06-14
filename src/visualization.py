#=================================== Import of the relevant libraries ======================================
import csv
import time
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import subprocess, sys
#=================================== Import of the relevant libraries ======================================

def visualization(orderedList, livePlot):
	
	print('visualization started')
	
	if livePlot == True:
		mlp.use('Agg') 
	else:
		mlp.use('TkAgg')
	
	#=================================== Implementation of all Variables =======================================
	row_counter_data_paths = 0		# Counter for the index number of orderedList
		
	row_counter_lvl_reply = 0		# Counter for all rows in the level_reply CSV file
	data_row_counter_lvl_reply = 0		# Counter of all rows with useful data in the level_reply CSV file
	ac_test_rx_succ_sum = 0			# Sum of all A/C test replies, which have been received successfully
	s_long_test_rx_succ_sum = 0		# Sum of all Mode S Long test replies, which have been received successfully
	s_short_test_rx_succ_sum = 0		# Sum of all Mode S Short test replies, which have been received successfully
	test_tx_sum = 0				# Sum of all test replies, which have been transmitted
	step_level = 1				# Step width for the list of levels in the successrate chart (max = 1 !!!)
	curr_planes = 0				# Average number of detected planes
	occupancy_channel = 0			# Occupancy of the channel in s

	level_for_successrate_chart = np.arange(-90, -45, step_level)		# List of levels for the successrate chart
	counter_ac_test_replies_per_level = np.zeros(int(45/step_level))	# List with the number of all A/C test replies per level
	counter_s_long_test_replies_per_level = np.zeros(int(45/step_level))	# List with the number of all Mode S Long test replies per level
	counter_s_short_test_replies_per_level = np.zeros(int(45/step_level))   # List with the number of all Mode S Short test replies per level
	ac_test_reply_succ = np.zeros(int(45/step_level))			# List of A/C successrate per level
	s_long_test_reply_succ = np.zeros(int(45/step_level))			# List of Mode S Long successrate per level
	s_short_test_reply_succ = np.zeros(int(45/step_level))			# List of Mode S Short successrate per level


	row_counter_amp_hist = 0	# Counter for all rows in the amp_hist CSV file
	str_time_begin = "empty"	# Start time
	str_time_end = "empty"		# End time
	time_begin = 0			# Start time as timestamp
	time_end = 0			# End time as timestamp
	time_space = 0			# Time space
	all_replies_sum = 0		# Sum of all received replies
	ac_replies_sum = 0		# Sum of all A/C replies
	s_long_replies_sum = 0		# Sum of all Mode S Long replies
	s_short_replies_sum = 0		# Sum of all Mode S Short replies
	   
	list_level_AC = np.zeros(45)				# List for the current number of A/C replies
	list_level_S_long = np.zeros(45)			# List for the current number of Mode S Long replies
	list_level_S_short = np.zeros(45)			# List for the current number of Mode S Short replies
	level_for_distribution_chart = np.arange(-90, -45, 1)	# List of levels for flight replies
	#=================================== Implementation of all Variables =======================================

	
	#================================ Collecting the data from the CSV files ===================================
	for line in orderedList:	# Read Path List
   
		if (row_counter_data_paths % 2) == 0:
	 
			# Read lvl_reply CSV file:
			with open(orderedList[row_counter_data_paths]) as csv_data_lvl_reply:
				lvl_reply_data = csv.reader(csv_data_lvl_reply, delimiter=',')
			
				row_counter_lvl_reply = 0	# Reset the row counter for the level_reply CSV

				# Fill the lists and variables with data of the level_reply CSV:
				for row in lvl_reply_data:
		
					if row_counter_lvl_reply > 0:	# We dont't need the fisrt row, because it only includes the topics.  
			
						for column in range(int(45/step_level)):
							if (float(row[14]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[14]) < (level_for_successrate_chart[column] + (step_level/2))):					
								if row[11] != '':
									counter_ac_test_replies_per_level[column] += 1					# Count all received A/C test replies in this range
									ac_test_reply_succ[column] = ac_test_reply_succ[column] + float(row[11])	# Build the sum of all A/C successrates in this range
					
							if (float(row[13]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[13]) < (level_for_successrate_chart[column] + (step_level/2))):
								if row[10] != '':
									counter_s_long_test_replies_per_level[column] += 1					# Count all received Mode S Long test replies in this range
									s_long_test_reply_succ[column] = s_long_test_reply_succ[column] + float(row[10])	# Build the sum of all Mode S Long successrates in this range

							if (float(row[12]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[12]) < (level_for_successrate_chart[column] + (step_level/2))):
								if row[9] != '':
									counter_s_short_test_replies_per_level[column] += 1					# Count all received Mode S Short test replies in this range
									s_short_test_reply_succ[column] = s_short_test_reply_succ[column] + float(row[9])	# Build the sum of all Mode S Short successrates in this range

						ac_test_rx_succ_sum = ac_test_rx_succ_sum + int(row[8])			# Build the sum of all A/C test replies, which have been received successfully
						s_long_test_rx_succ_sum = s_long_test_rx_succ_sum + int(row[7])	 	# Build the sum of all Mode S Long test replies, which have been received successfully
						s_short_test_rx_succ_sum = s_short_test_rx_succ_sum + int(row[6])	# Build the sum of all Mode S Short test replies, which have been received successfully

						test_tx_sum = test_tx_sum + int(row[5])					# Build the sum of all test replies, which have been transmitted
						curr_planes = curr_planes + int(row[4])					# Build the sum of all numbers for detected planes
						occupancy_channel = occupancy_channel + float(row[3])	   		# Build the sum of the hole occupancy of the channel

					row_counter_lvl_reply += 1  # Increment the level_reply row counter
	
				data_row_counter_lvl_reply = data_row_counter_lvl_reply + (row_counter_lvl_reply - 1) # Get the number of all rows with useful data
			
		else:
				
			# Read amp_hist CSV file
			with open(orderedList[row_counter_data_paths]) as csvdata_amp_hist:
				amp_hist_data = csv.reader(csvdata_amp_hist, delimiter=',')

				row_counter_amp_hist = 0	# Reset the row counter for the amp_hist CSV

				# Fill the lists and variables with data of the amp_hist CSV file:
				for row in amp_hist_data:
		   
					if row_counter_amp_hist > 0:	# We dont't need the fisrt row, because it only includes the topics. 
			
						# Build the sum of all A/C replies per level:
						if row[1] == "A/C Reply":
							for column in range(45):			
								if row[column + 3] != '':
									list_level_AC[column] = list_level_AC[column] + int(row[column + 3])	
			
						# Build the sum of all Mode S Long replies per level:
						if row[1] == "S Long Reply":
							for column in range(45):			
								if row[column + 3] != '':
									list_level_S_long[column] = list_level_S_long[column] + int(row[column + 3])
			
						# Build the sum of all Mode S Short replies per level:
						if row[1] == "S Short Reply":
							for column in range(45):			
								if row[column + 3] != '':
									list_level_S_short[column] = list_level_S_short[column] + int(row[column + 3])

						# Build the sum of all received replies:
						all_replies_sum = all_replies_sum + int(row[2])

						# Build the sum of all A/C replies:
						if ((row[1] == "A/C Reply") & (row[2] != '')):
							ac_replies_sum = ac_replies_sum + int(row[2])

						# Build the sum of all Mode S Long replies:
						if ((row[1] == "S Long Reply") & (row[2] != '')):
							s_long_replies_sum = s_long_replies_sum + int(row[2])

						# Build the sum of all Mode S Short replies:
						if ((row[1] == "S Short Reply") & (row[2] != '')):
							s_short_replies_sum = s_short_replies_sum + int(row[2])

						# Remember the start time:
						if (row_counter_data_paths == 1) & (row_counter_amp_hist == 1):
							str_time_begin = row[0]
			
						# Remember the last timestamp:
						str_time_end = row[0]
			
					row_counter_amp_hist += 1	# Increment the amp_hist row counter
	
		row_counter_data_paths += 1	# Increment the data_paths row counter

		
	if data_row_counter_lvl_reply == 0:
		data_row_counter_lvl_reply = 1						# If the file is empty, the counter has to be set to 1 to aviod a devision through 0
	curr_planes = float(curr_planes / data_row_counter_lvl_reply)			# Estimate the average number of detected planes
	occupancy_channel = float(occupancy_channel / data_row_counter_lvl_reply)	# Estimate the average occupancy of the channel
	
	# Get the successrate for the test replies at each level:
	for i in range(int(45/step_level)):
		if counter_ac_test_replies_per_level[i] == 0:
			counter_ac_test_replies_per_level[i] = 1						# If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
		ac_test_reply_succ[i] = float(ac_test_reply_succ[i] / counter_ac_test_replies_per_level[i])	# Estimate the A/C successrate

		if counter_s_long_test_replies_per_level[i] == 0:
			counter_s_long_test_replies_per_level[i] = 1							# If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
		s_long_test_reply_succ[i] = float(s_long_test_reply_succ[i] / counter_s_long_test_replies_per_level[i])	# Estimate the Mode S Long successrate

		if counter_s_short_test_replies_per_level[i] == 0:
			counter_s_short_test_replies_per_level[i] = 1								# If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
		s_short_test_reply_succ[i] = float(s_short_test_reply_succ[i] / counter_s_short_test_replies_per_level[i])	# Estimate the Mode S Short successrate

	
	########################################################################################################
        '''
        import configparser
	
        class TelegramProcessing:
        	def __init__(self):
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
        '''
        ########################################################################################################

	# Get the star time and the stop time as a timestamp:
	time_begin = time.mktime((int(str_time_begin[0:4]), int(str_time_begin[5:7]), int(str_time_begin[8:10]), int(str_time_begin[11:13]), int(str_time_begin[14:16]), int(str_time_begin[17:19]), 0, 0, 0))
	time_end = time.mktime((int(str_time_end[0:4]), int(str_time_begin[5:7]), int(str_time_end[8:10]), int(str_time_end[11:13]), int(str_time_end[14:16]), int(str_time_end[17:19]), 0, 0, 0))
	
	# Get the time space:
	time_space = int(time_end - time_begin)
	time_space_for_plot = time_space
	if time_space == 0:
		time_space = 1	# If there is only one data row we have to divide through 1 to avoid a devision through 0
	
	# Get the average number of replies for every type:
	for column in range(45):
		list_level_AC[column] = float(list_level_AC[column]/time_space)

	for column in range(45):
		list_level_S_long[column] = float(list_level_S_long[column]/time_space)

	for column in range(45):
		list_level_S_short[column] = float(list_level_S_short[column]/time_space)
	#================================ Collecting the data from the CSV files ===================================
	
	
	#============================================= Plotting ====================================================
	if livePlot == True:
		plt.rcParams["figure.figsize"] = (12, 7)	# Size of the plot frame
		plt.clf()				   	# When "livePlot == True" then overwrite the old plot
	else:
		f, axs = plt.subplots(2,2,figsize=(12, 7))  	# When "livePlot == False" then create a new plot; Also includes the size of the plot frame
	
	
	# Print the pie chart for the number of all test replies, which have been received successfully:
	pie_labels_test_replies = 'failed', 'Mode S Short', 'Mode S Long', 'A/C'	# Name of slices
	pie_values_test_replies = [(test_tx_sum - ac_test_rx_succ_sum - s_long_test_rx_succ_sum - s_short_test_rx_succ_sum), s_short_test_rx_succ_sum, s_long_test_rx_succ_sum, ac_test_rx_succ_sum]	# Values of slices
	pie_colors_test_replies = ['grey', 'orange', 'red', 'lightskyblue']		# Colors of the pie chart
	
	# Create the pie chart:
	axes_test_replies = plt.subplot2grid((2,2),(1,0))

	def make_autopct_for_pie_test_replies(pie_values_test_replies):
		def my_autopct_for_pie_test_replies(pct):
			total = sum(pie_values_test_replies)
			val = int(round(pct*total/100.0))
			return '{v:d} \n ({p:.2f}%)'.format(p=pct, v=val)
		return my_autopct_for_pie_test_replies
	
	axes_test_replies.pie(pie_values_test_replies, labels=pie_labels_test_replies, colors=pie_colors_test_replies, autopct=make_autopct_for_pie_test_replies(pie_values_test_replies), startangle=90, textprops={'fontsize': 8})
	plt.title(f'Decoding of all send test replies \n(abs.: {test_tx_sum}; avg.: {round((test_tx_sum / time_space), 2)} per s)')
  
	
	# Print the pie chart for the number of all replies:
	pie_labels_all_replies = 'Mode S Short', 'Mode S Long', 'A/C'				# Name of slices
	pie_values_all_replies = [s_short_replies_sum, s_long_replies_sum, ac_replies_sum]	# Values of slices
	pie_colors_all_replies = ['orange', 'red', 'lightskyblue']				# Colors of the pie chart
	
	# Create the pie chart:
	axes_all_replies = plt.subplot2grid((2,2),(1,1))

	def make_autopct_for_pie_all_replies(pie_values_all_replies):
		def my_autopct_for_pie_all_replies(pct):
			total = sum(pie_values_all_replies)
			val = int(round(pct*total/100.0))
			return '{v:d} \n ({p:.2f}%)'.format(p=pct, v=val)
		return my_autopct_for_pie_all_replies

	axes_all_replies.pie(pie_values_all_replies, labels=pie_labels_all_replies, colors=pie_colors_all_replies, autopct=make_autopct_for_pie_all_replies(pie_values_all_replies), startangle=90, textprops={'fontsize': 8})
	plt.title(f'Distribution of all received types \n(abs.: {all_replies_sum}; avg.: {round((all_replies_sum / time_space), 2)} per s)')
	

	# Print the successrate of the received test replies for each level:
	plt.subplot(2, 2, 1)
	plt.plot(level_for_successrate_chart, ac_test_reply_succ, '-x', color='lightskyblue')		# Create the plot
	plt.plot(level_for_successrate_chart, s_long_test_reply_succ, '-x', color='red')		# Create the plot
	plt.plot(level_for_successrate_chart, s_short_test_reply_succ, '-x', color='orange')		# Create the plot
	plt.ylabel('probability of receiving in %')							# x-label
	plt.xlabel('level [dBm]')									# y-label
	plt.legend(['A/C test replies', 'Mode S Long test replies', 'Mode S Short test replies'])	# Legend
	plt.grid(True)											# Grid
	plt.title(f'Successrate of all test replies')

	
	# Print the plot for the average number of replies for every type at each level:
	plt.subplot(2, 2, 2)
	plt.plot(level_for_distribution_chart, list_level_AC, 'o', color='lightskyblue')	# Print the data row for A/C
	plt.plot(level_for_distribution_chart, list_level_S_long,'s', color='red')		# Print the data row for Mode S Long
	plt.plot(level_for_distribution_chart, list_level_S_short,'^', color='orange')	  	# Print the data row for Mode S Short
	plt.ylabel('number of replies per s')							# y-label
	plt.xlabel('level [dBm]')								# x-label
	plt.legend(['A/C Replies', 'Mode S Long replies', 'Mode S Short replies'])		# Legend
	plt.grid(True)										# Grid
	plt.title(f'Distribution of all replies \n(abs.: {all_replies_sum}; avg.: {round((all_replies_sum / time_space), 2)} per s)')
		
	plt.suptitle(f'Evaluation for the time from {str_time_begin[0:19]} to {str_time_end[0:19]} \nTime space: {round(time_space_for_plot, 2)}s \nOccupancy of the channel: {round(occupancy_channel, 2)}s \nFlights on average: {round(curr_planes, 2)}', fontsize=14)
						
	plt.subplots_adjust(left = 0.07, bottom = 0.05, right = 0.95, top = 0.75, wspace = 0.25, hspace = 0.55)	# Distances of the sobplots
	
	
	# Save and show the plots:
	str_time_current = datetime.datetime.now().isoformat()	# Get the current time as a string
		
	if livePlot == True:
		start_time_for_liveplotname = f'{str_time_begin[0:10]}_{str_time_begin[11:19]}'					# Edit the start time string
		start_time_for_liveplotname = start_time_for_liveplotname.replace(':', '-')
		plotname = orderedList[0].replace(orderedList[0][-18:], f'liveplot_begin_{start_time_for_liveplotname}.pdf')	# Create the liveplot name (apropos of the file names) 
		
		if os.path.exists(plotname):
			print('Plot exstiert')
			plt.savefig(plotname, bbox_inches = 'tight')	# Save the plot			
		else:
			print('Plot existiert nicht')
			plt.savefig(plotname, bbox_inches = 'tight')	# Save the plot
			opener = "open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, plotname])
			
	else:
		start_time_for_plotname = f'{str_time_begin[0:10]}_{str_time_begin[11:19]}'		# Edit the start time string
		start_time_for_plotname = start_time_for_plotname.replace(':', '-')
		end_time_for_plotname = f'{str_time_end[0:10]}_{str_time_end[11:19]}'			# Edit the end time string
		end_time_for_plotname = end_time_for_plotname.replace(':', '-')
		current_time_for_plotname = f'{str_time_current[0:10]}_{str_time_current[11:19]}'   	# Edit the current time string
		current_time_for_plotname = current_time_for_plotname.replace(':', '-')
		plotname = orderedList[0].replace(orderedList[0][-27:], f'plot_{start_time_for_plotname}_to_{end_time_for_plotname}_printed_{current_time_for_plotname}.pdf')	# Create the plot name
		plt.savefig(plotname, bbox_inches='tight')  # Save the plot
		plt.show()
		
	print(f'figure saved as: {plotname}')
	#============================================= Plotting ====================================================
