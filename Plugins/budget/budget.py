import gi
from types import SimpleNamespace
from Plugins.budget.Entities.Model import ProductType, Store, Product, InvoiceProducts, Invoice
from DAL.UOW import UOW
import Helper.Crud as Crud

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject

budget_product_type_list_store = Gtk.ListStore.new((GObject.TYPE_INT, GObject.TYPE_STRING,))
budget_store_store = Gtk.ListStore.new((GObject.TYPE_INT, GObject.TYPE_STRING,))


def run(builder: Gtk.Builder):
    UOW.db.create_tables([ProductType, Store])
    View.load_product_type_list(builder)
    View.load_store(builder)
    print("budget loaded")


class View:
    def load_store(builder: Gtk.Builder):
        budget_store_tv = builder.get_object("tv_budget_store")
        Crud.load(Store, budget_store_store, budget_store_tv)

        budget_store_add = builder.get_object("budget_store_add")
        budget_store_add.connect("pressed", lambda _: Signal.on_budget_store_add_clicked(builder))

        budget_store_delete = builder.get_object("budget_store_delete")
        budget_store_delete.connect("pressed", lambda _: Signal.on_budget_store_delete_clicked(budget_store_tv))

        budget_store_save = builder.get_object("budget_store_save")
        budget_store_save.connect("pressed", lambda _: Signal.on_budget_store_save_clicked(builder,budget_store_tv))

        on_tv_store_select_cursor_row = lambda tree: Signal.on_tv_store_select_cursor_row(tree, builder)
        budget_store_tv.connect("cursor-changed", on_tv_store_select_cursor_row)

    def load_product_type_list(builder: Gtk.Builder):
        lst = list(ProductType.select())
        for item in lst:
            budget_product_type_list_store.append((item.id, item.name))
        # Product type
        budget_product_type_tv = builder.get_object("tv_budget_product_type")
        budget_product_type_add = builder.get_object("budget_product_type_add")
        budget_product_type_save = builder.get_object("budget_product_type_save")
        budget_product_type_delete = builder.get_object("budget_product_type_delete")


        budget_product_type_tv.set_model(budget_product_type_list_store)
        rendererID = Gtk.CellRendererText()
        columnID = Gtk.TreeViewColumn("#", rendererID, text=0)
        budget_product_type_tv.append_column(columnID)

        budget_product_type_tv.set_model(budget_product_type_list_store)
        rendererName = Gtk.CellRendererText()
        columnName = Gtk.TreeViewColumn("Name", rendererName, text=1)

        budget_product_type_tv.append_column(columnName)
        budget_product_type_add.connect("pressed", lambda _: Signal.on_budget_product_type_add_clicked(builder))

        on_budget_product_type_save_clicked = lambda tree: Signal.on_budget_product_type_save_clicked(builder)
        budget_product_type_save.connect("pressed", on_budget_product_type_save_clicked)

        on_budget_product_type_delete_clicked = lambda tree: Signal.on_budget_product_type_delete_clicked(builder)
        budget_product_type_delete.connect("pressed", on_budget_product_type_delete_clicked)

        on_tv_product_type_select_cursor_row = lambda tree: Signal.on_tv_product_type_select_cursor_row(tree, builder)
        budget_product_type_tv.connect("cursor-changed", on_tv_product_type_select_cursor_row)


class Signal:
    # TODO
    def on_tv_store_select_cursor_row(tree, builder: Gtk.Builder):
        Crud.select(Store,tree,builder, 'budget_store')

    def on_budget_store_save_clicked(builder,tv):
        Crud.update(Store,builder,tv,'budget_store')

    def on_budget_store_add_clicked(builder: Gtk.Builder):
        Crud.add(Store, budget_store_store, builder, 'budget_store')

    def on_budget_store_delete_clicked(tv:Gtk.TreeView):
        Crud.remove(tv,Store)

    # TODO Refactor
    def on_budget_product_type_add_clicked(builder: Gtk.Builder):
        budget_product_type_name_input = builder.get_object("budget_product_type_name_input")
        to_insert = SimpleNamespace(
            Name=budget_product_type_name_input.get_property("text")
        )
        id = ProductType.insert(name=to_insert.Name).execute()
        budget_product_type_list_store.append((id, to_insert.Name))

    # TODO Refactor
    def on_tv_product_type_select_cursor_row(tree, builder: Gtk.Builder):
        model, iter = tree.get_selection().get_selected()
        if iter is not None:
            value = model.get_value(iter, 1)
            budget_product_type_name_input = builder.get_object("budget_product_type_name_input")
            budget_product_type_name_input.set_property("text", value)

    # TODO Refactor
    def on_budget_product_type_save_clicked(builder: Gtk.Builder):
        tree = builder.get_object("tv_budget_product_type")
        model, iter = tree.get_selection().get_selected()
        budget_product_type_name_input = builder.get_object("budget_product_type_name_input")
        to_edit = SimpleNamespace(
            Id=model.get_value(iter, 0),
            Name=budget_product_type_name_input.get_property("text")
        )
        model.set(iter, 1, to_edit.Name)
        ProductType.update(name=to_edit.Name).where(ProductType.id == to_edit.Id).execute()

    # TODO Refactor
    def on_budget_product_type_delete_clicked(builder: Gtk.Builder):
        tree = builder.get_object("tv_budget_product_type")
        model, iter = tree.get_selection().get_selected()
        ProductType.delete().where(ProductType.id == model.get_value(iter, 0)).execute()
        model.remove(iter)
