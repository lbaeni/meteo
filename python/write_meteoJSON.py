#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import meteo_data


def write_json(db_path, output_path, module, correction) :
	'''read meteo data from database and write it to a json file'''

	# read meteo data from database
	db = meteo_data.meteo_data(db_path)
	data = db.get_data(module, 2678400) # get last 31 days
#	data = db.get_data(module, 86400.*60) # get last 60 days
#	data = db.get_data(module, 86400.*100) # get last 100 days
#	data = db.get_data(module) # get all data
	db.close()

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
write_json(db_path, output_path, 'SENSORSERIALNUMBER1', [0., 0., 0., 0., 0.])
write_json(db_path, output_path, 'SENSORSERIALNUMBER2', [0., 0., 0., 0., 0.])
