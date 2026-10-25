from django import template
from django import forms

register = template.Library()

@register.filter
def widget_type(bound_field):
    widget = bound_field.field.widget
    
  
    if bound_field.errors:
        if isinstance(widget, forms.MultiWidget):
            widgets = widget.widgets
        else:
            widgets = [widget]

        for w in widgets:
            classes = w.attrs.get("class", "").split()

            if "invalid" not in classes:
                classes.append("invalid")

            w.attrs["class"] = " ".join(classes)

    if isinstance(widget, forms.Textarea):
        classes = widget.attrs.get("class", "").split()

        if "materialize-textarea" not in classes:
            classes.append("materialize-textarea")

        widget.attrs["class"] = " ".join(classes)

    if isinstance(widget, forms.CheckboxInput):
        classes = widget.attrs.get("class", "").split()
        if "filled-in" not in classes:
            classes.append("filled-in")
        widget.attrs["class"] = " ".join(classes)

    if isinstance(widget, forms.RadioSelect):
        classes = widget.attrs.get("class", "").split()

        if "with-gap" not in classes:
            classes.append("with-gap")

        widget.attrs["class"] = " ".join(classes)

    if isinstance(widget, forms.SplitDateTimeWidget):
        widget.field_label = bound_field.label
        return "SplitDateTimeWidget"

    return widget.__class__.__name__

@register.inclusion_tag("components/forms/form.html")
def render_form(form):
    return {"form": form}

@register.filter
def get_field(form, name):
    return form[name]

@register.filter
def field_icon(bound_field):
    icons = getattr(bound_field.form, "field_icons", {})
    return icons.get(bound_field.name, "")