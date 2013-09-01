#!/usr/bin/python
import sqlite3
import time
import os, sys
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/lib/yoctopuce"))
from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *


def die(msg):
	sys.exit(msg+' (check USB cable)')

def init_db(db_path) :
	global connection, cursor
	connection = sqlite3.connect(db_path + "/meteo.db")
	cursor = connection.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS meteo (
		module TEXT, timestamp REAL, temperature REAL, humidity REAL, pressure REAL)""")
	connection.commit()

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

def add_data(module_name, timestamp, temperature, humidity, pressure) :
	data = (module_name, timestamp, temperature, humidity, pressure)
	cursor.execute("INSERT INTO meteo VALUES (?, ?, ?, ?, ?)", data)
	connection.commit()

def get_latestData(period) :
	start_time = (time.time() - period,)
	cursor.execute("SELECT * FROM meteo WHERE timestamp > ?", start_time)
	data = cursor.fetchall()
	return data

def write_currentData() :
	timestamp = time.time()
	temp  = temp_sensor .get_currentValue()
	hum   = hum_sensor  .get_currentValue()
	press = press_sensor.get_currentValue()
	module_name = module.get_serialNumber()
	add_data(module_name, timestamp, temp, hum, press)

target = sys.argv[1]
db_path = sys.argv[2]
init_db(db_path)
init_module(target)
write_currentData()



connection.close()
