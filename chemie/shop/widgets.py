from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class CheckboxMaterializeWidget(forms.CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)
        id_ = attrs["id"].split("id_")[1:]
        html = """
<label for="%(name)s">
  <input type="checkbox" name="%(name)s" id="%(id)s">
    <span></span>
</label>
        """ % {
            "name": name,
            "id": id_[0],
        }
        return mark_safe(html)
