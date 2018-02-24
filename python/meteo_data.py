#!/usr/bin/python
import sqlite3
import time
import os, sys


class meteo_data(object) :

	def __init__(self, db_path) :
		self.connection = sqlite3.connect(db_path)
		self.cursor = self.connection.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS meteo (
			module TEXT, timestamp REAL, temperature REAL, humidity REAL, pressure REAL)""")
		self.connection.commit()


	def add_data(self, module_name, timestamp, temperature, humidity, pressure) :
		data = (module_name, timestamp, temperature, humidity, pressure)
		self.cursor.execute("INSERT INTO meteo VALUES (?, ?, ?, ?, ?)", data)
		self.connection.commit()


	def get_latestData(self, period) :
		start_time = (time.time() - period,)
		self.cursor.execute("SELECT * FROM meteo WHERE timestamp > ?", start_time)
		data = self.cursor.fetchall()
		return data


	def get_allData(self, module) :
		return self.get_data(module)


	def get_data(self, module, period = -1) :
		if period < 0 :
			start_time = 0
		else :
			start_time = time.time() - period
		self.cursor.execute("SELECT * FROM meteo WHERE module = ? AND timestamp > ?", (module, start_time))
		data = self.cursor.fetchall()
		return data


	def close(self) :
		self.connection.close()


class database_handler(object) :
	'''context manager for the meteo database'''

	def __init__(self, db_path) :
		self.db_path = db_path


	def __enter__(self) :
		self.db = meteo_data(self.db_path)
		return self.db


	def __exit__(self, exc_type, exc_val, exc_tb) :
		self.db.close()
