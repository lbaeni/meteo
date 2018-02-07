#!/usr/bin/python
import os, sys
import yocto_meteo
import ConfigParser


db_path = os.path.dirname(os.path.realpath(__file__)) + '/../test'
config_file = os.path.dirname(os.path.realpath(__file__)) + '/../modules.cfg'
config = ConfigParser.ConfigParser()
config.optionxform = str # case sensitive options
config.read(config_file)
print config.sections()

for sensor in config.sections() :
	if config.get(sensor, 'type') != 'meteo' : continue
	target = config.get(sensor, 'serial_number')
	sensor = yocto_meteo.yocto_meteo(target)
	sensor.write_currentData(db_path)
