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

def get_allData() :
	cursor.execute("SELECT * FROM meteo")
	data = cursor.fetchall()
	return data

db_path = sys.argv[1]
output_path = sys.argv[2]
init_db(db_path)
#data = get_latestData(6000)
data = get_allData()

# writing temperature data to file
json = open(output_path + '/temperature.json', 'w')
json.write('[')
i = 0
for value in data :
	json.write('[{0},{1}]'.format(value[1], value[2]))
	i = i+1
	if i < len(data) :
		json.write(',')
json.write(']')
json.close()

# writing humidity data to file
json = open(output_path + '/humidity.json', 'w')
json.write('[')
i = 0
for value in data :
	json.write('[{0},{1}]'.format(value[1], value[3]))
	i = i+1
	if i < len(data) :
		json.write(',')
json.write(']')
json.close()

# writing pressure data to file
json = open(output_path + '/pressure.json', 'w')
json.write('[')
i = 0
for value in data :
	json.write('[{0},{1}]'.format(value[1], value[4]))
	i = i+1
	if i < len(data) :
		json.write(',')
json.write(']')
json.close()

# writing meteo data to file
json = open(output_path + '/meteo.json', 'w')
json.write('[')
i = 0
for value in data :
	json.write('[{0},{1},{2},{3}]'.format(value[1], value[2], value[3], value[4]))
	i = i+1
	if i < len(data) :
		json.write(',')
json.write(']')
json.close()


connection.close()
	
