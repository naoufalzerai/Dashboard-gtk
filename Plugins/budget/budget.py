import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

budget_product_type =[
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

def run(builder : Gtk.Builder):
    budget_product_type_list_store = builder.get_object("budget_product_type_list_store")
    # budget_product_type_list_store =Gtk.ListStore(str, int, str)
    for product_type in budget_product_type:
        budget_product_type_list_store.append(list(product_type))
    print("budget loaded")
