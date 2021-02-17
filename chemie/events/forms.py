import material as M
from dal import autocomplete
from django import forms
from django.core.validators import ValidationError
from extended_choices import Choices
from chemie.customprofile.models import GRADES
from .models import (
    Social,
    SocialEventRegistration,
    Bedpres,
    BedpresRegistration,
    BaseEvent,
    BaseRegistrationGroup,
)


class BaseRegisterEventForm(forms.ModelForm):
    allowed_grades = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=GRADES,
        label="Tillatte klassetrinn",
    )

    allowed_groups = forms.ModelMultipleChoiceField(
        queryset=BaseRegistrationGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Tillatte grupper",
        required=False,
    )

    def clean(self):
        super(BaseRegisterEventForm, self).clean()
        if not self.is_valid():
            return

        event_date, open_date = (
            self.cleaned_data["date"],
            self.cleaned_data["register_startdate"],
        )
        deadline, lock_in_date = (
            self.cleaned_data["register_deadline"],
            self.cleaned_data["deregister_deadline"],
        )

        if event_date < open_date:
            self.add_error(
                None,
                ValidationError(
                    {
                        "register_startdate": [
                            "Påmeldingen må være før arrangementet begynner"
                        ]
                    }
                ),
            )

        if event_date < deadline:
            self.add_error(
                None,
                ValidationError(
                    {
                        "register_deadline": [
                            "Påmeldingsfristen må være før arrangementet begynner"
                        ]
                    }
                ),
            )

        if event_date < lock_in_date:
            self.add_error(
                None,
                ValidationError(
                    {
                        "deregister_deadline": [
                            "Avmeldingsfristen må være før arrangementet begynner"
                        ]
                    }
                ),
            )

        if deadline < open_date:
            self.add_error(
                None,
                ValidationError(
                    {
                        "register_deadline": [
                            "Påmeldingsfristen må være etter påmeldingen begynner"
                        ]
                    }
                ),
            )

    def clean_allowed_grades(self):
        try:
            grades = self.cleaned_data.get("allowed_grades")
            grades = [int(grade) for grade in grades]
            _ = [GRADES.values[int(grade)] for grade in grades]
            return grades
        except (ValueError, KeyError):
            self.add_error(
                None,
                ValidationError(
                    {
                        "allowed_grades": [
                            "Tillatte klassetrinn er ikke akseptert"
                        ]
                    }
                ),
            )

    class Meta:
        abstract = True
        model = BaseEvent
        fields = [
            "title",
            "location",
            "description",
            "image",
            "sluts",
            "allowed_grades",
            "allowed_groups",
            "date",
            "register_startdate",
            "register_deadline",
            "deregister_deadline",
            "published",
        ]

        # Override field type from DateTimeField to SplitDateTimeField
        # Note that this field loads the widget from
        # chemie/templates/material/fields/django_splitdatetimewidget.html
        field_classes = {
            "date": forms.SplitDateTimeField,
            "register_startdate": forms.SplitDateTimeField,
            "register_deadline": forms.SplitDateTimeField,
            "deregister_deadline": forms.SplitDateTimeField,
        }


class RegisterEventForm(BaseRegisterEventForm):
    layout = M.Layout(
        M.Row(M.Column("published", "title")),
        M.Row("committee"),
        M.Row(
            M.Column("date", span_columns=1),
            M.Column("register_startdate", span_columns=1),
            M.Column("register_deadline", span_columns=1),
            M.Column("deregister_deadline", span_columns=1),
        ),
        M.Row("location"),
        M.Row("description"),
        M.Row("payment_information"),
        M.Row(M.Column("image"), M.Column("sluts")),
        M.Row("price_member", "price_not_member", "price_companion"),
        M.Row("companion", "sleepover", "night_snack", "check_in"),
        M.Row("allowed_grades", "allowed_groups"),
    )

    class Meta(BaseRegisterEventForm.Meta):
        model = Social
        fields = BaseRegisterEventForm.Meta.fields.copy()
        fields += [
            "committee",
            "payment_information",
            "price_member",
            "price_not_member",
            "price_companion",
            "companion",
            "sleepover",
            "night_snack",
            "check_in",
        ]


class RegisterBedpresForm(BaseRegisterEventForm):
    layout = M.Layout(
        M.Row("published", "title"),
        M.Row(
            M.Column("date", span_columns=1),
            M.Column("register_startdate", span_columns=1),
            M.Column("register_deadline", span_columns=1),
            M.Column("deregister_deadline", span_columns=1),
        ),
        M.Row("location"),
        M.Row("description"),
        M.Row(M.Column("image"), M.Column("sluts")),
        M.Row("allowed_grades"),
    )

    class Meta(BaseRegisterEventForm.Meta):
        model = Bedpres
        fields = BaseRegisterEventForm.Meta.fields.copy()


class SocialRegisterUserForm(forms.ModelForm):
    approval = forms.BooleanField(
        required=True,
        label="Jeg har lest og godkjenner Høiskolens Chemikerforenings samtykkeerklæring for arrangementer",
        validators=[lambda x: x == True],
    )

    class Meta:
        model = SocialEventRegistration

        fields = [
            "companion",
            "sleepover",
            "night_snack",
            "registration_group_members",
        ]
        widgets = {
            "registration_group_members": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete"
            )
        }

    def __init__(self, *args, **kwargs):
        enable_sleepover = kwargs.pop("enable_sleepover", True)
        enable_night_snack = kwargs.pop("enable_night_snack", True)
        enable_companion = kwargs.pop("enable_companion", True)
        enable_registration_group_members = kwargs.pop(
            "enable_registration_group_members", True
        )
        super(SocialRegisterUserForm, self).__init__(*args, **kwargs)
        if not enable_sleepover:
            self.fields.pop("sleepover")
        if not enable_night_snack:
            self.fields.pop("night_snack")
        if not enable_companion:
            self.fields.pop("companion")
        if not enable_registration_group_members:
            self.fields.pop("enable_registration_group_members")


class BedpresRegisterUserForm(forms.ModelForm):
    approval = forms.BooleanField(
        required=True,
        label="Jeg har lest og godkjenner Høiskolens Chemikerforenings samtykkeerklæring for arrangementer",
        validators=[lambda x: x == True],
    )

    class Meta:
        model = BedpresRegistration
        fields = ()


class DeRegisterUserForm(forms.Form):
    really_sure = forms.BooleanField(
        required=True, label="Er dette ditt endelige svar?"
    )


class EditBaseRegistrationGroupForm(forms.ModelForm):
    class Meta:
        model = BaseRegistrationGroup
        fields = ("members",)
        widgets = {
            "members": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete"
            )
        }
