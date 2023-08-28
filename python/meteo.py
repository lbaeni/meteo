#!/usr/bin/python
import time
from datetime import datetime
import pandas as pd
import os, sys
import meteo_data
import meteo_influxdb
import module
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib"))
from yoctopuce import yocto_api
from yoctopuce import yocto_humidity
from yoctopuce import yocto_temperature
from yoctopuce import yocto_pressure


class meteo(module.module) :

	def __init__(self, target, location = None, db_measurement = None) :
		module.module.__init__(self, target)
		self.hum_sensor   = yocto_humidity   .YHumidity   .FindHumidity   (target+'.humidity')
		self.press_sensor = yocto_pressure   .YPressure   .FindPressure   (target+'.pressure')
		self.temp_sensor  = yocto_temperature.YTemperature.FindTemperature(target+'.temperature')
		self.logger       = yocto_api        .YDataLogger .FindDataLogger (target+'.dataLogger')
		self.location = location
		self.db_measurement = db_measurement


	def par_sensor(self, parameter) :
		if parameter == 'pres' : return getattr(self, 'press_sensor')
		return getattr(self, '%s_sensor' % parameter)


	@property
	def sensor_types(self) :
		sensor_types = ['temp', 'hum', 'pres']
		return sensor_types


	@property
	def sensors(self) :
		sensors = [self.par_sensor(sensor_type) for sensor_type in self.sensor_types]
		return sensors


	def write_currentData(self, db_path) :
		return self.process_currentData(db_path = db_path)


	def process_currentData(self, db_path = None, influxdb_config = None) :
		timestamp = time.time()
		ts        = datetime.utcfromtimestamp(timestamp)
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


	def process_logger(self, db_path = None, influxdb_config = None) :
		end = time.time() - 15
		if db_path is not None :
			raise NotImplementedError('Usage of database file not implemented yet!')
		elif influxdb_config is not None :
			if self.db_measurement is None :
				self.die('Please define measurement for InfluxDB!')
			with meteo_influxdb.database_handler(influxdb_config) as db :
				start = db.get_latestTimestamp(self.db_measurement, self.location, self.module.get_serialNumber()).timestamp()
				df = self.read_logger(start, end)
				df = df[df.index > datetime.utcfromtimestamp(start)]
				df['location'] = self.location
				df['serial'  ] = self.module.get_serialNumber()
				db.add_df(df, self.db_measurement, tag_columns = ['location', 'serial'])
		else :
			start = 0
			return self.read_logger(start, end)


	def read_logger(self, start = 0, end = 0) :
		self.check_logFrequency()
		dfs = []
		for par in self.sensor_types :
			sensor = self.par_sensor(par)
			dataset = sensor.get_recordedData(start, end)
			progress = 0
			while progress < 100 :
				progress = dataset.loadMore()
			df_par = pd.DataFrame(columns = [par])
			for data in dataset.get_measures() :
				ts = datetime.utcfromtimestamp(data.get_startTimeUTC())
				df_par.loc[ts] = [data.get_averageValue()]
			dfs.append(df_par)
		df = pd.concat(dfs, axis = 1)
		return df


	def set_logger(self, state) :
		current_state = self.logger.get_recording()
		if state != current_state :
			result = self.logger.set_recording(state)
			if result != yocto_api.YAPI.SUCCESS :
				raise Exception('Could not change logger state to %d!' % state)


	def set_logFrequency(self, frequency) :
		saveToFlash = False
		for sensor in self.sensors :
			if sensor.get_logFrequency() != frequency :
				result = sensor.set_logFrequency(frequency)
				if result != yocto_api.YAPI.SUCCESS :
					raise Exception('Could not set logger frequency to %s!' % frequency)
				saveToFlash = True
		if saveToFlash :
			result = self.module.saveToFlash()
			if result != yocto_api.YAPI.SUCCESS :
				raise Exception('Could not settings to flash!')


	def check_logFrequency(self) :
		'''check if logger frequencies are the same or OFF'''
		frequencies = [sensor.get_logFrequency() for sensor in self.sensors]
		frequencies = [frequency for frequency in frequencies if frequency != 'OFF']
		if len(list(set(frequencies))) > 1 :
			raise NotImplementedError('Different logger frequencies are not supported yet!')
		return True
