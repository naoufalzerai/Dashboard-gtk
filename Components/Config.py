import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def init_config(builder: Gtk.Builder):
    btn_config = builder.get_object("btn_config")
    on_btn_config_click=lambda _ : Signal.on_btn_config_click(builder)
    btn_config.connect("clicked", on_btn_config_click)


class Signal:
    def on_btn_config_click(builder: Gtk.Builder):

        builder.add_from_file(f"./Components/Config.ui")
        window_config = builder.get_object("window_config")
        result = window_config.run()
        window_config.hide()