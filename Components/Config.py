import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def init_config(builder: Gtk.Builder):
    btn_config = builder.get_object("btn_config")
    btn_config.connect("clicked", lambda _: Signal.on_btn_config_click(builder))


class Signal:
    def on_btn_config_click(builder: Gtk.Builder):
        builder.add_from_file(f"./Components/Config.ui")
        window_config = builder.get_object("window_config")

        window_config.connect("response", lambda d: Signal.on_window_config_click(d))
        window_config.connect("close", lambda d: Signal.on_window_config_click(d))
        window_config.run()

    def on_window_config_click(window_config: Gtk.Dialog):
        window_config.destroy()
