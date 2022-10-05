#!/usr/bin/python
import time
from datetime import datetime
import os, sys
import meteo_data
import meteo_influxdb
import module
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib"))
from yoctopuce import yocto_humidity
from yoctopuce import yocto_temperature
from yoctopuce import yocto_pressure


class meteo(module.module) :

	def __init__(self, target, location = None, db_measurement = None) :
		module.module.__init__(self, target)
		self.hum_sensor   = yocto_humidity   .YHumidity   .FindHumidity   (target+'.humidity')
		self.press_sensor = yocto_pressure   .YPressure   .FindPressure   (target+'.pressure')
		self.temp_sensor  = yocto_temperature.YTemperature.FindTemperature(target+'.temperature')
		self.location = location
		self.db_measurement = db_measurement


	def write_currentData(self, db_path) :
		return self.process_currentData(db_path = db_path)


	def process_currentData(self, db_path = None, influxdb_config = None) :
		timestamp = time.time()
		ts        = datetime.fromtimestamp(timestamp)
		temp  = self.temp_sensor .get_currentValue()
		hum   = self.hum_sensor  .get_currentValue()
		press = self.press_sensor.get_currentValue()
		module_name = self.module.get_serialNumber()
		if db_path is not None :
			with meteo_data.database_handler(db_path) as db :
				db.add_data(module_name, timestamp, temp, hum, press)
		if influxdb_config is not None :
			if self.db_measurement is None :
				self.die('Please define measurement for InfluxDB!')
			with meteo_influxdb.database_handler(influxdb_config) as db :
				db.add_data(self.db_measurement, ts, temp, hum, press, self.location, module_name)
		return {
				'timestamp'   : timestamp,
				'temperature' : temp,
				'humidity'    : hum,
				'pressure'    : press}
