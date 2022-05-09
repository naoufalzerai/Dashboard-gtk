import sys

from DAL.UOW import UOW
from Service.Config import Config
from Components import Stack as st ,Config as cfg
import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

MAIN_STACK= "main_stack"
MAIN_WINDOW ="main"

class App(Gtk.Application):

    def __init__(self, config=[], *args, **kwargs):
        t = UOW.db
        super().__init__(*args, application_id="com.shellfox.seettings", **kwargs)

        self.config = config
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file('./app.ui')
            self.window = builder.get_object(MAIN_WINDOW)
            self.stack_bar =  builder.get_object(MAIN_STACK)
            st.init_stack(self.stack_bar,self.config.get_installed_plugin(),builder)
            cfg.init_config(builder)
            self.add_window(self.window)

        self.window.show_all()


if __name__ == '__main__':
    config = Config()
    app = App(config=config)
    app.run(sys.argv)
