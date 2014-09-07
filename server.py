#!/usr/bin/env python
import urllib2
import re
import time
import sqlite3
import sys
from datetime import datetime
import thread
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable() 

class Tuner:
	def __init__(self, ip):
		self.ip = ip
		self.conn = sqlite3.connect('ceton.db')
		self.c = self.conn.cursor()

		try: self.c.execute('CREATE TABLE tuner_log (ip text, datetime text, attribute text, number integer, value real)')
		except: "Could not create database/table"

	def log_state(self):
		date_string = str(datetime.now())
		try: 
			for i in xrange(6):
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','temperature','" + str(i) + "','" + str(self.get_temperature_i(i)) + "')")
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','transport_state','" + str(i) + "','" + str(self.get_transport_state_i(i)) + "')")
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','channel','" + str(i) + "','" + str(self.get_channel_i(i)) + "')")
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','signal_level','" + str(i) + "','" + str(self.get_signal_level_i(i)) + "')")
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','signal_snr','" + str(i) + "','" + str(self.get_signal_snr_i(i)) + "')")
				self.c.execute("INSERT INTO tuner_log VALUES ('" + self.ip + "','" + date_string + "','card_status','" + str(i) + "','" + str(self.get_card_status_i(i)) + "')")
				self.conn.commit()			
		except: print "Error querying device"

	def property_request(self, number, source, variable):
		html_result = urllib2.urlopen("http://" + self.ip + "/get_var?i=" + str(number) + "&s=" + str(source) + "&v=" + str(variable))
		parsed_result = re.sub('<[^<]+?>', '', html_result.readline()).split("}")[-1]
		html_result.close()
		return parsed_result

	def get_temperature_i(self, number):
		return self.property_request(number, "diag", "Temperature").split()[0]

	def get_transport_state_i(self, number):
		if(self.property_request(number, "av", "TransportState")=="PLAYING"): return 1 + number*0.01
		else: return 0 + number*0.01

	def get_channel_i(self, number):
		return float(self.property_request(number, "cas", "VirtualChannelNumber")) + number*0.1

	def get_signal_level_i(self, number):
		value = self.property_request(number, "diag", "Signal_Level").split()[0]
		if value == "Not": return 0 
		else: return value

	def get_signal_snr_i(self, number):
		value = self.property_request(number, "diag", "Signal_SNR").split()[0]	
		if value == "Not": return 0 
                else: return value

	def get_card_status_i(self, number):
		if(self.property_request(number, "cas", "CardStatus") == "Inserted"): return 1+number*0.01
		else: return 0+number*0.01

	def get_temperatures(self):
		temperatures = []
		for i in xrange(6):
			temperatures.append(self.get_temperature_i(i))
		return temperatures

	def get_transport_states(self):
		transport_states = []
		for i in xrange(6):
			transport_states.append(self.get_transport_state_i(i))
		return transport_states

	def get_channels(self):
		channels = []
		for i in xrange(6):
			channels.append(self.get_channel_i(i))
		return channels

	def get_signal_levels(self):
		signal_levels = []
		for i in xrange(6):
			signal_levels.append(self.get_signal_level_i(i))
		return signal_levels

	def get_signal_snrs(self):
		signal_snrs = []
		for i in xrange(6):
			signal_snrs.append(self.get_signal_snr_i(i))
		return signal_snrs


def spawn_tuner(tuner_ip, delay):
	tuner = Tuner(tuner_ip)
	print "Starting up tuner object, checking initial variables."	
	print "Temps:", tuner.get_temperatures()
	print "Transport States:", tuner.get_transport_states()
	print "Channels:", tuner.get_channels()
	print "Signal Levels:", tuner.get_signal_levels()
	print "Signal to Noise Ratio:", tuner.get_signal_snrs()
	print "CableCARD Status:", tuner.get_card_status_i(0)
	while(True):
		tuner.log_state()
		time.sleep(float(delay))

tuner_ip = sys.argv[1]
delay = sys.argv[2]

print "Logging " + tuner_ip + " with at a frequency of once every " + delay + " seconds"

thread.start_new_thread(spawn_tuner, (tuner_ip, delay,))

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/"]

httpd = server(server_address, handler)
httpd.serve_forever()
