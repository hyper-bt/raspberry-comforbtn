#!/usr/bin/python
import datetime
import time
import numpy

from DHTSensor import DHTSensor
from SqliteManager import SqliteManager
from IRReansceiver import IRReansceiver

# todo add log

#config
dhtSensorId = "2302"
dhtGPIOPin = 4
dbPath = "db/"
dbFileName = "taipei-house.db"
sensorPlace = "Taipei"
sensorDelay = 10
checkCycleDefine = 1#600
checkCycleThreshold = 0
checkCycle = 1
tempThreshold = 23.0
humidityThreshold = 60.0
numberOfQueryRecord = 30
deviceState = False

dhtSensor = DHTSensor(dhtSensorId, dhtGPIOPin)
irReansceiver = IRReansceiver()
sqliteManager = SqliteManager(dbPath, dbFileName)
sqliteManager.initTable()
sqliteManager.insertPlace(sensorPlace)
try:
    while True:
        humidity, temperature = dhtSensor.getData()
        if humidity is not None and temperature is not None:
            print datetime.datetime.now(), humidity, temperature
            sqliteManager.insertSensorData(sensorPlace, temperature, humidity)
            time.sleep(sensorDelay)
        checkCycle -= 1
        if checkCycle < checkCycleThreshold:
            checkCycle = checkCycleDefine
            # get the last numberOfQueryRecord record and average it
            dbResults = sqliteManager.querySensorData("temp, humidity", sensorPlace, numberOfQueryRecord);
            if dbResults is not []:
                avgTemp = numpy.average(numpy.array(dbResults)[:,0])
                avgHumidity = numpy.average(numpy.array(dbResults)[:,1])
                # open or close heater
                if avgTemp < tempThreshold and deviceState is False:
                    irReansceiver.restartIRService()
                    irReansceiver.sendIRCommand("heater", "KEY_OPEN")
                    deviceState = True
                elif avgTemp > tempThreshold and deviceState is True:
                    irReansceiver.restartIRService()
                    irReansceiver.sendIRCommand("heater", "KEY_CLOSE")
                    deviceState = False

except KeyboardInterrupt:
    sqliteManager.disConnectDB()
    print "close process..."
