#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import meteo_data
import argparse
import ConfigParser
import json


def write_json(db_path, output_path, module, correction, period = -1) :
	'''read meteo data from database and write it to a json file'''

	# read meteo data from database
	with meteo_data.database_handler(db_path) as db :
		data = db.get_data(module, period)

	# writing meteo data to file
	json_data = []
	i = 0
	last_timestamp = data[0][1]
	for value in data :
		if abs(value[1] - last_timestamp) > 90. :
			j = 0
			while j < int((abs(value[1] - last_timestamp) - 30.) / 60.) :
				json_data.append([last_timestamp + (j+1)*60., 'null', 'null', 'null'])
				j += 1
		json_data.append([value[1], value[2]+correction[2], value[3]+correction[3], value[4]+correction[4]])
		i = i+1
		last_timestamp = value[1]
	with open(output_path+'/'+module+'.json', 'w') as json_file :
		json.dump(json_data, json_file)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help = 'path of meteo database', default = os.path.dirname(os.path.realpath(__file__)) + '/../test/meteo.db')
arg_parser.add_argument('-c', '--config'  , help = 'config file of modules', default = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg'  )
arg_parser.add_argument('-o', '--output'  , help = 'output directory'      , default = os.path.dirname(os.path.realpath(__file__)) + '/../test'         )
arg_parser.add_argument('-p', '--period'  , help = 'time period in days'   , default = -1                                                               , type = int)
args = arg_parser.parse_args()
db_path     = args.database
config_file = args.config
output_path = args.output
period      = args.period * 86400

config = ConfigParser.ConfigParser()
config.optionxform = str # case sensitive options
config.read(config_file)

for sensor in config.sections() :
	if config.get(sensor, 'type') != 'meteo' : continue
	target = config.get(sensor, 'serial_number')
	temp_offset  = float(config.get(sensor, 'temp_offset' ))
	hum_offset   = float(config.get(sensor, 'hum_offset'  ))
	press_offset = float(config.get(sensor, 'press_offset'))
	write_json(db_path, output_path, target, [0., 0., temp_offset, hum_offset, press_offset], period)
