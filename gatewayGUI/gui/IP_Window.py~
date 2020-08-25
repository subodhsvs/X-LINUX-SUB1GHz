import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ComboBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="IoT Gateway: Connected Nodes")

        self.maximize()

        name_store = Gtk.ListStore(int, str)
        name_store.append([1,  "Node 1: IP_Addr1"])
        name_store.append([11, "Node 2: IP_Addr2"])
        name_store.append([12, "Node 3: IP_Addr3"])
        name_store.append([2,  "Node 4: IP_Addr4"])
        name_store.append([3,  "Node 5: IP_Addr5"])
        name_store.append([31, "Node 6: IP_Addr6"])

        self.OKButton = Gtk.Button("    OK    ")
        self.OKButton.connect('clicked', self.on_ok_clicked)
        self.CancelButton = Gtk.Button("  Cancel  ")
        self.CancelButton.connect('clicked', self.on_cancel_clicked)

        MyLabel = Gtk.Label("Select Sensor Node from below list")

        name_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)

        self.fix = Gtk.Fixed()
        self.fix.put(MyLabel,40,50)
        self.fix.put(name_combo, 40, 80)
        self.fix.put(self.OKButton, 400, 80)
        self.fix.put(self.CancelButton, 400,150)
        self.add(self.fix)

    def on_changed(self, widget):
      self.label.set_label(widget.get_active_text())

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

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
    def on_ok_clicked(self, widget):
        # save the opted drop down option (Node - IP).
        import sensorDataDisplay
        gui = sensorDataDisplay.SensorDataWindow()
        gui.show_all()
        # self.destroy()

    #
    # Callback for "Cancel" button clicked.
    #
    def on_cancel_clicked(self, widget):
        self.destroy()



win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
