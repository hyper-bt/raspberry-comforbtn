#!/usr/bin/python
import datetime
import sqlite3

class SqliteManager:
    def __init__(self, dbPath, dbName):
        self.dbPath = dbPath
        self.dbName = dbName
        self.dbConnect = None
        self.dbCurson = None
        self.connectDB()

    def connectDB(self):
        self.dbConnect = sqlite3.connect(self.dbPath + self.dbName)
        self.dbCurson = self.dbConnect.cursor()

    def isConnectExist(self):
        if self.dbConnect is not None and self.dbCurson is not None:
            return True
        return False

    def isTableExist(self, table):
        if self.isConnectExist():
            sql = "PRAGMA table_info({table})".format(table = table)
            self.dbCurson.execute(sql)
            values = self.dbCurson.fetchone()
            if values != None:
                return True
        return False

    def initTable(self):
        if self.isConnectExist():
            am2302DataSql = "CREATE TABLE IF NOT EXISTS `sensorData` (" + \
                            "`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," + \
                            "`place` INTEGER NOT NULL," + \
                            "`datetimes` TEXT," + \
                            "`temp`  REAL," + \
                            "`humidity`  REAL);"
            placeSql = "CREATE TABLE IF NOT EXISTS `place` (" + \
                            "`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," + \
                            "`name`  TEXT);"
            self.dbCurson.execute(am2302DataSql)
            self.dbCurson.execute(placeSql)
            if self.dbCurson.rowcount == 2:
                self.dbConnect.commit()
                return True
        return False

    def disConnectDB(self):
        self.dbCurson.close()
        self.dbConnect.close()

    def insertPlace(self, place):
        if self.isConnectExist() and self.isTableExist('sensorData') and self.isTableExist('place'):
            if self.selectPlace(place) == None:
                sql = "INSERT INTO place VALUES (NULL, '{place}')".format(place = place)
                self.dbCurson.execute(sql)
                if self.dbCurson.rowcount == 1:
                    self.dbConnect.commit()
                    return True
        return False

    def insertSensorData(self, place, temp, humidity):
        if self.isConnectExist() and self.isTableExist('sensorData') and self.isTableExist('place'):
            placeId = self.selectPlace(place)[0]
            currentDatetime = datetime.datetime.now()
            if placeId != None:
                sql = "INSERT INTO sensorData VALUES (NULL, {place}, '{datetime}', '{temp}', '{humidity}')".format(\
                    place = placeId, \
                    datetime = currentDatetime, \
                    temp = temp, \
                    humidity = humidity)
                self.dbCurson.execute(sql)
                if self.dbCurson.rowcount == 1:
                    self.dbConnect.commit()
                    return True
        return False

    def selectPlace(self, place):
        if self.isConnectExist() and self.isTableExist('sensorData') and self.isTableExist('place'):
            sql = "SELECT * from place where name = '{place}'".format(place = place)
            self.dbCurson.execute(sql)
            values = self.dbCurson.fetchone()
            return values
        return None

    def querySensorData(self, fields, place, limit):
        if self.isConnectExist() and self.isTableExist('sensorData') and self.isTableExist('place'):
            sql = "select {fields} from sensorData where \
                        place = (select id from place where name = '{place}') \
                        order by id DESC limit {limit};".format( \
                            fields = fields, \
                            place = place, \
                            limit = limit)
            self.dbCurson.execute(sql)
            values = self.dbCurson.fetchall()
            return values
        return []
