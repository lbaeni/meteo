from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class meteo_influxdb(object) :

	def __init__(self, db_config) :
		self.url    = db_config['url'   ]
		self.token  = db_config['token' ]
		self.org    = db_config['org'   ]
		self.bucket = db_config['bucket']
		self.client = InfluxDBClient(url = self.url, token = self.token, org = self.org)
		self.write_api = self.client.write_api(write_options = SYNCHRONOUS)


	def add_data(self, measurement, timestamp, temperature, humidity, pressure, location, serial) :
		point = Point(measurement) \
				.tag('location', location) \
				.tag('serial'  , serial  ) \
				.field('temp', temperature) \
				.field('hum' , humidity   ) \
				.field('pres', pressure   ) \
				.time(timestamp, WritePrecision.S)
		self.write_api.write(self.bucket, self.org, point)


	def close(self) :
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
