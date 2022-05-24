import gi

from Helper import Dashboard_GTK
from Plugins.budget.Entities.Model import ProductType, Store, Product, InvoiceProducts, Invoice
from DAL.UOW import UOW
import Helper.Crud as Crud

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


GLADE_FILE = './Plugins/budget/budget.ui'
budget_product_type_list_store = Gtk.ListStore.new((GObject.TYPE_INT, GObject.TYPE_STRING,))
budget_store_store = Gtk.ListStore.new((GObject.TYPE_INT, GObject.TYPE_STRING,))
budget_product_store = Gtk.ListStore.new((GObject.TYPE_INT,GObject.TYPE_INT, GObject.TYPE_STRING,GObject.TYPE_STRING))
budget_invoice_store = Gtk.ListStore.new((GObject.TYPE_INT,GObject.TYPE_STRING,GObject.TYPE_FLOAT))


def run(builder: Gtk.Builder):
    UOW.db.create_tables([ProductType, Store, Product, Invoice, InvoiceProducts])
    View.load_invoice(builder)
    View.load_product(builder)
    View.load_product_type_list(builder)
    View.load_store(builder)

    # Product.insert(name='test',inventory=12,type=ProductType.get_by_id(1)).execute()
    print("budget loaded")


class View:
    def load_product(builder):
        budget_product_save = builder.get_object("budget_product_save")
        budget_product_tv = builder.get_object("tv_budget_product")
        budget_product_add = builder.get_object("budget_product_add")
        budget_product_delete = builder.get_object("budget_product_delete")

        Crud.load(Product, budget_product_store, budget_product_tv, builder, budget_product_type_combo=ProductType)
        budget_product_tv.connect("cursor-changed", lambda tree: Signal.on_budget_product_select_cursor(tree, builder))
        budget_product_save.connect("pressed", lambda _: Signal.on_budget_product_save_clicked(builder, budget_product_tv))
        budget_product_add.connect("pressed", lambda _: Signal.on_budget_product_add_clicked(builder))
        budget_product_delete.connect("pressed", lambda _: Signal.on_budget_product_delete_clicked(budget_product_tv))

    def load_store(builder: Gtk.Builder):
        budget_store_tv = builder.get_object("tv_budget_store")
        budget_store_add = builder.get_object("budget_store_add")
        budget_store_delete = builder.get_object("budget_store_delete")
        budget_store_save = builder.get_object("budget_store_save")

        Crud.load(Store, budget_store_store, budget_store_tv)

        budget_store_add.connect("pressed", lambda _: Signal.on_budget_store_add_clicked(builder))
        budget_store_delete.connect("pressed", lambda _: Signal.on_budget_store_delete_clicked(budget_store_tv))
        budget_store_save.connect("pressed", lambda _: Signal.on_budget_store_save_clicked(builder, budget_store_tv))
        budget_store_tv.connect("cursor-changed", lambda tree: Signal.on_tv_store_select_cursor_row(tree, builder))

    def load_product_type_list(builder: Gtk.Builder):
        budget_product_type_tv = builder.get_object("tv_budget_product_type")
        budget_product_type_add = builder.get_object("budget_product_type_add")
        budget_product_type_save = builder.get_object("budget_product_type_save")
        budget_product_type_delete = builder.get_object("budget_product_type_delete")

        Crud.load(ProductType, budget_product_type_list_store, budget_product_type_tv)

        budget_product_type_add.connect("pressed", lambda _: Signal.on_budget_product_type_add_clicked(builder))
        budget_product_type_save.connect("pressed", lambda _: Signal.on_budget_product_type_save_clicked(builder,budget_product_type_tv))
        budget_product_type_delete.connect("pressed", lambda _: Signal.on_budget_product_type_delete_clicked(budget_product_type_tv))
        budget_product_type_tv.connect("cursor-changed", lambda tree: Signal.on_tv_product_type_select_cursor_row(tree, builder))

    def load_invoice(builder: Gtk.Builder):
        tv_budget_incoice = builder.get_object('tv_budget_incoice')
        budget_invoice_details_button = builder.get_object("budget_invoice_details_button")

        budget_invoice_details_button.connect("pressed",lambda _:Dashboard_GTK.build_modal(builder,GLADE_FILE,'budget_invoice_detail_pop'))
        Crud.load(Invoice,budget_invoice_store,tv_budget_incoice,builder,('date'),budget_invoice_store_combo=Store)

class Signal:
    #  Store
    def on_tv_store_select_cursor_row(tree, builder: Gtk.Builder):
        Crud.select(Store, tree, builder, 'budget_store')

    def on_budget_store_save_clicked(builder, tv):
        Crud.update(Store, builder, tv, 'budget_store')

    def on_budget_store_add_clicked(builder: Gtk.Builder):
        Crud.add(Store, budget_store_store, builder, 'budget_store')

    def on_budget_store_delete_clicked(tv: Gtk.TreeView):
        Crud.remove(tv, Store)

    # product type
    def on_budget_product_type_add_clicked(builder: Gtk.Builder):
        Crud.add(ProductType, budget_product_type_list_store, builder, 'budget_product_type')

    def on_tv_product_type_select_cursor_row(tree, builder: Gtk.Builder):
        Crud.select(ProductType, tree, builder, 'budget_product_type')

    def on_budget_product_type_save_clicked(builder, tv):
        Crud.update(ProductType, builder, tv, 'budget_product_type')

    def on_budget_product_type_delete_clicked(tv: Gtk.TreeView):
        Crud.remove(tv, ProductType)

    # product
    def on_budget_product_select_cursor(tree,builder):
        Crud.select(Product,tree,builder,'budget_product')

    # TODO
    def on_budget_product_save_clicked(builder, tv):
        Crud.update(Product, builder, tv, 'budget_product')

    def on_budget_product_add_clicked(builder: Gtk.Builder):
        Crud.add(Product, budget_product_store, builder, 'budget_product')

    def on_budget_product_delete_clicked(tv: Gtk.TreeView):
        Crud.remove(tv, Product)
