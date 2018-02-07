#!/usr/bin/python
import os, sys
import yocto_meteo
import ConfigParser
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help = 'directory of meteo database', default = os.path.dirname(os.path.realpath(__file__)) + '/../test'       )
arg_parser.add_argument('-c', '--config'  , help = 'config file of modules'     , default = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg')
args = arg_parser.parse_args()
db_path     = args.database
config_file = args.config

config = ConfigParser.ConfigParser()
config.optionxform = str # case sensitive options
config.read(config_file)

for sensor in config.sections() :
	if config.get(sensor, 'type') != 'meteo' : continue
	target = config.get(sensor, 'serial_number')
	sensor = yocto_meteo.yocto_meteo(target)
	sensor.write_currentData(db_path)
