import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,GObject

budget_product_type = [
    ("Beverages",),
    ("Bread/Bakery",),
    ("Canned/Jarred Goods ",),
    ("Dairy",),
    ("Dry/Baking Goods",),
    ("Frozen Foods",),
    ("Meat",),
    ("Produce",),
    ("Cleaners",),
    ("Paper Goods",),
    ("Personal Care ",),
    ("Electronic",),
    ("Subscriptions",),
    ("Other",),
]

budget_product_type_list_store = Gtk.ListStore.new((GObject.TYPE_STRING,))


def run(builder: Gtk.Builder):
    View.load_product_type_list(builder,budget_product_type)
    print("budget loaded")


class View:
    def load_product_type_list(builder: Gtk.Builder,items):
        budget_product_type_tv = builder.get_object("tv_product_type")
        budget_product_type_add = builder.get_object("budget_product_type_add")
        for product_type in items:
            budget_product_type_list_store.append(list(product_type))

        budget_product_type_tv.set_model(budget_product_type_list_store)
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", rendererText, text=0)
        budget_product_type_tv.append_column(column)
        budget_product_type_add.connect("pressed",lambda _:Signal.on_budget_product_type_add_clicked(builder))


class Signal:
    def on_budget_product_type_add_clicked(builder: Gtk.Builder):
        budget_product_type_list_store.append(("test",))
