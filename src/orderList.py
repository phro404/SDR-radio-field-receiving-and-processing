import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Userinterface:
    
    def __init__(self):
        #initialize attributes
        self.__file_path = "None"

        #initalize gui-window
        self.window = tk.Tk()
        self.window.title("radio-field-measurement")
        self.window.geometry("900x500")

        #initalize buttons
        self.first_button = tk.Button(self.window, text = "Start measurement", relief = tk.RAISED, bg = "blue",
                                    fg = "black", font = ("15"), command = self.callBack)

        self.second_button = tk.Button(self.window, text = "Plot from data", relief = tk.RAISED, width = 25, 
                                    height = 5, bg = "blue", fg = "black", font = ("15"),
                                    command = self.__openexplorer_button_action__)

        self.third_button = tk.Button(self.window, text = "Exit", relief = tk.RAISED, width = 25, height = 5, bg = "red", 
                                    fg = "black", font = ("15"), command = self.window.quit)

        #link buttons with gui-window
        self.first_button.place(relx = 0.1, rely = 0.14, relwidth = 0.370, relheight = 0.3)
        self.second_button.place(relx = 0.53, rely = 0.14, relwidth = 0.370, relheight = 0.3)
        self.third_button.place(relx = 0.1, rely = 0.54, relwidth = 0.8, relheight = 0.3)

        self.window.mainloop()  #forces the gui to stay opened, but lets the __init__-method never end

    def orderPathList(self, unorderedList):

        if ((len(unorderedList) < 2) or len(unorderedList) % 2 == 1):   #to few or an odd number of files had been selected
             tk.messagebox.showinfo("Error", "Wrong data selection, please pick again.")
             return 0

        orderedList = []
        foundflag = 0
        for  i in range(0, 24):
            for j in unorderedList:
                if (-1 != j.rfind("lvl_reply_")):   #rfind returns '-1' if element is not found
                    tempindex = j.rfind("lvl_reply_")   #rfind returns position in string if sub-string is found 

                    #generating string for hour-search
                    if(i < 10):
                        tempstr = "0" + str(i)
                    else:
                        tempstr = str(i)

                    if(-1 != j.rfind(tempstr, (tempindex + 21))):   #checking hour
                        orderedList.append(j)

                        #searching for matching amp_hist file element by element
                        for k in unorderedList:
                            if (-1 != k.rfind("amp_hist_")):
                                tempindex = k.rfind("amp_hist_")
                                if(-1 != k.rfind(tempstr, (tempindex + 20))):
                                    orderedList.append(k)
                                    foundflag = 1
                                    break

                        if (foundflag == 0):    #no matching amp_hist file found in whole list
                            tk.messagebox.showinfo("Error", "Wrong data selection, please pick again.")
                            return 0
                        else:
                            foundflag = 0

# ================================================================= Own code ==============================================================
        # Show file paths
        for i in orderedList:
            print(i)

        #=================================== Import of the relevant libraries ======================================
        import csv
        import time
        import matplotlib as mlp
        import matplotlib.pyplot as plt
        import numpy as np
        #=================================== Import of the relevant libraries ======================================


        #=================================== Implementation of all Variables =======================================
        row_counter_data_paths = 0      # Counter for the index number of orderedList
        
        row_counter_lvl_reply = 0       # Counter for all rows in the level_reply CSV file
        data_row_counter_amp_hist = 0   # Counter of all rows with useful data in the level_reply CSV file
        ac_test_rx_succ_sum = 0         # Sum of all A/C test replies, which have been received successfully
        s_long_test_rx_succ_sum = 0     # Sum of all Mode S Long test replies, which have been received successfully
        s_short_test_rx_succ_sum = 0    # Sum of all Mode S Short test replies, which have been received successfully
        test_tx_sum = 0                 # Sum of all test replies, which have been transmitted
        step_level = 1                  # Step width for the list of levels in the successrate chart
        curr_planes = 0                 # Average number of detected planes
        occupancy_channel_sum = 0       # Occupancy of the channel in s

        level_for_successrate_chart = np.arange(-90, -45, step_level)           # List of levels for the successrate chart
        counter_ac_test_replies_per_level = np.zeros(int(45/step_level))        # List with the number of all A/C test replies per level
        counter_s_long_test_replies_per_level = np.zeros(int(45/step_level))    # List with the number of all Mode S Long test replies per level
        counter_s_short_test_replies_per_level = np.zeros(int(45/step_level))   # List with the number of all Mode S Short test replies per level
        ac_test_reply_succ = np.zeros(int(45/step_level))                       # List of A/C successrate per level
        s_long_test_reply_succ = np.zeros(int(45/step_level))                   # List of Mode S Long successrate per level
        s_short_test_reply_succ = np.zeros(int(45/step_level))                  # List of Mode S Short successrate per level
     

        row_counter_amp_hist = 0        # Counter for all rows in the amp_hist CSV file
        str_time_begin = "empty"        # Start time
        str_time_end = "empty"          # End time
        all_replies_sum = 0      # Sum of all received replies
        ac_replies_sum = 0              # Sum of all A/C replies
        s_long_replies_sum = 0          # Sum of all Mode S Long replies
        s_short_replies_sum = 0         # Sum of all Mode S Short replies
       
        list_level_AC = np.zeros(45)                            # List for the current number of A/C replies
        list_level_S_long = np.zeros(45)                        # List for the current number of Mode S Long replies
        list_level_S_short = np.zeros(45)                       # List for the current number of Mode S Short replies
        level_for_distribution_chart = np.arange(-90, -45, 1)   # List of levels for flight replies
        #=================================== Implementation of all Variables =======================================


        #================================ Collecting the data from the CSV files ===================================
        for line in orderedList:  # Read Path List
   
            if (row_counter_data_paths % 2) == 0:
     
                # Read lvl_reply CSV file
                with open(orderedList[row_counter_data_paths]) as csv_data_lvl_reply:
                    lvl_reply_data = csv.reader(csv_data_lvl_reply, delimiter=';')
            
                    row_counter_lvl_reply = 0   # Reset the row counter for the level_reply CSV

                    # Fill the lists and variables with data of the level_reply CSV
                    for row in lvl_reply_data:
        
                        if row_counter_lvl_reply > 0:     # We dont't need the fisrt row, because it only includes the topics.  
            
                            for column in range(int(45/step_level)):
                                if (float(row[11]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[11]) < (level_for_successrate_chart[column] + (step_level/2))):                    
                                    if row[8] != '':
                                        counter_ac_test_replies_per_level[column] += 1                              # Count all received A/C test replies in this range
                                        ac_test_reply_succ[column] = ac_test_reply_succ[column] + float(row[8])     # Build the sum of all A/C successrates in this range
                    
                                if (float(row[10]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[10]) < (level_for_successrate_chart[column] + (step_level/2))):
                                    if row[7] != '':
                                        counter_s_long_test_replies_per_level[column] += 1                                  # Count all received Mode S Long test replies in this range
                                        s_long_test_reply_succ[column] = s_long_test_reply_succ[column] + float(row[7])     # Build the sum of all Mode S Long successrates in this range

                                if (float(row[9]) >= (level_for_successrate_chart[column] - (step_level/2))) & (float(row[9]) < (level_for_successrate_chart[column] + (step_level/2))):
                                    if row[6] != '':
                                        counter_s_short_test_replies_per_level[column] += 1                                  # Count all received Mode S Short test replies in this range
                                        s_short_test_reply_succ[column] = s_short_test_reply_succ[column] + float(row[6])    # Build the sum of all Mode S Short successrates in this range

                            ac_test_rx_succ_sum = ac_test_rx_succ_sum + int(row[5])             # Build the sum of all A/C test replies, which have been received successfully
                            s_long_test_rx_succ_sum = s_long_test_rx_succ_sum + int(row[4])     # Build the sum of all Mode S Long test replies, which have been received successfully
                            s_short_test_rx_succ_sum = s_short_test_rx_succ_sum + int(row[3])   # Build the sum of all Mode S Short test replies, which have been received successfully

                            test_tx_sum = test_tx_sum + int(row[2])                             # Build the sum of all test replies, which have been transmitted
                            curr_planes = curr_planes + int(row[12])                            # Build the sum of all numbers for detected planes
                            occupancy_channel_sum = occupancy_channel_sum + float(row[13])      # Build the sum of the hole occupancy of the channel

                        row_counter_lvl_reply += 1  # Increment the level_reply row counter
    
                    data_row_counter_amp_hist = data_row_counter_amp_hist + (row_counter_lvl_reply - 1) # Get the number of all rows with useful data
            
            else:
                
                # Read amp_hist CSV file
                with open(orderedList[row_counter_data_paths]) as csvdata_amp_hist:
                    amp_hist_data = csv.reader(csvdata_amp_hist, delimiter=',') # we need ; for reading amp_hist_2019-11-07_test

                    row_counter_amp_hist = 0    # Reset the row counter for the amp_hist CSV

                    # Fill the lists and variables with data of the amp_hist CSV file
                    for row in amp_hist_data:
           
                        if row_counter_amp_hist > 0:    # We dont't need the fisrt row, because it only includes the topics. 
            
                            # Build the sum of all A/C replies per level
                            if row[1] == "A/C Reply":
                                for column in range(45):            
                                    if row[column + 3] != '':
                                        list_level_AC[column] = list_level_AC[column] + int(row[column + 3])    
            
                            # Build the sum of all Mode S Long replies per level
                            if row[1] == "S Long Reply":
                                for column in range(45):            
                                    if row[column + 3] != '':
                                        list_level_S_long[column] = list_level_S_long[column] + int(row[column + 3])
            
                            # Build the sum of all Mode S Short replies per level
                            if row[1] == "S Short Reply":
                                for column in range(45):            
                                    if row[column + 3] != '':
                                        list_level_S_short[column] = list_level_S_short[column] + int(row[column + 3])

                            # Build the sum of all received replies
                            all_replies_sum = all_replies_sum + int(row[2])

                            # Build the sum of all A/C replies
                            if ((row[1] == "A/C Reply") & (row[2] != '')):
                                ac_replies_sum = ac_replies_sum + int(row[2])

                            # Build the sum of all Mode S Long replies
                            if ((row[1] == "S Long Reply") & (row[2] != '')):
                                s_long_replies_sum = s_long_replies_sum + int(row[2])

                            # Build the sum of all Mode S Short replies
                            if ((row[1] == "S Short Reply") & (row[2] != '')):
                                s_short_replies_sum = s_short_replies_sum + int(row[2])

                            # Remember the start time
                            if (row_counter_data_paths == 1) & (row_counter_amp_hist == 1):
                                str_time_begin = row[0]
            
                            # Remember the last timestamp
                            str_time_end = row[0]
            
                        row_counter_amp_hist += 1   # Increment the amp_hist row counter
    
            row_counter_data_paths += 1  # Increment the data_paths row counter

          
        curr_planes = int(curr_planes / data_row_counter_amp_hist)      # Estimate the average number of detected planes

        # Get the successrate for the test replies at each level
        for i in range(int(45/step_level)):
            if counter_ac_test_replies_per_level[i] == 0:
                counter_ac_test_replies_per_level[i] = 1    # If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
            ac_test_reply_succ[i] = ac_test_reply_succ[i] / counter_ac_test_replies_per_level[i]     # Estimate the A/C successrate

            if counter_s_long_test_replies_per_level[i] == 0:
                counter_s_long_test_replies_per_level[i] = 1    # If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
            s_long_test_reply_succ[i] = s_long_test_reply_succ[i] / counter_s_long_test_replies_per_level[i]     # Estimate the Mode S Long successrate

            if counter_s_short_test_replies_per_level[i] == 0:
                counter_s_short_test_replies_per_level[i] = 1    # If there or no replies at this level, the counter has to be set to 1 to aviod a devision through 0
            s_short_test_reply_succ[i] = s_short_test_reply_succ[i] / counter_s_short_test_replies_per_level[i]     # Estimate the Mode S Short successrate


        # Get the star time and the stop time as a timestamp
        time_begin = time.mktime((int(str_time_begin[0:4]), int(str_time_begin[5:7]), int(str_time_begin[8:10]), int(str_time_begin[11:13]), int(str_time_begin[14:16]), int(str_time_begin[17:19]), 0, 0, 0))
        time_end = time.mktime((int(str_time_end[0:4]), int(str_time_begin[5:7]), int(str_time_end[8:10]), int(str_time_end[11:13]), int(str_time_end[14:16]), int(str_time_end[17:19]), 0, 0, 0))
    
        # Get the time space
        time_space = int(time_end - time_begin)
        if time_space == 0:
            time_space = 1  # If there is only one data row we have to divide through 1 to avoid a devision through 0
    
        # Get the average number of replies for every type
        for column in range(45):
            list_level_AC[column] = int(list_level_AC[column]/time_space)

        for column in range(45):
            list_level_S_long[column] = int(list_level_S_long[column]/time_space)

        for column in range(45):
            list_level_S_short[column] = int(list_level_S_short[column]/time_space)
        #================================ Collecting the data from the CSV files ===================================


        #============================================= Plotting ====================================================
        plt.figure()   # Clear figure
        
        # Print the pie chart for the number of all test replies, which have been received successfully
        pie_labels_test_replies = 'failed', 'Mode S Short', 'Mode S Long', 'A/C'    # Name of slices
        pie_values_test_replies = [(test_tx_sum - ac_test_rx_succ_sum - s_long_test_rx_succ_sum - s_short_test_rx_succ_sum), s_short_test_rx_succ_sum, s_long_test_rx_succ_sum, ac_test_rx_succ_sum]    # Value of slices
        pie_colors_test_replies = ['grey', 'orange', 'red', 'lightskyblue']  # Colors of the pie chart
    
        # Create the pie chart
        axes_test_replies = plt.subplot2grid((2,2),(1,0))

        def make_autopct_for_pie_test_replies(pie_values_test_replies):
            def my_autopct_for_pie_test_replies(pct):
                total = sum(pie_values_test_replies)
                val = int(round(pct*total/100.0))
                return '{v:d} \n ({p:.2f}%)'.format(p=pct, v=val)
            return my_autopct_for_pie_test_replies
    
        axes_test_replies.pie(pie_values_test_replies, labels=pie_labels_test_replies, colors=pie_colors_test_replies, autopct=make_autopct_for_pie_test_replies(pie_values_test_replies), startangle=90)
        plt.title(f'Decoding of all test replies (abs.: {test_tx_sum})')
  

        # Print the pie chart for the number of all replies
        pie_labels_all_replies = 'Mode S Short', 'Mode S Long', 'A/C'                       # Name of slices
        pie_values_all_replies = [s_short_replies_sum, s_long_replies_sum, ac_replies_sum]  # Value of slices
        pie_colors_all_replies = ['orange', 'red', 'lightskyblue']                          # Colors of the pie chart
    
        # Create the pie chart
        axes_all_replies = plt.subplot2grid((2,2),(1,1))

        def make_autopct_for_pie_all_replies(pie_values_all_replies):
            def my_autopct_for_pie_all_replies(pct):
                total = sum(pie_values_all_replies)
                val = int(round(pct*total/100.0))
                return '{v:d} \n ({p:.2f}%)'.format(p=pct, v=val)
            return my_autopct_for_pie_all_replies

        axes_all_replies.pie(pie_values_all_replies, labels=pie_labels_all_replies, colors=pie_colors_all_replies, autopct=make_autopct_for_pie_all_replies(pie_values_all_replies), startangle=90)
        plt.title(f'Distribution of all received types \n(abs.: {all_replies_sum}; avg.: {int(all_replies_sum / time_space)} per s)')
    

        # Print the successrate of the received test replies for each level
        plt.subplot(2, 2, 1)
        plt.plot(level_for_successrate_chart, ac_test_reply_succ, '-x', color='lightskyblue')       # Create the plot
        plt.plot(level_for_successrate_chart, s_long_test_reply_succ, '-x', color='red')            # Create the plot
        plt.plot(level_for_successrate_chart, s_short_test_reply_succ, '-x', color='orange')        # Create the plot
        plt.ylabel('probability of receiving in %')                                                 # x-label
        plt.xlabel('level [dBm]')                                                                   # y-label
        plt.legend(['A/C test replies', 'Mode S Long test replies', 'Mode S Short test replies'])   # Legend
        plt.grid(True)                                                                              # Grid
        plt.title(f'Successrate of all test replies')

    
        # Print the plot for the average number of replies for every type at each level
        plt.subplot(2, 2, 2)
        plt.plot(level_for_distribution_chart, list_level_AC, 'o', color='lightskyblue')    # Print the data row for A/C
        plt.plot(level_for_distribution_chart, list_level_S_long,'s', color='red')          # Print the data row for Mode S Long
        plt.plot(level_for_distribution_chart, list_level_S_short,'^', color='orange')      # Print the data row for Mode S Short
        plt.ylabel('number of replies per s')                                               # y-label
        plt.xlabel('level [dBm]')                                                           # x-label
        plt.legend(['A/C Replies', 'Mode S Long replies', 'Mode S Short replies'])          # Legend
        plt.grid(True)                                                                      # Grid
        plt.title(f'Distribution of all replies \n(abs.: {all_replies_sum}; avg.: {int(all_replies_sum / time_space)} per s)')


        plt.suptitle(f'Evaluation for the time from {str_time_begin[0:19]} to {str_time_end[0:19]} \nOccupancy of the channel: {round(occupancy_channel_sum, 3)}s \nFlights on average: {curr_planes}', fontsize=14)
        plt.show()   # Show diagram   
        #============================================= Plotting ====================================================

        
# ================================================================= Own code ==============================================================
        return orderedList

    def __openexplorer_button_action__(self):   #method for second button, opens the file-explorer
        unorderedList = filedialog.askopenfilenames()
        self.__file_path = self.orderPathList(unorderedList)

    def callBack(self):     #method for first button, is supposed to be the link to the first main-process
        tk.messagebox.showinfo( "Lorem ipsum dolor sit amet,", "consectetur adipisici elit,")   #just a dummy
        #TODO: insert code here
      
    def get_file_path(self):    #get-method for file path
        return self.__file_path


    
