import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio


def init_stack(stack: Gtk.Stack, config: list, builder: Gtk.Builder):
    for page in config:
        builder.add_from_file(f"./Plugins/{page}/{page}.ui")
        window = builder.get_object(page)
        name = "label%s" % page
        title = "Page %s" % page
        stack.add_titled(window, name, title)
