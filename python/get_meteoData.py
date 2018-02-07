#!/usr/bin/python
import sqlite3
import time
import os, sys
import meteo_data
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/lib/yoctopuce"))
from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *


def die(msg):
	sys.exit(msg+' (check USB cable)')

def init_module(target) :
	errmsg=YRefParam()
	# Setup the API to use local USB devices
	if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
		sys.exit("init error"+errmsg.value)
	global module
	module = YModule.FindModule(target)
	if not module.isOnline() : die('device not connected')
	global hum_sensor, temp_sensor, press_sensor
	hum_sensor   = YHumidity   .FindHumidity   (target+'.humidity')
	press_sensor = YPressure   .FindPressure   (target+'.pressure')
	temp_sensor  = YTemperature.FindTemperature(target+'.temperature')

def write_currentData() :
	timestamp = time.time()
	temp  = temp_sensor .get_currentValue()
	hum   = hum_sensor  .get_currentValue()
	press = press_sensor.get_currentValue()
	module_name = module.get_serialNumber()
	db.add_data(module_name, timestamp, temp, hum, press)

target = sys.argv[1]
db_path = sys.argv[2]
global db
db = meteo_data.meteo_data(db_path)
init_module(target)
write_currentData()



db.close()
