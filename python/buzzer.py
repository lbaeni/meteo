#!/usr/bin/python
import os, sys
import module
# add /usr/lib/yoctopuce to the PYTHONPATH
sys.path.append(os.path.join("/usr/local/lib/yoctopuce"))
import yocto_buzzer
import yocto_led
import yocto_anbutton


class buzzer(module.module) :

	def __init__(self, target) :
		module.module.__init__(self, target)
		self.buzzer  = yocto_buzzer  .YBuzzer  .FindBuzzer  (target)
		self.led1    = yocto_led     .YLed     .FindLed     (target + '.led1')
		self.led2    = yocto_led     .YLed     .FindLed     (target + '.led2')
		self.button1 = yocto_anbutton.YAnButton.FindAnButton(target + '.anButton1')
		self.button2 = yocto_anbutton.YAnButton.FindAnButton(target + '.anButton2')


	def get_led(self, led_no) :
		if   led_no == 1 : led = self.led1
		elif led_no == 2 : led = self.led2
		else :
			self.die('LED not found!')
		return led


	def flash_led(self, led_no, mode_str = 'PANIC', luminosity = 50) :
		led = self.get_led(led_no)
		modes = ['STILL', 'RELAX', 'AWARE', 'RUN', 'CALL', 'PANIC']
		if not mode_str in modes :
			self.die('Only flash modes %s are available!' % ', '.join(modes))
		mode = getattr(yocto_led.YLed, 'BLINKING_%s' % mode_str)
		led.set_power(yocto_led.YLed.POWER_ON)
		led.set_blinking(mode)
		led.set_luminosity(luminosity)


	def turn_ledOff(self, led_no) :
		led = self.get_led(led_no)
		led.set_power(yocto_led.YLed.POWER_OFF)


	def get_ledPower(self, led_no) :
		led = self.get_led(led_no)
		return led.get_power() == yocto_led.YLed.POWER_ON


	def play_success(self) :
		self.buzzer.playNotes("200% 'G12 C E G6 E12 G2")


	def play_alarm(self) :
		self.buzzer.playNotes("A32^ A^ A^ A4^")
