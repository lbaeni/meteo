#!/usr/bin/python
import os, sys
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib/yoctopuce"))
import yocto_api
import yocto_buzzer
import yocto_led
import yocto_anbutton


class buzzer(object) :

	def __init__(self, target) :
		errmsg = yocto_api.YRefParam()

		# Setup the API to use local USB devices
		if yocto_api.YAPI.RegisterHub("usb", errmsg) != yocto_api.YAPI.SUCCESS:
			sys.exit("init error" + errmsg.value)
		self.module = yocto_api.YModule.FindModule(target)
		if not self.module.isOnline() : self.die('device not connected')

		self.buzzer  = yocto_buzzer  .YBuzzer  .FindBuzzer  (target)
		self.led1    = yocto_led     .YLed     .FindLed     (target + '.led1')
		self.led2    = yocto_led     .YLed     .FindLed     (target + '.led2')
		self.button1 = yocto_anbutton.YAnButton.FindAnButton(target + '.anButton1')
		self.button2 = yocto_anbutton.YAnButton.FindAnButton(target + '.anButton2')


	def die(self, msg) :
		sys.exit(msg+' (check USB cable)')


	def get_led(self, led_no) :
		if   led_no == 1 : led = self.led1
		elif led_no == 2 : led = self.led2
		else :
			print '[ERROR] LED not found!'
			sys.exit(1)
		return led


	def flash_led(self, led_no, mode_str = 'PANIC') :
		led = self.get_led(led_no)
		modes = ['STILL', 'RELAX', 'AWARE', 'RUN', 'CALL', 'PANIC']
		if not mode_str in modes :
			print '[ERROR] Only flash modes %s are available!' % ', '.join(modes)
			sys.exit(1)
		mode = getattr(yocto_led.YLed, 'BLINKING_%s' % mode_str)
		led.set_power(yocto_led.YLed.POWER_ON)
		led.set_blinking(mode)


	def turn_ledOff(self, led_no) :
		led = self.get_led(led_no)
		led.set_power(yocto_led.YLed.POWER_OFF)


	def play_success(self) :
		self.buzzer.playNotes("200% 'G12 C E G6 E12 G2")
