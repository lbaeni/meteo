#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import time
import os, sys

def init_db(db_path) :
	global connection, cursor
	connection = sqlite3.connect(db_path + "/meteo.db")
	cursor = connection.cursor()
#	cursor.execute("""CREATE TABLE IF NOT EXISTS meteo (
#		module TEXT, timestamp REAL, temperature REAL, humidity REAL, pressure REAL)""")
	connection.commit()

def get_latestData(period) :
	start_time = (time.time() - period,)
	cursor.execute("SELECT * FROM meteo WHERE timestamp > ?", start_time)
	data = cursor.fetchall()
	return data

def get_allData(module) :
	return get_data(module)

def get_data(module, period = -1) :
#	print module
	if period < 0 :
		start_time = 0
	else :
		start_time = time.time() - period
	cursor.execute("SELECT * FROM meteo WHERE module = ? AND timestamp > ?", (module, start_time))
	data = cursor.fetchall()
	return data

def write_json(output_path, module, correction) :
	data = get_data(module, 2678400) # get last 31 days
#	data = get_data(module, 86400.*60) # get last 60 days
#	data = get_data(module, 86400.*100) # get last 100 days
#	data = get_data(module) # get all data
	# writing meteo data to file
	json = open(output_path+'/'+module+'.json', 'w')
	json.write('[')
	i = 0
	for value in data :
		json.write('[{0},{1},{2},{3}]'.format(value[1], value[2]+correction[2], value[3]+correction[3], value[4]+correction[4]))
		i = i+1
		if i < len(data) :
			json.write(',\n')
	json.write(']')
	json.close()

db_path = sys.argv[1]
output_path = sys.argv[2]
init_db(db_path)
write_json(output_path, 'SENSORSERIALNUMBER1', [0., 0., 0., 0., 0.])
write_json(output_path, 'SENSORSERIALNUMBER2', [0., 0., 0., 0., 0.])


connection.close()
	
