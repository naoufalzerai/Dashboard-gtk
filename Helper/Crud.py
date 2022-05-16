import string

from DAL.UOW import BaseModel
from gi.repository import Gtk
import inspect
from peewee import *


def add(
        model,
        store: Gtk.ListStore,
        builder: Gtk.Builder,
        prefix: string
):
    temp = model()
    _, fields = get_attrs(model)

    for i, field in enumerate(fields):
        if field[1] != AutoField:
            input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}").get_property("text")
            setattr(temp, field[0], input)

    temp.save()
    store.append(peewee_object_to_list(fields, temp))


def remove(
        tv: Gtk.TreeView,
        model
):
    selected_value, iter = tv.get_selection().get_selected()
    model.delete().where(model.id == selected_value.get_value(iter, 0)).execute()
    selected_value.remove(iter)


def update(
        model,
        builder: Gtk.Builder,
        tv:Gtk.TreeView,
        prefix: string
):
    _, fields = get_attrs(model)
    temp = model()

    selected, iter = tv.get_selection().get_selected()

    if iter is not None:
        for i, field in enumerate(fields):
            if field[1] != AutoField:
                input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}").get_property("text")
                setattr(temp, field[0], input)
                selected.set(iter, i, input)
            else:
                setattr(temp,field[0],selected.get_value(iter, 0))
    temp.save()


def load(
        model,
        store: Gtk.ListStore,
        tv: Gtk.TreeView,
        builder :Gtk.Builder = None,
        **kwargs
):
    # Load data into ListStore
    lst = list(model.select())
    _, fields = get_attrs(model)

    for item in lst:
        store.append(peewee_object_to_list(fields, item))

    # Load fk
    for key,val in kwargs.items():
        combobox = builder.get_object(key)
        temp_cmb = val.select().execute()
        model = Gtk.ListStore(str,int)

        for row in temp_cmb:
            model.append([getattr(row,'name'),getattr(row,'id')])

        combobox.set_model(model)
        renderer = Gtk.CellRendererText()
        combobox.pack_start(renderer, True)
        combobox.add_attribute(renderer, "text", 0)
        combobox.set_active(0)


        # Create TreeView
    tv.set_model(store)

    # Create renderers and columns
    for i, field in enumerate(fields):
        col = Gtk.TreeViewColumn(field[0], field[2][0], text=i)
        tv.append_column(col)


def select(
        model,
        tv: Gtk.TreeView,
        builder: Gtk.Builder,
        prefix: string
):
    selected, iter = tv.get_selection().get_selected()
    _, fields = get_attrs(model)
    if iter is not None:
        for i, field in enumerate(fields):
            value = selected.get_value(iter, i)
            if field[1] != AutoField:
                input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}")
                if input is not None:
                    if field[1].__name__ == 'ForeignKeyField':
                        # TODO set active
                        input.set_active_id(value)
                    else:
                        input.set_property("text", str(value))
                else:
                    pass
            else:
                pass


# TODO
def peewee_types_to_gtk_column(ptype):
    return {
        AutoField: (Gtk.CellRendererText(), 'input'),
        TextField: (Gtk.CellRendererText(), 'input'),
        CharField: (Gtk.CellRendererText(), 'input'),
        IntegerField:(Gtk.CellRendererText(), 'input'),
        ForeignKeyField:(Gtk.CellRendererText(), 'input'),
    }[ptype]


def get_attrs(klass):
    attrs = inspect.getmembers(klass)
    members = [a for a in attrs if not (a[0].startswith('__') and a[0].endswith('__'))]
    fields = [(a[0], type(a[1]), peewee_types_to_gtk_column(type(a[1]))) for a in members if isinstance(a[1], Field)]
    return members, fields


def peewee_object_to_list(
        fields: list,
        model: BaseModel
):
    temp = list()
    for field in fields:
        if field[1].__name__ == "ForeignKeyField" and not field[0].endswith("_id"):
            fk = getattr(model, field[0])
            temp.append(getattr(fk,"name"))
        else:
            temp.append(getattr(model, field[0]))
    return temp
