from __future__ import print_function
import os
import subprocess
import signal
import gi
import pmp_definitions
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject
import sys
import time
from utils import gtk_utils
from threading import Thread
# svs code begin

# svs code end

#svs start code

#svs end code

class MyWindow(Gtk.ApplicationWindow):
    # constructor for a Gtk.ApplicationWindow

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Sensor Data from Wireless Node", application=app)
#        self.set_default_size(200, 100)
#svs
        self.set_title('Sensor Data from Wireless Node')
        self.maximize()
        self.set_border_width(gtk_utils.DEFAULT_SPACE)
        self.set_position(Gtk.WindowPosition.CENTER)
        # self.connect('destroy', Gtk.Widget.destroy)
        self.connect('destroy', self.destroy)
        # self.main_grid = Gtk.Grid()
        # self.main_grid.set_row_spacing(gtk_utils.DEFAULT_SPACE)
        # self.main_grid.set_row_homogeneous(False)
        # self.main_grid.set_vexpand(True)
        # self.main_grid.set_hexpand(True)
        # self.add(self.main_grid)
        self.fix = Gtk.Fixed()

# svs code BEGIN
        self.image1 = Gtk.Image()
        self.image1.set_from_file(pmp_definitions.PMP_PATH + '/media/temperature.png')
#        self.image1.set_from_file(
#            pmp_definitions.PMP_PATH + '/media/setup_gateway_blue.png')

        self.image2 = Gtk.Image()
        self.image2.set_from_file(pmp_definitions.PMP_PATH + '/media/humidity.png')
#        self.image2.set_from_file('setup_gateway_blue.png')

        self.image3 = Gtk.Image()
        self.image3.set_from_file(pmp_definitions.PMP_PATH + '/media/accelerometer.png')
#        self.image3.set_from_file('setup_gateway_blue.png')

        self.image4 = Gtk.Image()
        self.image4.set_from_file(pmp_definitions.PMP_PATH + '/media/pressureGauge.png')
#        self.image4.set_from_file('setup_gateway_blue.png')

        self.temperatureTextBuffer = Gtk.TextBuffer()
        self.temperatureTextview = Gtk.TextView.new_with_buffer(self.temperatureTextBuffer)
        self.temperatureTextBuffer.set_text("Temperature =  NA")
        print('Log 1')


        self.temperatureTextview.set_editable(False)
        self.temperatureBox = Gtk.Box()
        self.temperatureBox.add(self.temperatureTextview)

        self.humidityTextBuffer = Gtk.TextBuffer()
        self.humidityTextview = Gtk.TextView.new_with_buffer(self.humidityTextBuffer)
        self.humidityTextBuffer.set_text("Humidity = NA")

        self.humidityTextview.set_editable(False)
        self.humidityBox = Gtk.Box()
        self.humidityBox.add(self.humidityTextview)

        self.accTextBuffer = Gtk.TextBuffer()
        self.accTextview = Gtk.TextView.new_with_buffer(self.accTextBuffer)
        self.accTextBuffer.set_text("Acceleration X,Y,Z = NA")

        self.accTextview.set_editable(False)
        self.accBox = Gtk.Box()
        self.accBox.add(self.accTextview)


        self.pressureTextBuffer = Gtk.TextBuffer()
        self.pressureTextview = Gtk.TextView.new_with_buffer(self.pressureTextBuffer)
        self.pressureTextBuffer.set_text("Pressure = NA")


        self.pressureTextview.set_editable(False)
        self.pressureBox = Gtk.Box()
        self.pressureBox.add(self.pressureTextview)

        print('Log 2')
#------------------------------------------------------------------------------#
        # self.main_grid.add(self.image1)
        # self.main_grid.attach(self.temperatureBox,0,1,1,1)
        # self.main_grid.attach(self.image2, 1, 0, 1, 1)
        # self.main_grid.attach(self.humidityBox,1,1,1,1)
        # self.main_grid.attach(self.image3, 0, 2, 1, 1)
        # self.main_grid.attach(self.accBox,0,3,1,1)
        # self.main_grid.attach(self.image4, 1, 2, 1, 1)
        # self.main_grid.attach(self.pressureBox,1,3,1,1)

        self.fix.put(self.image1, 150, 5)  # column = 100 ; row = 20
        self.fix.put(self.temperatureBox,150,170)
        self.fix.put(self.image2,450,5)
        self.fix.put(self.humidityBox,450,170)
        self.fix.put(self.image3,150,200)
        self.fix.put(self.accBox,150,365)
        self.fix.put(self.image4,450,200)
        self.fix.put(self.pressureBox,450,365)


        self.add(self.fix)


        print('Log 3')

#svs code END


# 1. define the thread, updating text in all four text booxes...
        self.update = Thread(target=self.svsFuncUpdateSensorVal)
# 2. Deamonize the thread to make it stop with the GUI
        self.update.setDaemon(True)
# 3. Start the thread
        self.update.start()

    def svsFuncUpdateSensorVal(self):
        # replace this with your thread to update the text
#        n = 1
        fo = open("/usr/local/gatewayGUI/gui/DB.txt", "r+")
        while True:
            time.sleep(1)
            fo.seek(0,0)
            readVal = fo.read(2)
            if readVal != 'OK':
                fo.seek(0,0)
                readStr = fo.read()
                SensorString = readStr.split('\n')

#            newtext = str(n)+" monkey" if n == 1 else str(n)+" monkeys"
                newtextTemp = "Temperature = " + str(SensorString[0])
                print ("Temp read = " , str(SensorString[0]))
                GObject.idle_add(self.temperatureTextBuffer.set_text, newtextTemp,
                priority=GObject.PRIORITY_DEFAULT
                )

                #prepare pressure value string
                newtextPressure = "Pressure at Node = " + str(SensorString[1])
                print ("Humidity read = " , str(SensorString[1]))
                GObject.idle_add(self.pressureTextBuffer.set_text, newtextPressure,
                priority=GObject.PRIORITY_DEFAULT
                )

                #prepare humidity value string
                newtextHumidity = "Humidity at Node = " + str(SensorString[2])
                print ("Humidity read = " , str(SensorString[2]))
                GObject.idle_add(self.humidityTextBuffer.set_text, newtextHumidity,
                priority=GObject.PRIORITY_DEFAULT
                )

                #prepare Acc value X Y Z string
                newtextACC_xyz = "ACC_X = "+str(SensorString[3])+"ACC_Y = "+str(SensorString[4])+"ACC_Z = "+str(SensorString[5])
                print ("ACC_X = "+str(SensorString[3]),"ACC_Y = "+str(SensorString[4]),
                "ACC_Z = "+str(SensorString[5]))
                GObject.idle_add(self.accTextBuffer.set_text, newtextACC_xyz,
                priority=GObject.PRIORITY_DEFAULT
                )

                #reset the file to be written by mpuhub.py
                fo.seek(0,0)
                fo.write('OK')
#            n += 1

#        self.update_button = Gtk.Button('Update')
#        self.update_button.connect('clicked', self.on_update_clicked)

#        self.close_button = Gtk.Button('Close')
#        self.close_button.connect('clicked', self.on_close_clicked)

#        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=gtk_utils.DEFAULT_SPACE)
#        self.hbox.set_homogeneous(True)
#        self.hbox.set_hexpand(True)
##        self.hbox.add(self.update_button)
#        self.hbox.add(self.close_button)
##        import mpuhub

        #svs

        # # create a label
        # label = Gtk.Label()
        # # set the text of the label
        # #tempSTR = sprint("Temperature = ", 27)
        # label.set_text("Temperature = ")
        # # add the label to the window
        # self.add(label)

    #
    # Callback for "Close" button clicked.
    #
    def on_close_clicked(self, widget):
        self.destroy()

class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        print('MyApplication.init ...')

    def do_activate(self):
        win = MyWindow(self)
        print('MyApplication.do_activate ...')
        win.show_all()

    def do_startup(self):
        print('MyApplication.do_startup ...')
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
