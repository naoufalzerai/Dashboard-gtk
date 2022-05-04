import sys
from Service.config import Config
from Components.Stack import init_stack
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class App(Gtk.Application):
    def __init__(self, config=[], *args, **kwargs):
        super().__init__(*args, application_id="com.shellfox.seettings", **kwargs)
        self.config = config
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file('./app.ui')
            self.window = builder.get_object("main")
            self.stack_bar =  builder.get_object("stack1")
            init_stack(self.stack_bar,self.config.menu,builder)
            self.add_window(self.window)

        self.window.show_all()


if __name__ == '__main__':
    config = Config()
    app = App(config=config)
    app.run(sys.argv)
