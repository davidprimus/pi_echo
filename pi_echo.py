#!/usr/bin/python
# Must use python 2 for flask_ask
#
# pi_echo.py
	# Reports weather sensor data via a Raspberry Pi and the Amazon echo
	# BarLazyM, LLC
	# David Primus
	# Gunnison, Colorado, USA
#

# import modules
from Adafruit_BME280 import *
import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
# initialize modules
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

@ask.launch
# the Intro function is executed upon AVS skill launch
def Intro():
	# must read temperature before humidity and pressure to enable compensation
	degreesC = round(sensor.read_temperature(), 1)
	pascals = sensor.read_pressure()
	hectopascals = pascals / 100
	# convert to barometric pressure at sea level via offset based on altitude of 7810 feet
	sea_level_hectopascals = round(hectopascals+255.1508512, 1)
	humidity = round(sensor.read_humidity(), 1)
	speech_text = "The Raspberry Pi reports  " + str(degreesC) + \
		" degrees Celsius. The humidity is " + str(humidity) + \
		" percent. The pressure is " + str(sea_level_hectopascals) + " hectopascals."
	return statement(speech_text).simple_card("Raspberry Pi", speech_text)

if __name__ == '__main__':
	app.run(debug=True)
	
	
	



