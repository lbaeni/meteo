#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import meteo_data
import argparse
import ConfigParser


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

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help = 'directory of meteo database', default = os.path.dirname(os.path.realpath(__file__)) + '/../test'       )
arg_parser.add_argument('-c', '--config'  , help = 'config file of modules'     , default = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg')
arg_parser.add_argument('-o', '--output'  , help = 'output directory'           , default = os.path.dirname(os.path.realpath(__file__)) + '/../test'       )
args = arg_parser.parse_args()
db_path     = args.database
config_file = args.config
output_path = args.output

config = ConfigParser.ConfigParser()
config.optionxform = str # case sensitive options
config.read(config_file)

for sensor in config.sections() :
	if config.get(sensor, 'type') != 'meteo' : continue
	target = config.get(sensor, 'serial_number')
	temp_offset  = float(config.get(sensor, 'temp_offset' ))
	hum_offset   = float(config.get(sensor, 'hum_offset'  ))
	press_offset = float(config.get(sensor, 'press_offset'))
	write_json(db_path, output_path, target, [0., 0., temp_offset, hum_offset, press_offset])
