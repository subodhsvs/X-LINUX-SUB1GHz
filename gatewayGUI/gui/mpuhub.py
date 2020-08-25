from gi.repository import Gtk #svs
import sys #svs
import urllib.request
from string import Template
from SensorData import SensorData
import socket
import time
import json

#################### CONSTANTS ####################
HOST = '127.0.0.1' #Localhost
SOCK_PORT = 65445  #Port for MPU Gateway application
ENABLE_SOCKET = True

DATASTATE_READY      = 0
DATASTATE_CONNECTED  = 1
DATASTATE_RECDHEADER = 2
DATASTATE_RECVDATA   = 3

uriTemplate = Template('http://cloudbridge.azurewebsites.net/api/channels/Update?id=81&writekey=4H8FPGISJKD7NAPW&ax=$ax&ay=$ay&az=$az&p=$p&t=$t&h=$h')
fo = open("DB.txt", "w+")
fo.write('OK')

#mnumber = 0
#################### FUNCTIONS ####################
def uploadData(acc_x, acc_y, acc_z, pressure, temperature, humidity):
    #conn = http.client.HTTPConnection("cloudbridge.azurewebsites.net", timeout = 100)
    uriString = uriTemplate.substitute(ax = acc_x, ay = acc_y, az = acc_z, p = pressure, t = temperature, h = humidity)
    #print(uriString)
    #conn.request("GET", uriString)
    #r1 = conn.getresponse()
    #if r1.status == 200:
    #    print("OK")
    #else:
    #    print("server status " + str(r1.status))
    ur = urllib.request.urlopen(uriString)

#This function is for testing purpose only
def sendRandomDataToCloud():
    b = 1
    #sensorData = SensorDataWithTest()
    #sensorData.initWithRandomData()
    #for counter in range(100):
        #uploadData(acc_x, acc_y, acc_z, pressure, temperature, humidity)
        #sensorData.updateWithRandomData()

def processSensorData(data):
    #this functions processeses the data recieved from client
    #mnumber += 1
    #print("message number is : " + str(mnumber))
    jsonLog = {}
    jsonLog['mydata'] = []

    sensor = SensorData()
    print('Ip Address ::'+':'.join('{:02X}'.format(a) for a in data[:8]))
    sensor.parseSensorData(data, 8)
    print(sensor.printSensorData())
    jsonLog['mydata'].append({
    'timestamp' : str(datetime.datetime.now()),
    'temperature' : temp,
    'pressure' : press,
    'humidity' : humidity,
    'acc_x' : acc_x,
    'acc_y' : acc_y,
    'acc_z' : acc_z
    })
    #add this packet data to /tmp/data.txt file which is a json file
    with open('/tmp/data.txt', 'a') as outfile:
        json.dump(jsonLog, outfile)


    fo.seek(0,0)            # set file pointer to zero to read from first position
    readVal = fo.read(2)    # read first two bytes
    if readVal == "OK":
        print('read OK')
        fo.seek(0,0)        # set file pointer to zero
        # write all data to buffer file where it can be picked by the GUI
        fo.write(str(sensor.temperature))
        fo.write("\n")
        fo.write(str(sensor.pressure))
        fo.write("\n")
        fo.write(str(sensor.humidity))
        fo.write("\n")
        fo.write(str(sensor.acc_x))
        fo.write("\n")
        fo.write(str(sensor.acc_y))
        fo.write("\n")
        fo.write(str(sensor.acc_z))
        fo.write("\n")   # write all sensor value

#    /* SUBODH: My entry point */
# I am commenting the Cloud up load for now. Lets make it configurable from
# GUI in future
#    uploadData(sensor.acc_x, sensor.acc_y, sensor.acc_z, sensor.pressure, sensor.temperature, sensor.humidity)
    time.sleep(3)

#for i in range(3):
#    uploadData(0, 0, 0, 0, 0, 0)
#################### VARIABLES & CODE  ####################
datastate = DATASTATE_READY

print("STMPU Gateway Hub Application v0.85 Started :-)")

## Add code to check internet connectivity
if ENABLE_SOCKET:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, SOCK_PORT))
    serverSocket.listen(1)
else:
    #test code
    data = bytearray([0xb , 0x51 , 0x33 , 0x33 , 0x6e , 0x34 , 0x86 , 0x34 , 0x10 , 0xfa , 0x0 , 0x20 , 0x3e , 0x0 , 0x40 , 0xe1 , 0xff , 0x5 , 0x0 , 0xe1 , 0x3 , 0x80 , 0xc , 0x0 , 0xf7 , 0xff , 0xf5 , 0xff , 0x30 , 0x3f , 0x0 , 0x90 , 0x88 , 0x0 , 0x60 , 0x47 , 0x1, 0x00])
    processSensorData(data)

#svs start
class MyWindow(Gtk.ApplicationWindow):
    # constructor for a Gtk.ApplicationWindow

    def __init__(self, app):
        Gtk.Window.__init__(self, title="SRA-SAIL Show Temperature", application=app)
        self.set_default_size(400, 200)

        # create a label
        label = Gtk.Label()
        # set the text of the label
        label.set_text("Temperature = ")
        # add the label to the window
        self.add(label)


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

#svs end

while ENABLE_SOCKET:
    if datastate == DATASTATE_READY:
        print("Waiting for client connection on port " + str(SOCK_PORT) + " ..")
        #Create connection
        clientSocket, addr = serverSocket.accept()
        print("Client connected..")
        datastate = DATASTATE_CONNECTED
        data = bytearray()

    if datastate == DATASTATE_CONNECTED:
        sendData = bytearray(1)
        sendData[0] = 1
        clientSocket.send(sendData)
        data = clientSocket.recv(1)
        if data:
            datastate = DATASTATE_RECDHEADER
            dataLen = data[0]
            dataRecd = 0
            print("Length of data to read = " + str(dataLen))
        else:
            #Socket closed
            clientSocket.close()
            datastate = DATASTATE_READY

    if datastate == DATASTATE_RECDHEADER:
        data = clientSocket.recv(dataLen)
        dataRecd = len(data)
        data = bytearray(data)
        if dataRecd == dataLen:
            print("Received data")
            print(str(data))
            # svs: Log Raw Data here
            processSensorData(data)
            # svs: Log JSON  Data in this
            datastate = DATASTATE_CONNECTED

        else:
            datastate = DATASTATE_RECVDATA
        #to handle disconnection and other errors
    if datastate == DATASTATE_RECVDATA:
        time.sleep(0.100)
        dataAdditional = clientSocket.recv(dataLen - dataRecd)
        dataRecd += len(dataAdditional)
        if(dataRecd == dataLen):
            print("Received data")
            print(str(data))
            processSensorData(data)
            datastate = DATASTATE_CONNECTED
        else:
            data.extend(bytearray(dataAdditional))



#http://cloudbridge.azurewebsites.net/api/channels/Update?id=81&writekey=4H8FPGISJKD7NAPW&ax=200&ay=400&az=600&p=200&l=50&t=37
