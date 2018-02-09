#!/usr/bin/python
import os, sys
import yocto_meteo
import ConfigParser
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help = 'path of meteo database', default = os.path.dirname(os.path.realpath(__file__)) + '/../test/meteo.db')
arg_parser.add_argument('-c', '--config'  , help = 'config file of modules', default = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg'  )
args = arg_parser.parse_args()
db_path     = args.database
config_file = args.config

config = ConfigParser.ConfigParser()
config.optionxform = str # case sensitive options
config.read(config_file)

# get module lists
meteo_sensors = [module for module in config.sections() if config.get(module, 'type') == 'meteo' ]
buzzers       = [module for module in config.sections() if config.get(module, 'type') == 'buzzer']

for sensor in meteo_sensors :
	target = config.get(sensor, 'serial_number')
	sensor = yocto_meteo.yocto_meteo(target)
	sensor.write_currentData(db_path)
