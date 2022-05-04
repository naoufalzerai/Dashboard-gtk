import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class App(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.shellfox.seettings", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file('./app.ui')
            self.window =  builder.get_object("main")
            self.add_window(self.window)

        self.window.show_all()


if __name__ == '__main__':
    app = App()
    app.run(sys.argv)
