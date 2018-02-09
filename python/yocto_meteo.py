#!/usr/bin/python
import time
import os, sys
import meteo_data
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib/yoctopuce"))
from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *


class yocto_meteo(object) :

	def __init__(self, target) :
		errmsg = YRefParam()

		# Setup the API to use local USB devices
		if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
			sys.exit("init error"+errmsg.value)
		self.module = YModule.FindModule(target)
		if not self.module.isOnline() : self.die('device not connected')
		self.hum_sensor   = YHumidity   .FindHumidity   (target+'.humidity')
		self.press_sensor = YPressure   .FindPressure   (target+'.pressure')
		self.temp_sensor  = YTemperature.FindTemperature(target+'.temperature')


	def die(self, msg) :
		sys.exit(msg+' (check USB cable)')


	def write_currentData(self, db_path) :
		timestamp = time.time()
		temp  = self.temp_sensor .get_currentValue()
		hum   = self.hum_sensor  .get_currentValue()
		press = self.press_sensor.get_currentValue()
		module_name = self.module.get_serialNumber()
		db = meteo_data.meteo_data(db_path)
		db.add_data(module_name, timestamp, temp, hum, press)
		db.close()
