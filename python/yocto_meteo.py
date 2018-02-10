#!/usr/bin/python
import time
import os, sys
import meteo_data
import module
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib/yoctopuce"))
import yocto_humidity
import yocto_temperature
import yocto_pressure


class yocto_meteo(module.module) :

	def __init__(self, target) :
		module.module.__init__(self, target)
		self.hum_sensor   = yocto_humidity   .YHumidity   .FindHumidity   (target+'.humidity')
		self.press_sensor = yocto_pressure   .YPressure   .FindPressure   (target+'.pressure')
		self.temp_sensor  = yocto_temperature.YTemperature.FindTemperature(target+'.temperature')


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
		return [temp, hum, press]
