import string
from datetime import datetime

from DAL.UOW import BaseModel
from gi.repository import Gtk
import inspect
from peewee import *


def add(
        model,
        store: Gtk.ListStore,
        builder: Gtk.Builder,
        prefix: string,
        to_hide: list = ()
):
    temp = model()
    _, fields = get_attrs(model)

    for i, field in enumerate(fields):
        if field[1] != AutoField:
            input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}")
            if input is not None:
                if type(input) == Gtk.ComboBox:
                    id, val = combobox_get_selected(input)
                    setattr(temp, f"{field[0]}_id", id)
                elif field[1].field_type == 'DATETIME':
                    date = input.get_date()
                    setattr(temp, field[0], datetime(date[0], date[1], date[2]))
                elif field[1].field_type == 'INT':
                    setattr(temp, field[0], int(input.get_property("text")))
                elif field[1].field_type == 'FLOAT':
                    setattr(temp, field[0], float(input.get_property("text")))
                else:
                    setattr(temp, field[0], input.get_property("text"))
            else:
                pass

    temp.save()
    to_append = peewee_object_to_list(fields, temp, to_hide)
    store.append(to_append)


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
        tv: Gtk.TreeView,
        prefix: string,
        to_hide: list = ()
):
    _, fields = get_attrs(model)
    temp = model()

    selected, iter = tv.get_selection().get_selected()
    if iter is None:
        return
    iter_i = 0
    for i, field in enumerate(fields):
        if field[1] != AutoField:
            input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}")
            if input is not None:
                if type(input) == Gtk.ComboBox:
                    id, val = combobox_get_selected(input)
                    setattr(temp, f"{field[0]}_id", id)
                    selected.set(iter, iter_i, val)
                elif field[1].field_type == 'INT':
                    setattr(temp, field[0], int(input.get_property("text")))
                    selected.set(iter, iter_i, int(input.get_property("text")))
                elif field[1].field_type == 'FLOAT':
                    setattr(temp, field[0], float(input.get_property("text")))
                    selected.set(iter, iter_i, float(input.get_property("text")))
                elif field[1].field_type == 'DATETIME':
                    date = input.get_date()
                    setattr(temp, field[0], datetime(date[0], date[1], date[2]))
                    iter_i -= 1
                else:
                    setattr(temp, field[0], input.get_property("text"))
                    selected.set(iter, iter_i, input.get_property("text"))
            iter_i += 1
        else:
            setattr(temp, field[0], selected.get_value(iter, 0))
            iter_i += 1

    temp.save()


def load(
        model,
        store: Gtk.ListStore,
        tv: Gtk.TreeView,
        builder :Gtk.Builder = None,
        to_hide:list = (),
        where:list=(True),
        **kwargs
):
    # Load data into ListStore
    lst = list(model
               .select()
               .where(where)
               )
    _, fields = get_attrs(model)

    store.clear()

    for item in lst:
        try:
            s = peewee_object_to_list(fields, item,to_hide)
            store.append(s)
        except Exception as e:
            print(e)


    # Load fk combobox
    for key,val in kwargs.items():
        combobox = builder.get_object(key)
        temp_cmb = val.select().execute()
        modelCB = Gtk.ListStore(int,str)

        Gtk.CellLayout.clear(combobox)
        for row in temp_cmb:
            modelCB.append([getattr(row,'id'),getattr(row,'name')])

        combobox.set_model(modelCB)
        combobox.props.id_column=0
        renderer = Gtk.CellRendererText()
        combobox.pack_start(renderer, True)
        combobox.add_attribute(renderer, "text", 1)
        combobox.set_active(0)


        # Create TreeView

    tv.set_model(store)

    # Create renderers and columns
    # Remove last columns
    for c in tv.get_columns():
        tv.remove_column(c)
    i = 0
    for field in fields:
        if field[0] not in to_hide:
            col = Gtk.TreeViewColumn(field[0], field[2][0], text=i)
            col.set_sort_column_id(i)
            tv.append_column(col)
            i += 1


def select(
        model,
        tv: Gtk.TreeView,
        builder: Gtk.Builder,
        prefix: string,
        to_hide:list = (),
):
    selected, iter = tv.get_selection().get_selected()
    _, fields = get_attrs(model,to_hide)
    if iter is not None:
        for i, field in enumerate(fields):
            value = selected.get_value(iter, i)
            if field[1] != AutoField and field[0] not in to_hide:
                input = builder.get_object(f"{prefix}_{field[0]}_{field[2][1]}")
                if input is not None:
                    if type(input) == Gtk.ComboBox:
                        id, val = combobox_get_selected(input)
                        set_combobox(input,value=value)
                    elif type(input) == Gtk.Entry:
                        input.set_property("text", str(value))
            else:
                pass

def combobox_get_selected(combo):
    model = combo.get_model()
    active =combo.get_active()
    return model[active][0],model[active][1]

def set_combobox(combo,id = None,value=""):
    model =combo.get_model()
    if id is not None:
        index = [ idx for idx,mod in enumerate(model) if mod[0]==id]
    else:
        index = [idx for idx, mod in enumerate(model) if mod[1] == value]
    return combo.set_active(index[0])

# TODO
def peewee_types_to_gtk_column(ptype):
    def float_renderer():
        right = Gtk.CellRendererText()
        # right.set_property('xalign', 1.0)
        #right.set_property('editing',True)
        return  right

    return {
        AutoField: (Gtk.CellRendererText(), 'input'),
        TextField: (Gtk.CellRendererText(), 'input'),
        CharField: (Gtk.CellRendererText(), 'input'),
        IntegerField:(Gtk.CellRendererText(), 'input'),
        FloatField:(float_renderer(), 'input'),
        ForeignKeyField:(Gtk.CellRendererText(), 'combo'),
        DateTimeField: (Gtk.CellRendererText(), 'input'),
    }[ptype]


def get_attrs(klass,to_hide:list=()):
    attrs = inspect.getmembers(klass)
    members = [a for a in attrs if not (a[0].startswith('__') and a[0].endswith('__')) and not (a[0].endswith('_id') and type(a[1]) == ForeignKeyField)]
    fields = [(a[0], type(a[1]), peewee_types_to_gtk_column(type(a[1]))) for a in members if isinstance(a[1], Field) and a[0] not in to_hide]
    return members, fields


def peewee_object_to_list(
        fields: list,
        model: BaseModel,
        to_hide: list=()
):
    temp = list()
    for field in fields:
        if field[1].__name__ == "ForeignKeyField" and not field[0].endswith("_id") and field[0] not in to_hide:
            fk = getattr(model, field[0])
            temp.append(getattr(fk,"name"))
        elif field[0] not in to_hide:
            temp.append(getattr(model, field[0]))
    return temp
