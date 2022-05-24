def build_modal(builder, glade_file_path, modal_name):
    pop = builder.get_object(modal_name)
    if pop is None:
        builder.add_objects_from_file(glade_file_path, [modal_name])
        pop = builder.get_object(modal_name)
    result = pop.run()
    pop.hide()
    return result
