import random

#################### CONSTANTS ####################

SENSOR_TEMPERATURE_ID = 0x10
SENSOR_PRESSURE_ID = 0x20
SENSOR_HUMIDITY_ID = 0x30
SENSOR_ACCELEROMETER_ID =  0x40
SENSOR_GYROMETER_ID = 0x80
SENSOR_MAGNETOMETER_ID = 0x90

SENSOR_TEMPERATURE_RANGE        = (0, 100)
SENSOR_PRESSURE_RANGE           = (0, 1000)
SENSOR_HUMIDITY_RANGE           = (0, 100)
SENSOR_ACCELEROMETER_RANGE      = (-1000, 1000)
SENSOR_GYROMETER_RANGE          = (-1000, 1000)
SENSOR_MAGNETOMETER_RANGE       = (-1000, 1000)


#################### LOCAL FUNCTIONS ####################
def CheckValidSensorID(data):
    if data == SENSOR_TEMPERATURE_ID or data == SENSOR_PRESSURE_ID \
        or data == SENSOR_HUMIDITY_ID or data == SENSOR_ACCELEROMETER_ID \
            or data == SENSOR_GYROMETER_ID or data == SENSOR_MAGNETOMETER_ID:
        return True
    else:
        return False

def uint16FromBytes(data, offset):
    num = data[offset + 1] * 256 + data[offset]
    return num

def int16FromBytes(data, offset):
    num = data[offset + 1] * 256 + data[offset]
    #check correctness
    if num > 32767:
        num = (0xFFFF - num) * -1
    return num

def extractTemperatureData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 3:
        print("Incorrect sensor data : Temperature field!!")
        return (False, 0)
    temperature = int(int16FromBytes(data, offset + 1) / 10)
    offset += 3
    return (True, offset, temperature)

def extractPressureData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 3:
        print("Incorrect sensor data : Pressure field!!")
        return (False, 0)
    pressure = int16FromBytes(data, offset + 1)
    pressure = 980
    offset += 3
    return (True, offset, pressure)

def extractHumidityData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 3:
        print("Incorrect sensor data : Humidity field!!")
        return (False, 0)
    humidity = uint16FromBytes(data, offset + 1)
    offset += 3
    return (True, offset, humidity)

def extractAccData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 7:
        print("Incorrect sensor data : Acceleration field length!!")
        return (False, 0, 0, 0, 0)
    acc_x = int16FromBytes(data, offset + 1)
    offset += 3
    if data[offset] == (SENSOR_ACCELEROMETER_ID + 1):
        #Non concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 6:
            if data[offset + 3] == (SENSOR_ACCELEROMETER_ID + 2):
                acc_y = int16FromBytes(data, offset + 1)
                acc_z = int16FromBytes(data, offset + 4)
                offset += 6
            else:
                #This takes care of the case where acc data may
                #contain a value that coincidentally matches ACC_ID
                acc_y = int16FromBytes(data, offset + 0)
                acc_z = int16FromBytes(data, offset + 2)
                offset += 4
    else:
        #Concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 4:
            acc_y = int16FromBytes(data, offset + 0)
            acc_z = int16FromBytes(data, offset + 2)
            offset += 4
        else:
            print("Incorrect sensor data : Acceleration field length!!")
            return (False, 0, 0, 0, 0)
    return (True, offset, acc_x, acc_y, acc_z)


def extractGyrData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 7:
        print("Incorrect sensor data : Gyroscope field length!!")
        return (False, 0, 0, 0, 0)
    gyr_x = int16FromBytes(data, offset + 1)
    offset += 3
    if data[offset] == (SENSOR_GYROMETER_ID + 1):
        #Non concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 6:
            if data[offset + 3] == (SENSOR_GYROMETER_ID + 2):
                gyr_y = int16FromBytes(data, offset + 1)
                gyr_z = int16FromBytes(data, offset + 4)
                offset += 6
            else:
                #This takes care of the case where acc data may
                #contain a value that coincidentally matches ACC_ID
                gyr_y = int16FromBytes(data, offset + 0)
                gyr_z = int16FromBytes(data, offset + 2)
                offset += 4
    else:
        #Concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 4:
            gyr_y = int16FromBytes(data, offset + 0)
            gyr_z = int16FromBytes(data, offset + 2)
            offset += 4
        else:
            print("Incorrect sensor data : Gyroscope field length!!")
            return (False, 0, 0, 0, 0)
    return (True, offset, gyr_x, gyr_y, gyr_z)


def extractMagData(data, offset):
    remaining_len = len(data) - offset
    if remaining_len < 7:
        print("Incorrect sensor data : Magnetometer field length!!")
        return (False, 0, 0, 0, 0)
    mag_x = int16FromBytes(data, offset + 1)
    offset += 3
    if data[offset] == (SENSOR_MAGNETOMETER_ID + 1):
        #Non concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 6:
            if data[offset + 3] == (SENSOR_MAGNETOMETER_ID + 2):
                mag_y = int16FromBytes(data, offset + 1)
                mag_z = int16FromBytes(data, offset + 4)
                offset += 6
            else:
                #This takes care of the case where acc data may
                #contain a value that coincidentally matches ACC_ID
                mag_y = int16FromBytes(data, offset + 0)
                mag_z = int16FromBytes(data, offset + 2)
                offset += 4
    else:
        #Concise format in use
        #check minimum length requiment of 6
        if (len(data) - offset) >= 4:
            mag_y = int16FromBytes(data, offset + 0)
            mag_z = int16FromBytes(data, offset + 2)
            offset += 4
        else:
            print("Incorrect sensor data : Magnetometer field length!!")
            return (False, 0, 0, 0, 0)
    return (True, offset, mag_x, mag_y, mag_z)

#################### CLASSES ####################
class SensorData:

    def __init__(self):
        v = 1
    temperature = 0
    IsValidtemperature = False
    pressure = 0
    IsValidPressure = False
    humidity = 0
    IsValidHumidity = False
    (acc_x, acc_y, acc_z) = (0, 0, 0)
    IsValidAcceleration = False
    (gyr_x, gyr_y, gyr_z) = (0, 0, 0)
    IsValidGyroData = False
    (mag_x, mag_y, mag_z) = (0, 0, 0)
    IsValidMagnetoData = False

    def printSensorData(self):
        return "T = {}, P = {}, H = {}, Ax = {}, Ay = {}, Az = {}, Gx = {}, Gy = {}, Gz = {}, Mx = {}, My = {}, Mz = {}"\
            .format(self.temperature, self.pressure, \
                self.humidity, self.acc_x, self.acc_y, self.acc_z, self.gyr_x, self.gyr_y, self.gyr_z, \
                    self.mag_x, self.mag_y, self.mag_z)


    def parseSensorData(self, data, offset):
        isDataOutOfRange = False
        if len(data) < 3 :
            print("Incorrect sensor data : Min Length voilation!!")
            return False

        while(True):
            if len(data) - offset < 3:
                return True
            sensorID = data[offset]
            if sensorID == SENSOR_TEMPERATURE_ID:
                (self.IsValidtemperature, offset, self.temperature) = extractTemperatureData(data, offset)
                if self.temperature < SENSOR_TEMPERATURE_RANGE[0] or self.temperature > SENSOR_TEMPERATURE_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidtemperature:
                    break
            elif sensorID == SENSOR_PRESSURE_ID:
                (self.IsValidPressure, offset, self.pressure) = extractPressureData(data, offset)
                if self.pressure < SENSOR_PRESSURE_RANGE[0] or self.pressure > SENSOR_PRESSURE_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidPressure:
                    break
            elif sensorID == SENSOR_HUMIDITY_ID:
                (self.IsValidHumidity, offset, self.humidity) = extractHumidityData(data, offset)
                if self.humidity < SENSOR_HUMIDITY_RANGE[0] or self.humidity > SENSOR_HUMIDITY_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidHumidity:
                    break
            elif sensorID == SENSOR_ACCELEROMETER_ID:
                (self.IsValidAcceleration, offset, self.acc_x, self.acc_y, self.acc_z) = \
                    extractAccData(data, offset)
                if self.acc_x < SENSOR_ACCELEROMETER_RANGE[0] or self.acc_x > SENSOR_ACCELEROMETER_RANGE[1] \
                    or self.acc_y < SENSOR_ACCELEROMETER_RANGE[0] or self.acc_y > SENSOR_ACCELEROMETER_RANGE[1] \
                        or self.acc_z < SENSOR_ACCELEROMETER_RANGE[0] or self.acc_z > SENSOR_ACCELEROMETER_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidAcceleration:
                    break
            elif sensorID == SENSOR_GYROMETER_ID:
                (self.IsValidGyroData, offset, self.gyr_x, self.gyr_y, self.gyr_z) = \
                    extractGyrData(data, offset)
                if self.gyr_x < SENSOR_GYROMETER_RANGE[0] or self.gyr_x > SENSOR_GYROMETER_RANGE[1] \
                    or self.gyr_y < SENSOR_GYROMETER_RANGE[0] or self.gyr_y > SENSOR_GYROMETER_RANGE[1] \
                        or self.gyr_z < SENSOR_GYROMETER_RANGE[0] or self.gyr_z > SENSOR_GYROMETER_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidGyroData:
                    break
            elif sensorID == SENSOR_MAGNETOMETER_ID:
                (self.IsValidMagnetoData, offset, self.mag_x, self.mag_y, self.mag_z) = \
                    extractMagData(data, offset)
                if self.mag_x < SENSOR_MAGNETOMETER_RANGE[0] or self.mag_x > SENSOR_MAGNETOMETER_RANGE[1] \
                    or self.mag_y < SENSOR_MAGNETOMETER_RANGE[0] or self.mag_y > SENSOR_MAGNETOMETER_RANGE[1] \
                        or self.mag_z < SENSOR_MAGNETOMETER_RANGE[0] or self.mag_z > SENSOR_MAGNETOMETER_RANGE[1]:
                    isDataOutOfRange = True
                if not self.IsValidMagnetoData:
                    break

