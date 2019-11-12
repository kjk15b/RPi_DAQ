'''
Kolby Kiesling
Abilene Buoy Systems
11-11-2019

This program reads dummy data from an Arduino Uno and stores it locally on the Pi
Will be updated in a local GitHub
'''

import serial # only library we want right now...
import sys
import re # I forgot that I need to be searching for patterns, lol...
import datetime # for logging features

udev = "/dev/ttyACM0" # our Arduino device location

int_header = re.compile("Intensity:") # intensity header
tmp_header = re.compile("Temperature:") # temperature header

data_set = 0 # start on the 0th index for data files
# TODO: Make this adjust to the last file + 1

intensity, temp = list(), list() # our two lists to hold our data...

try:
	dev = serial.Serial(udev, 9600, timeout=1) # open the device
except:
	print("\n\n\nErrors with opening the device\n\n\n")

def lazy_log():
	try:
		data_collected = 0 # we want to count up on data collected
		while data_collected <= 10:
			print("Data collected:\t{}".format(data_collected)) # let us know where we are
			for i in range(10): # ten attempts to find the data TODO: optimize
				line = dev.readline() # read in data
				matchI = re.search("Intensity", line) # look to see if this is intensity data
				matchT = re.search("Temperature", line) # look to see if it is temperature data
				
				if matchI: # if we found intensity header
					line = re.sub(int_header, '', line) # extract the data
					try:
						intensity.append(float(line))
						print("Intensity:\t{}".format(line))
					except:
						print"\n\n\nError in float conversion\n\n\n"
				elif matchT: # if we found temperature header
					line = re.sub(tmp_header, '', line)
					try:
						temp.append(float(line))
						print("Temperature:\t{}".format(line))
					except:
						print("\n\n\nError in float conversion\n\n\n")
				else:
					print('') # empty lines to keep going

			data_collected += 1 # increment our data collected by one each time we iterate
	except:
		print("\n\n\nIssues with serial communications\n\n\n")

		# Now that we have collected our data let us look to log it internally
	try:
		#label = "data_" + str(data_set) # label our file appropriately
		prefix = "/home/pi/abs_source/data/" # prefix to find our directory
		label = prefix + str(datetime.datetime.now()) + ".csv" # TODO: Issues with first file opening, causes exception to be raised 
		f = open(label, "w") # try to create a new data file
		print("Opening:\t{}".format(label))
		for i in range(data_collected):
			f.write(str(intensity[i]) + ',' + str(temp[i]) + '\n')

		f.close() # close the file now
	except:
		print("\n\n\nError in file handeling...\n\n\n")





# demo of lazy-logging features...
for k in range(10): # cycle through ten times:
	print("Iteration:\t{}".format(k))
	lazy_log() # fetch some data
	data_set += 1 # increment our data set

