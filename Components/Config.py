import gi

from Helper import Dashboard_GTK

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

GLADE_FILE = "./Components/Config.ui"

def init_config(builder: Gtk.Builder):
    btn_config = builder.get_object("btn_config")
    on_btn_config_click=lambda _ : Signal.on_btn_config_click(builder)
    btn_config.connect("clicked", on_btn_config_click)


class Signal:
    def on_btn_config_click(builder: Gtk.Builder):
        res = Dashboard_GTK.build_modal(builder,GLADE_FILE,'window_config')
        print(res)