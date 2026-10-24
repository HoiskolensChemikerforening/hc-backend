from django import template
from django import forms

register = template.Library()

@register.filter
def widget_type(bound_field):
    widget = bound_field.field.widget

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

    if isinstance(widget, forms.SplitDateTimeWidget):
        widget.field_label = bound_field.label
        return "SplitDateTimeWidget"

    return widget.__class__.__name__

@register.inclusion_tag("components/forms/form.html")
def render_form(form):
    return {"form": form}