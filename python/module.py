#!/usr/bin/python
import os, sys
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib/yoctopuce"))
import yocto_api


class module(object) :

	def __init__(self, target) :
		errmsg = yocto_api.YRefParam()

		# Setup the API to use local USB devices
		if yocto_api.YAPI.RegisterHub("usb", errmsg) != yocto_api.YAPI.SUCCESS:
			sys.exit("init error" + errmsg.value)
		self.module = yocto_api.YModule.FindModule(target)
		if not self.module.isOnline() : self.die('device not connected')


	def die(self, msg) :
		sys.exit(msg+' (check USB cable)')
