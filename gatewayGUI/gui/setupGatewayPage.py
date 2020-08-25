import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SetupGateway(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="IoT Gateway: Connected Nodes")

        self.maximize()


        self.ConfigWiFi = Gtk.Button(" Configure Wi-Fi ")
        self.ConfigWiFi.connect('clicked', self.on_ConfigWiFi_clicked)

        self.SaveNClose = Gtk.Button("  Save and Close  ")
        self.SaveNClose.connect('clicked', self.on_SaveNClose_clicked)

        self.ReadMe = Gtk.Button("  README  ")
        self.ReadMe.connect('clicked', self.on_ReadMe_clicked)

        self.MyLabel = Gtk.Label("Setup Gateway")

        self.EnableIoT = Gtk.CheckButton()
        self.EnableIoT.set_label('Enable IoT (Cloud) operation')
        # self.wifi_button.set_active(False)
        self.EnableIoT.set_active(False)
        self.EnableIoT.connect('toggled', self.on_EnableIoT_toggled)


        self.EnableLogging = Gtk.CheckButton()
        self.EnableLogging.set_label('Enable Logging(/tmp/GateayLogFile)')
        self.EnableLogging.set_active(True)
        self.EnableLogging.connect('toggled', self.on_EnableLogging_toggled)

        # name_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        # name_combo.connect("changed", self.on_name_combo_changed)
        # name_combo.set_entry_text_column(1)

        self.fix = Gtk.Fixed()
        self.fix.put(self.MyLabel,300,10)
        self.fix.put(self.EnableIoT,100, 100)
        self.fix.put(self.EnableLogging,100, 150)
        self.fix.put(self.ReadMe,500,120)
        # self.fix.put(name_combo, 40, 80)
        self.fix.put(self.ConfigWiFi, 100, 300)
        self.fix.put(self.SaveNClose, 400,300)
        self.add(self.fix)

    def on_changed(self, widget):
      self.label.set_label(widget.get_active_text())

    # def on_name_combo_changed(self, combo):
    #     tree_iter = combo.get_active_iter()
    #     if tree_iter is not None:
    #         model = combo.get_model()
    #         row_id, name = model[tree_iter][:2]
    #         print("Selected: ID=%d, name=%s" % (row_id, name))
    #     else:
    #         entry = combo.get_child()
    #         print("Entered: %s" % entry.get_text())

    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)

    def on_currency_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
    #
    # Callback for "OK" button clicked.
    #
    def on_ConfigWiFi_clicked(self, widget):
        # save the opted drop down option (Node - IP).
        print("Config WiFi page clicked")
        import configWiFiPage
        gui = configWiFiPage.configWiFiPage()
        gui.show_all()
        # self.destroy()

    #
    # Callback for "Cancel" button clicked.
    #
    def on_SaveNClose_clicked(self, widget):
        # svs: write your code to save the state of selected options
        # and then destroy this GUI window
        self.destroy()

    def on_ReadMe_clicked(self,widget):
        print("Function : on_ReadMe_clicked() \n")
        # svs: write your code to open a README window which would have imporatant info

    def on_EnableLogging_toggled(self,widget):
        print("Function : on_EnableLogging_toggled() \n")
        # self.destroy()
        # svs: write your code here

    def on_EnableIoT_toggled(self,widget):
        print("Function : on_EnableIoT_toggled() \n")
        # svs: write your code here


# win = SetupGateway()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()
