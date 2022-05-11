from DAL.UOW import BaseModel
from gi.repository import Gtk
import inspect
from peewee import *

def add():

    pass


def remove():
    pass


def update():
    pass


def load(
        model: BaseModel,
        store: Gtk.ListStore,
        tv: Gtk.TreeView

         ):
    # Load data into ListStore
    lst = list(model.select())

    for item in lst:
        store.append((item.id, item.name))

    # Create TreeView
    tv.set_model(store)
    _, fields = get_attrs(model)
    # Create rendrers and columns
    for i,field in enumerate(fields):
        renderer = peewee_types_to_gtk_column(field[1])
        col = Gtk.TreeViewColumn(field[0],renderer,text=i)
        tv.append_column(col)

    pass

def peewee_types_to_gtk_column(ptype):
    return {
        AutoField: Gtk.CellRendererText(),
        TextField:Gtk.CellRendererText(),
        CharField:Gtk.CellRendererText()
    }[ptype]

def get_attrs(klass):
    attrs = inspect.getmembers(klass)
    members = [a for a in attrs if not (a[0].startswith('__') and a[0].endswith('__') )]
    fields = [(a[0],type(a[1])) for a in members if isinstance(a[1],Field)]
    return members,fields
