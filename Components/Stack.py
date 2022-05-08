import importlib

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def init_stack(stack: Gtk.Stack, config: list, builder: Gtk.Builder):
    sub_title = builder.get_object("main_header_bar")
    main_stack = builder.get_object("main_stack")
    main_panned = builder.get_object("main_panned")
    on_change_visible_stack = lambda main_stack, param: Signal.on_main_stack_change(sub_title, main_stack, param)
    main_stack.connect("notify::visible-child", on_change_visible_stack)

    for page in config:
        builder.add_from_file(f"./Plugins/{page}/{page}.ui")

        spec = importlib.util.spec_from_file_location(page, f"./Plugins/{page}/{page}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.run(builder)
        window = builder.get_object(page)
        name = "label%s" % page

        stack.add_titled(window, name, page.capitalize())


class Signal:
    def on_main_stack_change(sub_title: Gtk.HeaderBar, stack: Gtk.Stack, selected):
        title = stack.child_get_property(stack.get_visible_child(), 'title')
        sub_title.set_subtitle(title)
