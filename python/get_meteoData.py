#!/usr/bin/python
import os, sys
import yocto_meteo


target = sys.argv[1]
db_path = sys.argv[2]
sensor = yocto_meteo.yocto_meteo(target)
sensor.write_currentData(db_path)
