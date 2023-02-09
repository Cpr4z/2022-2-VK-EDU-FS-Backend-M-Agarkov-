def add_field_placeholders(form):
    for field_name, field in form.fields.items():
        form.fields[field_name].widget.attrs['placeholder'] = field.label
    return form
