#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import meteo_data
import argparse
import ConfigParser


def write_json(db_path, output_path, module, correction, period = -1) :
	'''read meteo data from database and write it to a json file'''

	# read meteo data from database
	with meteo_data.database_handler(db_path) as db :
		data = db.get_data(module, period)

	# writing meteo data to file
	with open(output_path+'/'+module+'.json', 'w') as json :
		json.write('[')
		i = 0
		last_timestamp = data[0][1]
		for value in data :
			if abs(value[1] - last_timestamp) > 90. :
				j = 0
				while j < int((abs(value[1] - last_timestamp) - 30.) / 60.) :
					json.write('[{0}, null, null, null],\n'.format(last_timestamp + (j+1)*60.))
					j += 1
			json.write('[{0},{1},{2},{3}]'.format(value[1], value[2]+correction[2], value[3]+correction[3], value[4]+correction[4]))
			i = i+1
			if i < len(data) :
				json.write(',\n')
			last_timestamp = value[1]
		json.write(']')

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help = 'path of meteo database', default = os.path.dirname(os.path.realpath(__file__)) + '/../test/meteo.db')
arg_parser.add_argument('-c', '--config'  , help = 'config file of modules', default = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg'  )
arg_parser.add_argument('-o', '--output'  , help = 'output directory'      , default = os.path.dirname(os.path.realpath(__file__)) + '/../test'         )
arg_parser.add_argument('-p', '--period'  , help = 'time period in seconds', default = -1                                                               , type = int)
args = arg_parser.parse_args()
db_path     = args.database
config_file = args.config
output_path = args.output
period      = args.period

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
