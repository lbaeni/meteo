#!/usr/bin/python
import os, sys
import time
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib"))
from yoctopuce import yocto_api


class module(object) :

	def __init__(self, target) :
		errmsg = yocto_api.YRefParam()

		# Setup the API to use local USB devices or hub on localhost
		if yocto_api.YAPI.RegisterHub("usb", errmsg) != yocto_api.YAPI.SUCCESS:
			if yocto_api.YAPI.RegisterHub("127.0.0.1", errmsg) != yocto_api.YAPI.SUCCESS :
				self.die("Initialisation error. " + errmsg.value)
		self.module = yocto_api.YModule.FindModule(target)
		if not self.module.isOnline() :
			self.die('Device %s not connected (check USB cable)!' % target)


	def die(self, msg) :
		sys.exit('[ERROR] %s: %s' % (time.strftime('%a %d %b %Y %H:%M:%S'), msg))


	def turn_beaconOn(self) :
		self.module.set_beacon(yocto_api.YModule.BEACON_ON)


	def turn_beaconOff(self) :
		self.module.set_beacon(yocto_api.YModule.BEACON_OFF)
