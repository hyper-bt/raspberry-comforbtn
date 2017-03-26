#!/usr/bin/python

import Adafruit_DHT

class DHTSensor:
    def __init__(self, type, pin):
        sensor_args = { '11': Adafruit_DHT.DHT11, '22': Adafruit_DHT.DHT22, '2302': Adafruit_DHT.AM2302 }
        self.pin = pin
        self.sensor = sensor_args[type]

    def getData(self):
        humidity, temperature = None, None
        if self.pin is not None and self.sensor is not None:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return humidity, temperature