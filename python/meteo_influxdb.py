from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd


class meteo_influxdb(object) :

	def __init__(self, db_config) :
		self.url    = db_config['url'   ]
		self.token  = db_config['token' ]
		self.org    = db_config['org'   ]
		self.bucket = db_config['bucket']
		self.client = InfluxDBClient(url = self.url, token = self.token, org = self.org)
		self.write_api = self.client.write_api(write_options = SYNCHRONOUS)


	def add_data(self, measurement, timestamp, temperature, humidity, pressure, location = None, serial = None) :
		point = Point(measurement)
		if location is not None : point.tag('location', location)
		if serial   is not None : point.tag('serial'  , serial  )
		point.field('temp', temperature)
		point.field('hum' , humidity   )
		point.field('pres', pressure   )
		point.time(timestamp, WritePrecision.S)
		self.write_api.write(self.bucket, self.org, point)


	def add_df(self, df, measurement, tag_columns = []) :
		self.write_api.write(self.bucket, self.org, df, write_precision = WritePrecision.S, data_frame_measurement_name = measurement, data_frame_tag_columns = tag_columns)


	def get_latestData(self, measurement, location = None, serial = None) :
		requirements = ''
		if serial   != None : requirements += ' and r.serial == "%s"'   % serial
		if location != None : requirements += ' and r.location == "%s"' % location
		query = f'from(bucket: "%s") |> range(start: 0, stop: now()) |>  filter(fn: (r) => r._measurement == "%s"%s) |> sort(columns: ["_time"], desc: false) |> last(column: "_time") |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")' % (self.bucket, measurement, requirements)
		df = self.client.query_api().query_data_frame(query = query, org = self.org)
		return df


	def get_latestTimestamp(self, measurement, location = None, serial = None) :
		df = self.get_latestData(measurement, location, serial)
		if len(df.index) == 1 :
			timestamp = df.loc[0, '_time']
			return timestamp
		elif len(df.index) == 0 :
			return pd.Timestamp('1970-01-01T00:00:00Z')
		elif len(df.index) > 1 :
			timestamp = df.sort_values(by = '_time')._time.iloc[0]
			return timestamp


	def close(self) :
		self.write_api.close()
		self.client.close()


class database_handler(object) :
	'''context manager for the meteo database'''

	def __init__(self, db_config) :
		self.db_config = db_config


	def __enter__(self) :
		self.db = meteo_influxdb(self.db_config)
		return self.db


	def __exit__(self, exc_type, exc_val, exc_tb) :
		self.db.close()
