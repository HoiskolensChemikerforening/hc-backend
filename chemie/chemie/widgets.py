from django import forms


class MaterializeSplitDateTimeWidget(forms.SplitDateTimeWidget):
    template_name = "components/forms/widgets/split_datetime.html"

    def __init__(self, attrs=None):
        super().__init__(
            attrs=attrs,
            date_format="%Y-%m-%d",
            time_format="%H:%M",
            date_attrs={"class": "datepicker", "data-form-control": "date"},
            time_attrs={"class": "timepicker", "data-form-control": "time"},
        )

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["label"] = getattr(self, "field_label", "")
        context["widget"]["required"] = self.is_required
        return context