#!/usr/bin/python
import os, sys
import yocto_meteo
import buzzer
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

data = {}
for module in meteo_sensors :
	data[module] = {}
	target = config.get(module, 'serial_number')
	sensor = yocto_meteo.yocto_meteo(target)
	[data[module]['temp'], data[module]['hum'], data[module]['press']] = sensor.write_currentData(db_path)
	sensor.turn_beaconOff()

	# activate buzzer if temperature is above threshold
	if config.has_option(module, 'buzzer') :
		buz_name   = config.get(module  , 'buzzer'       )
		buz_target = config.get(buz_name, 'serial_number')
		buz = buzzer.buzzer(buz_target)
		temp_threshold = float(config.get(module, 'temp_threshold'))
		if data[module]['temp'] > temp_threshold :
			if not buz.get_ledPower(2) :
				buz.play_alarm()
			buz.turn_ledOff(1)
			buz.flash_led(2, 'RUN')
		else :
			buz.turn_ledOff(2)
			buz.flash_led(1, 'STILL', 1)

# compare temperature of different sensors
for module in meteo_sensors :
	if not config.has_option(module, 'temp_threshold') : continue
	reference_module = config.get(module, 'temp_threshold')
	if not reference_module in meteo_sensors : continue
	target = config.get(module, 'serial_number')
	sensor = yocto_meteo.yocto_meteo(target)
	if data[module]['temp'] > data[reference_module]['temp'] : sensor.turn_beaconOn()
	else                                                     : sensor.turn_beaconOff()
