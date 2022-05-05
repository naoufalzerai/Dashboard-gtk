import importlib

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def init_stack(stack: Gtk.Stack, config: list, builder: Gtk.Builder):
    for page in config:
        builder.add_from_file(f"./Plugins/{page}/{page}.ui")

        spec = importlib.util.spec_from_file_location(page, f"./Plugins/{page}/{page}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        window = builder.get_object(page)
        name = "label%s" % page
        title = "Page %s" % page
        stack.add_titled(window, name, title)
