#!/usr/bin/env python
import numpy
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import datetime
import sqlite3
import uuid
import time 
import os

def plot_attribute(c, attribute, title, ylabel):
	fig = plt.figure()
	plt.margins(0,0.2)
	graph = fig.add_subplot(111)

	plt.ylabel(ylabel)
	plt.title(title)
	for i in xrange(6):

		dates = []
		values = []
#		print datetime.datetime.time(datetime.datetime.now())
		for row in c.execute('SELECT datetime, value FROM tuner_log WHERE attribute=? AND number=?',(attribute,i)):
			dates.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
			values.append(float(row[1]))
#		print datetime.datetime.time(datetime.datetime.now())
		graph.plot_date(dates, values, '-', label="T: "+str(i))
#		print len(dates)

	graph.xaxis.set_major_locator(mpl.dates.HourLocator())
	graph.xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
	graph.xaxis.set_minor_locator(mpl.dates.MinuteLocator())
	plt.legend(ncol=3,prop={'size':8})

	filename = "images/" + str(uuid.uuid4()) + ".png"
	try:os.mkdir("images")
	except: pass
	fig.savefig(filename)
	plt.clf()
	return filename




print "Content-type: text/html"
print
print "<title>Ceton Stats</title>"
print "<body>"
conn = sqlite3.connect('ceton.db')
c = conn.cursor()

filename = []
filename.append(plot_attribute(c, "temperature", "Tuner Temperature", "Temp (C)"))
print '<img src="' + filename[-1] + '">'

filename.append(plot_attribute(c, "signal_level", "Tuner Signal Level", "Level (dBmV)"))
print '<img src="' + filename[-1] + '">'

filename.append(plot_attribute(c, "signal_snr", "Tuner Signal to Noise Ratio", "SNR (dB)"))
print '<img src="' + filename[-1] + '">'

filename.append(plot_attribute(c, "transport_state", "Tuner State (Playing/Stopped)", "State"))
print '<img src="' + filename[-1] + '">'

filename.append(plot_attribute(c, "channel", "Tuned Channel", "Channel Number"))
print '<img src="' + filename[-1] + '">'

filename.append(plot_attribute(c, "card_status", "CableCARD Status (Inserted/Undetected)", "State"))
print '<img src="' + filename[-1] + '">'

print "</body>"

